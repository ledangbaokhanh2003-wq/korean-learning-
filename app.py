import streamlit as st
import pandas as pd

# 1. CẤU HÌNH TRANG CƠ BẢN
st.set_page_config(
    page_title="나의 한국어 사전 | My Korean Hub",
    page_icon="🇰🇷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. TÙY CHỈNH CSS (PHONG CÁCH HÀN QUỐC TỐI GIẢN)
st.markdown("""
<style>
    /* Nhập font Noto Sans KR chuyên dụng cho tiếng Hàn */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    /* Tùy chỉnh màu nền và khoảng cách */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Thiết kế thẻ (Card) mềm mại */
    div[data-testid="stVerticalBlock"] div[data-testid="stVerticalBlock"] {
        background-color: #ffffff;
        border-radius: 16px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    div[data-testid="stVerticalBlock"] div[data-testid="stVerticalBlock"]:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }

    /* Typography cho Tiếng Hàn */
    .ko-title {
        font-size: 24px;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 4px;
    }
    
    .vi-meaning {
        font-size: 15px;
        color: #666666;
        margin-bottom: 16px;
    }

    /* Thiết kế Nhãn dán (Badges) phong cách Kakao/Naver */
    .badge-noun {
        background-color: #F1F3F5;
        color: #495057;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
        display: inline-block;
        margin-right: 6px;
    }
    .badge-verb {
        background-color: #E6F4EA;
        color: #137333;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
        display: inline-block;
        margin-right: 6px;
    }
    .badge-topic {
        background-color: #FCE8E6;
        color: #C5221F;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
        display: inline-block;
    }
    
    /* Dòng phân cách mờ */
    hr {
        margin-top: 0.5rem;
        margin-bottom: 1rem;
        border: 0;
        border-top: 1px solid #F1F3F5;
    }
</style>
""", unsafe_allow_html=True)

# 3. DỮ LIỆU MẪU (Mô phỏng dữ liệu kéo về từ Google Sheets)
@st.cache_data
def load_mock_data():
    data = [
        {"root": "가다", "type": "Động từ", "meaning": "Đi", "present": "가요", "past": "갔어요", "future": "갈 거예요", "topic": "Đời sống", "example": "저는 사무실에 가요 (Tôi đi đến văn phòng)."},
        {"root": "먹다", "type": "Động từ", "meaning": "Ăn", "present": "먹어요", "past": "먹었어요", "future": "먹을 거예요", "topic": "Đời sống", "example": "점심을 먹어요 (Ăn trưa)."},
        {"root": "교재", "type": "Danh từ", "meaning": "Giáo trình", "present": "-", "past": "-", "future": "-", "topic": "Giáo dục", "example": "새 교재를 준비했어요 (Tôi đã chuẩn bị giáo trình mới)."},
        {"root": "회의", "type": "Danh từ", "meaning": "Cuộc họp", "present": "-", "past": "-", "future": "-", "topic": "Văn phòng", "example": "오늘 회의가 있어요? (Hôm nay có họp không?)."},
        {"root": "주문하다", "type": "Động từ", "meaning": "Gọi món / Đặt hàng", "present": "주문해요", "past": "주문했어요", "future": "주문할 거예요", "topic": "Đời sống", "example": "제가 커피를 주문할게요 (Tôi sẽ gọi cà phê)."},
        {"root": "사장님", "type": "Danh từ", "meaning": "Giám đốc", "present": "-", "past": "-", "future": "-", "topic": "Văn phòng", "example": "사장님, 안녕하세요! (Chào Giám đốc!)."}
    ]
    return pd.DataFrame(data)

df = load_mock_data()

# 4. GIAO DIỆN CHÍNH (UI)
st.title("📚 나의 한국어 사전 (Thư viện Tiếng Hàn)")
st.markdown("<p style='color: #868e96; font-size: 16px; margin-top: -10px;'>Trạm lưu trữ từ vựng và ngữ pháp cá nhân hóa.</p>", unsafe_allow_html=True)

# Sidebar (Menu điều hướng)
with st.sidebar:
    st.header("메뉴 (Menu)")
    menu = st.radio("Chọn chức năng:", ["📖 Tra cứu từ vựng", "📝 Ôn tập ngữ pháp", "⚙️ Cài đặt Database"])
    st.markdown("---")
    st.markdown("Tiến độ hôm nay:")
    st.progress(60)
    st.caption("Đã học 6/10 từ")

# --- CHỨC NĂNG TRA CỨU TỪ VỰNG ---
if menu == "📖 Tra cứu từ vựng":
    
    # Thanh công cụ tìm kiếm và lọc
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("🔍 Tìm kiếm tiếng Hàn hoặc tiếng Việt...", placeholder="Ví dụ: 회의, ăn, đi...")
    with col2:
        topic_filter = st.selectbox("📂 Lọc theo chủ đề", ["Tất cả", "Văn phòng", "Đời sống", "Giáo dục"])

    # Xử lý logic lọc dữ liệu
    filtered_df = df.copy()
    if search_query:
        filtered_df = filtered_df[
            filtered_df['root'].str.contains(search_query, case=False) | 
            filtered_df['meaning'].str.contains(search_query, case=False)
        ]
    if topic_filter != "Tất cả":
        filtered_df = filtered_df[filtered_df['topic'] == topic_filter]

    st.markdown("<br>", unsafe_allow_html=True)

    # Hiển thị dữ liệu dạng Grid (Lưới Card)
    # Chia làm 3 cột để thẻ nhìn gọn gàng
    cols = st.columns(3)
    
    for index, row in filtered_df.iterrows():
        # Phân bổ các thẻ đều vào 3 cột
        with cols[index % 3]:
            # Dùng container có viền để tạo thẻ (Card)
            with st.container(border=True):
                # CSS cho Loại từ
                badge_class = "badge-verb" if row['type'] == "Động từ" else "badge-noun"
                
                # Render nội dung thẻ bằng HTML để ép font và màu sắc chuẩn Hàn
                st.markdown(f"""
                <div>
                    <span class='{badge_class}'>{row['type']}</span>
                    <span class='badge-topic'>{row['topic']}</span>
                    <div class='ko-title'>{row['root']}</div>
                    <div class='vi-meaning'>{row['meaning']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Nút mở rộng để xem chia thì và ví dụ
                with st.expander("Xem chi tiết & Chia thì"):
                    if row['type'] == "Động từ":
                        # Hiển thị bảng chia thì siêu gọn
                        st.markdown("**🔄 Chia thì:**")
                        st.markdown(f"- **Hiện tại:** {row['present']}")
                        st.markdown(f"- **Quá khứ:** {row['past']}")
                        st.markdown(f"- **Tương lai:** {row['future']}")
                        st.markdown("<hr>", unsafe_allow_html=True)
                        
                    st.markdown("**💬 Ví dụ:**")
                    st.info(row['example'])

elif menu == "📝 Ôn tập ngữ pháp":
    st.subheader("🛠️ Cấu trúc ngữ pháp đang xây dựng...")
    st.info("Tính năng này sẽ kết nối với tab Ngữ pháp trên Google Sheets của bạn.")

elif menu == "⚙️ Cài đặt Database":
    st.subheader("Kết nối Google Sheets")
    st.text_input("Nhập Google Sheet ID (Dành cho kết nối API):", type="password")
    st.button("Lưu cấu hình")
    
    st.markdown("---")
    st.write("Dữ liệu thô (Raw Data View):")
    st.dataframe(df, use_container_width=True)
