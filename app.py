import streamlit as st
import pandas as pd

# 1. CẤU HÌNH TRANG
st.set_page_config(
    page_title="나의 한국어 사전 | My Korean Hub",
    page_icon="🇰🇷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. TÙY CHỈNH CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
    
    /* 🌟 BỘ LỌC THÔNG MINH CHO SÁNG/TỐI (TỰ ĐỘNG) */
    :root {
        --card-bg: #ffffff;
        --card-border: #F1F3F5;
        --card-hover: #e9ecef;
        --text-main: #212529;
        --text-sub: #495057;
        --grammar-bg: #F8F9FA;
    }

    @media (prefers-color-scheme: dark) {
        :root {
            --card-bg: #262730; /* Nền xám đậm cho thẻ */
            --card-border: #444444; /* Viền tối màu */
            --card-hover: #666666;
            --text-main: #FAFAFA; /* Chữ màu trắng sáng */
            --text-sub: #CCCCCC; /* Chữ xám nhạt */
            --grammar-bg: #1E1E1E;
        }
    }

    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    .block-container { padding-top: 2rem; }
    
    /* Thiết kế thẻ Card cho Từ vựng */
    .card-container {
        background-color: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        transition: all 0.2s ease;
    }
    .card-container:hover {
        box-shadow: 0 8px 24px rgba(0,0,0,0.05);
        border-color: var(--card-hover);
    }

    /* Thiết kế thẻ Card riêng cho Ngữ pháp */
    .grammar-card {
        background-color: var(--grammar-bg);
        border-left: 5px solid #4285F4;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 15px;
    }

    .ko-title { font-size: 26px; font-weight: 700; color: var(--text-main); margin-bottom: 2px; }
    .vi-meaning { font-size: 16px; color: var(--text-sub); margin-bottom: 12px; }
    .grammar-title { font-size: 22px; font-weight: 700; color: #1A73E8; margin-bottom: 8px; }

    .badge { padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 500; margin-right: 6px; }
    .badge-verb { background-color: #E6F4EA; color: #137333; }
    .badge-noun { background-color: #F1F3F5; color: #495057; }
    .badge-adj { background-color: #FFF0F5; color: #C2185B; }
</style>
""", unsafe_allow_html=True)

# 3. KẾT NỐI DỮ LIỆU GOOGLE SHEETS
# Bạn hãy dán 2 link CSV tương ứng vào dưới đây:
VOCAB_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT1UXIB65E42LIrgxKSH2Mp0fw09NB3PC67AErwV5pFdP1e06KEBNytC7MdnlIhCANL7CNsWBa-WGOi/pub?gid=0&single=true&output=csv"
GRAMMAR_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT1UXIB65E42LIrgxKSH2Mp0fw09NB3PC67AErwV5pFdP1e06KEBNytC7MdnlIhCANL7CNsWBa-WGOi/pub?gid=954320771&single=true&output=csv" 

@st.cache_data(ttl=600)
def load_data(url, is_grammar=False):
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        df = df.fillna("-")
        return df
    except Exception as e:
        st.error(f"⚠️ Lỗi đọc Google Sheets: {e}")
        st.warning("Đang hiển thị dữ liệu dự phòng. Vui lòng kiểm tra lại link 'Publish to web'.")
        if is_grammar:
            data = [{"Cấu trúc": "-아/어서", "Ý nghĩa": "Vì... nên...", "Ví dụ": "비가 와서 집에 있어요.", "Ghi chú": "Không dùng đuôi mệnh lệnh"}]
            return pd.DataFrame(data)
        else:
            data = [{"Từ gốc": "가다", "Loại": "Động từ", "Nghĩa (English)": "To go", "Hiện tại (-요)": "가요", "Quá khứ (-았/었)": "갔어요", "Tương lai (-ㄹ 거예요)": "갈 거예요", "Định ngữ": "-", "Tiếp diễn (-고 있어요)": "가고 있어요", "Ví dụ": "사무실에 가요."}]
            return pd.DataFrame(data)

df_vocab = load_data(VOCAB_URL, is_grammar=False)
df_grammar = load_data(GRAMMAR_URL, is_grammar=True)

# 4. THANH MENU BÊN TRÁI (SIDEBAR)
with st.sidebar:
    st.image("https://flagcdn.com/w160/kr.png", width=60) # Logo cờ Hàn Quốc chuẩn
    st.title("Menu")
    menu = st.radio("Chọn không gian học tập:", ["📖 Từ vựng", "📝 Ngữ pháp"])
    st.markdown("---")
    st.caption("Cập nhật dữ liệu trực tiếp từ Google Sheets.")

# ==========================================
# KHÔNG GIAN 1: TỪ VỰNG (Giữ nguyên như cũ)
# ==========================================
if menu == "📖 Từ vựng":
    st.title("📚 나의 한국어 사전 (Từ Vựng)")
    st.markdown("<p style='color: var(--text-sub); font-size: 16px; margin-top: -10px;'>Trạm lưu trữ từ vựng cá nhân hóa.</p>", unsafe_allow_html=True)
    st.divider()

    search = st.text_input("🔍 Tìm kiếm từ vựng...", placeholder="Nhập từ tiếng Hàn hoặc tiếng Anh/Việt")

    if search:
        df_display = df_vocab[df_vocab['Từ gốc'].str.contains(search, case=False) | df_vocab['Nghĩa (English)'].str.contains(search, case=False)]
    else:
        df_display = df_vocab

    def render_cards(data, tab_key):
        if data.empty:
            st.warning("Không tìm thấy từ vựng nào trong mục này. 😅")
            return

        items_per_page = 9 
        total_pages = (len(data) // items_per_page) + (1 if len(data) % items_per_page > 0 else 0)
        
        page_num = 1
        if total_pages > 1:
            col_space, col_page = st.columns([8, 2])
            with col_page:
                page_num = st.number_input("Trang", min_value=1, max_value=total_pages, step=1, key=f"page_{tab_key}")

        start_idx = (page_num - 1) * items_per_page
        end_idx = start_idx + items_per_page
        page_data = data.iloc[start_idx:end_idx]

        cols = st.columns(3)
        for idx, (original_idx, row) in enumerate(page_data.iterrows()):
            with cols[idx % 3]:
                if row['Loại'] == "Động từ": badge_type = "badge-verb"
                elif row['Loại'] == "Tính từ": badge_type = "badge-adj"
                else: badge_type = "badge-noun"
                
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

    tab_all, tab_verb, tab_adj, tab_noun = st.tabs(["🌎 Tất cả", "🏃 Động từ", "🎨 Tính từ", "📦 Danh từ & Khác"])

    with tab_all: render_cards(df_display, "all")
    with tab_verb: render_cards(df_display[df_display['Loại'] == "Động từ"], "verb")
    with tab_adj: render_cards(df_display[df_display['Loại'] == "Tính từ"], "adj")
    with tab_noun: render_cards(df_display[~df_display['Loại'].isin(["Động từ", "Tính từ"])], "noun")

# ==========================================
# KHÔNG GIAN 2: NGỮ PHÁP (Mới)
# ==========================================
elif menu == "📝 Ngữ pháp":
    st.title("📝 Sổ tay Ngữ pháp")
    st.markdown("<p style='color: var(--text-sub); font-size: 16px; margin-top: -10px;'>Hệ thống hóa cấu trúc câu tiếng Hàn.</p>", unsafe_allow_html=True)
    st.divider()

    search_g = st.text_input("🔍 Tìm kiếm cấu trúc...", placeholder="Nhập ngữ pháp hoặc ý nghĩa tiếng Việt...")

    if search_g:
        df_g_display = df_grammar[df_grammar['Cấu trúc'].str.contains(search_g, case=False) | df_grammar['Ý nghĩa'].str.contains(search_g, case=False)]
    else:
        df_g_display = df_grammar

    if df_g_display.empty:
        st.warning("Không tìm thấy ngữ pháp phù hợp.")
    else:
        # Hiển thị từng ngữ pháp dạng danh sách từ trên xuống
        for idx, row in df_g_display.iterrows():
            st.markdown(f"""
            <div class="grammar-card">
                <div class="grammar-title">{row.get('Cấu trúc', '-')}</div>
                <div style="font-size: 16px; margin-bottom: 10px;"><b>Ý nghĩa:</b> {row.get('Ý nghĩa', '-')}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if row.get('Ghi chú', '-') != "-":
                st.caption(f"⚠️ **Lưu ý:** {row.get('Ghi chú', '-')}")
                
            with st.expander("💬 Xem ví dụ chi tiết"):
                st.success(row.get('Ví dụ', '-'))
            st.write("") # Tạo khoảng trống giữa các ngữ pháp
