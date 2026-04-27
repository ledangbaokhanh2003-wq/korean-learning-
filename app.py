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
    .badge-topic { background-color: #FCE8E6; color: #C5221F; }
</style>
""", unsafe_allow_html=True)

# 3. KẾT NỐI DỮ LIỆU GOOGLE SHEETS
# Thay đường link dưới đây bằng link "Publish to Web" định dạng CSV của bạn
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT1UXIB65E42LIrgxKSH2Mp0fw09NB3PC67AErwV5pFdP1e06KEBNytC7MdnlIhCANL7CNsWBa-WGOi/pub?output=csv"

@st.cache_data(ttl=600) # Lưu bộ nhớ đệm 10 phút để tăng tốc độ tải
def load_data():
    try:
        # Nếu chưa có link thật, dùng dữ liệu mẫu để demo
        df = pd.read_csv(SHEET_URL)
        return df
    except:
        # Dữ liệu dự phòng nếu link Sheets lỗi
        data = [
            {"Từ gốc": "가다", "Loại từ": "Động từ", "Nghĩa": "Đi", "Hiện tại": "가요", "Quá khứ": "갔어요", "Chủ đề": "Đời sống", "Ví dụ": "저는 사무실에 가요."},
            {"Từ gốc": "교재", "Loại từ": "Danh từ", "Nghĩa": "Giáo trình", "Hiện tại": "-", "Quá khứ": "-", "Chủ đề": "Giáo dục", "Ví dụ": "새 교재가 있어요."}
        ]
        return pd.DataFrame(data)

df = load_data()

# 4. GIAO DIỆN NGƯỜI DÙNG
st.title("📚 나의 한국어 사전")
st.write("Dữ liệu được cập nhật trực tiếp từ Google Sheets của bạn.")

# Thanh tìm kiếm
search = st.text_input("🔍 Tìm kiếm từ vựng...", placeholder="Nhập từ tiếng Hàn hoặc tiếng Việt")

# Lọc dữ liệu
if search:
    df = df[df['Từ gốc'].str.contains(search, case=False) | df['Nghĩa'].str.contains(search, case=False)]

# Hiển thị dạng lưới
cols = st.columns(3)
for idx, row in df.iterrows():
    with cols[idx % 3]:
        badge_type = "badge-verb" if row['Loại từ'] == "Động từ" else "badge-noun"
        
        st.markdown(f"""
        <div class="card-container">
            <span class="badge {badge_type}">{row['Loại từ']}</span>
            <span class="badge badge-topic">{row['Chủ đề']}</span>
            <div class="ko-title">{row['Từ gốc']}</div>
            <div class="vi-meaning">{row['Nghĩa']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("Chi tiết chia thì & Ví dụ"):
            st.write(f"**Hiện tại:** {row['Hiện tại']}")
            st.write(f"**Quá khứ:** {row['Quá khứ']}")
            st.divider()
            st.info(f"💡 {row['Ví dụ']}")
