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
# Thay đường link dưới đây bằng link "Publish to Web" định dạng CSV của bạn
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT1UXIB65E42LIrgxKSH2Mp0fw09NB3PC67AErwV5pFdP1e06KEBNytC7MdnlIhCANL7CNsWBa-WGOi/pub?output=csv"

@st.cache_data(ttl=600) # Lưu bộ nhớ đệm 10 phút để tăng tốc độ tải
def load_data():
    try:
        # Đọc dữ liệu và thay thế các ô trống bằng dấu "-"
        df = pd.read_csv(SHEET_URL)
        df = df.fillna("-")
        return df
    except:
        # Dữ liệu dự phòng khớp với cấu trúc mới
        data = [
            {"Từ gốc": "가다", "Loại": "Động từ", "Nghĩa (English)": "To go", "Hiện tại (-요)": "가요", "Quá khứ (-았/었)": "갔어요", "Tương lai (-ㄹ 거)": "갈 거예요", "Định ngữ": "-", "Tiếp diễn (-고 있어요)": "가고 있어요", "Ví dụ": "사무실에 가요."}
        ]
        return pd.DataFrame(data)

df = load_data()

# 4. GIAO DIỆN NGƯỜI DÙNG
st.title("📚 나의 한국어 사전")
st.write("Dữ liệu được cập nhật trực tiếp từ Google Sheets의 bạn.")

# Thanh tìm kiếm
search = st.text_input("🔍 Tìm kiếm từ vựng...", placeholder="Nhập từ tiếng Hàn hoặc tiếng Anh/Việt")

# Lọc dữ liệu (Sửa lại tên cột Nghĩa)
if search:
    df = df[df['Từ gốc'].str.contains(search, case=False) | df['Nghĩa (English)'].str.contains(search, case=False)]

# Hiển thị dạng lưới
cols = st.columns(3)
for idx, row in df.iterrows():
    with cols[idx % 3]:
        # Phân loại màu cho badge
        if row['Loại'] == "Động từ":
            badge_type = "badge-verb"
        elif row['Loại'] == "Tính từ":
            badge_type = "badge-adj"
        else:
            badge_type = "badge-noun"
        
        # Bỏ đi phần "Chủ đề" vì sheet không còn cột này
        st.markdown(f"""
        <div class="card-container">
            <span class="badge {badge_type}">{row['Loại']}</span>
            <div class="ko-title">{row['Từ gốc']}</div>
            <div class="vi-meaning">{row['Nghĩa (English)']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("Chi tiết chia thì & Ví dụ"):
            # Chia làm 2 cột nhỏ bên trong expander cho gọn gàng
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Hiện tại:** {row['Hiện tại (-요)']}")
                st.write(f"**Quá khứ:** {row['Quá khứ (-았/었)']}")
                st.write(f"**Tương lai:** {row['Tương lai (-ㄹ 거)']}")
            with col2:
                st.write(f"**Tiếp diễn:** {row['Tiếp diễn (-고 있어요)']}")
                st.write(f"**Định ngữ:** {row['Định ngữ']}")
            
            st.divider()
            st.info(f"💡 {row['Ví dụ']}")
