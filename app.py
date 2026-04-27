import streamlit as st
import pandas as pd

# 1. CẤU HÌNH TRANG
st.set_page_config(
    page_title="나의 한국어 사전 | My Korean Hub",
    page_icon="🇰🇷",
    layout="wide"
)

# 2. TÙY CHỈNH CSS (PHONG CÁCH HÀN QUỐC TỐI GIẢN)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    .block-container {
        padding-top: 2rem;
    }
    
    .stAlert {
        border-radius: 12px;
    }

    /* Thiết kế thẻ Card */
    .card-container {
        background-color: #ffffff;
        border: 1px solid #F1F3F5;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        transition: all 0.2s ease;
    }
    
    .card-container:hover {
        box-shadow: 0 8px 24px rgba(0,0,0,0.05);
        border-color: #e9ecef;
    }

    .ko-title {
        font-size: 26px;
        font-weight: 700;
        color: #212529;
        margin-bottom: 2px;
    }
    
    .vi-meaning {
        font-size: 16px;
        color: #495057;
        margin-bottom: 12px;
    }

    .badge {
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
        margin-right: 6px;
    }
    
    .badge-verb { background-color: #E6F4EA; color: #137333; }
    .badge-noun { background-color: #F1F3F5; color: #495057; }
    .badge-adj { background-color: #FFF0F5; color: #C2185B; } /* Thêm màu cho Tính từ */
</style>
""", unsafe_allow_html=True)

# 3. KẾT NỐI DỮ LIỆU GOOGLE SHEETS
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT1UXIB65E42LIrgxKSH2Mp0fw09NB3PC67AErwV5pFdP1e06KEBNytC7MdnlIhCANL7CNsWBa-WGOi/pub?output=csv"

@st.cache_data(ttl=600)
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = df.columns.str.strip()
        df = df.fillna("-")
        return df
    except:
        data = [
            {"Từ gốc": "가다", "Loại": "Động từ", "Nghĩa (English)": "To go", "Hiện tại (-요)": "가요", "Quá khứ (-았/었)": "갔어요", "Tương lai (-ㄹ 거예요)": "갈 거예요", "Định ngữ": "-", "Tiếp diễn (-고 있어요)": "가고 있어요", "Ví dụ": "사무실에 가요."}
        ]
        return pd.DataFrame(data)

df = load_data()

# 4. GIAO DIỆN NGƯỜI DÙNG
st.title("📚 나의 한국어 사전")
st.markdown("<p style='color: #868e96; font-size: 16px; margin-top: -10px;'>Trạm lưu trữ từ vựng cá nhân hóa (Đồng bộ với Google Sheets).</p>", unsafe_allow_html=True)
st.divider()

# Thanh tìm kiếm
search = st.text_input("🔍 Tìm kiếm từ vựng...", placeholder="Nhập từ tiếng Hàn hoặc tiếng Anh/Việt")

# Lọc dữ liệu theo tìm kiếm
if search:
    df_display = df[df['Từ gốc'].str.contains(search, case=False) | df['Nghĩa (English)'].str.contains(search, case=False)]
else:
    df_display = df

# HÀM HIỂN THỊ DANH SÁCH DẠNG LƯỚI CÓ PHÂN TRANG
def render_cards(data, tab_key):
    if data.empty:
        st.warning("Không tìm thấy từ vựng nào trong mục này. 😅")
        return

    # Thiết lập phân trang
    items_per_page = 9 # Tối đa 9 từ (3 hàng) 1 trang
    total_pages = (len(data) // items_per_page) + (1 if len(data) % items_per_page > 0 else 0)
    
    # UI Chọn trang (Chỉ hiển thị nếu có lớn hơn 1 trang)
    page_num = 1
    if total_pages > 1:
        col_space, col_page = st.columns([8, 2])
        with col_page:
            page_num = st.number_input("Trang", min_value=1, max_value=total_pages, step=1, key=f"page_{tab_key}")
            st.caption(f"Tổng số: {total_pages} trang")

    # Tính toán dữ liệu hiển thị cho trang hiện tại
    start_idx = (page_num - 1) * items_per_page
    end_idx = start_idx + items_per_page
    page_data = data.iloc[start_idx:end_idx]

    # Hiển thị lưới Card
    cols = st.columns(3)
    for idx, (original_idx, row) in enumerate(page_data.iterrows()):
        with cols[idx % 3]:
            # Phân loại màu cho badge
            if row['Loại'] == "Động từ":
                badge_type = "badge-verb"
            elif row['Loại'] == "Tính từ":
                badge_type = "badge-adj"
            else:
                badge_type = "badge-noun"
            
            st.markdown(f"""
            <div class="card-container">
                <span class="badge {badge_type}">{row['Loại']}</span>
                <div class="ko-title">{row['Từ gốc']}</div>
                <div class="vi-meaning">{row['Nghĩa (English)']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("Chi tiết chia thì & Ví dụ"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Hiện tại:** {row.get('Hiện tại (-요)', '-')}")
                    st.write(f"**Quá khứ:** {row.get('Quá khứ (-았/었)', '-')}")
                    st.write(f"**Tương lai:** {row.get('Tương lai (-ㄹ 거예요)', '-')}")
                with col2:
                    st.write(f"**Tiếp diễn:** {row.get('Tiếp diễn (-고 있어요)', '-')}")
                    st.write(f"**Định ngữ:** {row.get('Định ngữ', '-')}")
                
                st.divider()
                st.info(f"💡 {row.get('Ví dụ', '-')}")

# 5. TẠO CÁC TAB ĐỂ PHÂN LOẠI
tab_all, tab_verb, tab_adj, tab_noun = st.tabs(["🌎 Tất cả", "🏃 Động từ", "🎨 Tính từ", "📦 Danh từ & Khác"])

with tab_all:
    render_cards(df_display, "all")

with tab_verb:
    render_cards(df_display[df_display['Loại'] == "Động từ"], "verb")

with tab_adj:
    render_cards(df_display[df_display['Loại'] == "Tính từ"], "adj")

with tab_noun:
    # Lấy các từ không phải Động từ và Tính từ (Danh từ, Trợ từ...)
    render_cards(df_display[~df_display['Loại'].isin(["Động từ", "Tính từ"])], "noun")
