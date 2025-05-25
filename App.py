import streamlit as st
import re
import base64

# ❗️ PHẢI đặt dòng này TRƯỚC mọi lệnh Streamlit khác
st.set_page_config(page_title="Mở Link Tự Động", layout="centered")

# === Hàm đọc ảnh và chuyển sang base64 để nhúng vào CSS ===
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        b64_data = base64.b64encode(img_file.read()).decode()
        return f"data:image/jpeg;base64,{b64_data}"

# Đọc ảnh nền từ file a1.jpg
img_base64 = get_base64_image("a1.jpg")

# === CSS tuỳ chỉnh ảnh nền và giao diện ===
st.markdown(
    f"""
    <style>
    html, body, .stApp {{
        margin: 0;
        padding: 0;
        height: 100%;
    }}

    body {{
        background-image: url("{img_base64}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: 50% 50%;
    }}

    /* Ẩn header Streamlit */
    header {{
        visibility: hidden;
        height: 0px;
    }}

    .stApp {{
        backdrop-filter: blur(8px);
        background-color: rgba(0, 0, 0, 0.4);
        color: #fff;
    }}

    h1, h2, h3, h4, h5, h6, label, .stText, .stMarkdown {{
        color: #ffffff !important;
    }}

    textarea, .stTextArea textarea {{
        background-color: rgba(255, 255, 255, 0.9) !important;
        color: #000000 !important;
        font-weight: 500;
    }}

    .stButton > button {{
        background-color: #ffffff !important;
        color: #000000 !important;
        font-weight: bold;
        border: 2px solid #aaa;
    }}

    .stAlert {{
        background-color: rgba(0, 0, 0, 0.5) !important;
        color: #fff !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)


# === Giao diện người dùng ===
st.title("📎 Mỗi Link là 1 dòng")

raw_text = st.text_area("Dán link vào đây:", height=150, placeholder="Dán link vào đây, mỗi link trên một dòng...")

# === Xử lý URL: thay ViewPDF thành wpviewfile ===
def convert(link):
    return re.sub(r'ViewPDF', 'wpviewfile', link, flags=re.IGNORECASE)

# === Khi người dùng bấm nút chuẩn bị link ===
if st.button("✅ Đã cung cấp đủ link"):
    links = [convert(line.strip()) for line in raw_text.splitlines() if line.strip()]
    st.session_state.queue = links
    st.success(f"Đã chuẩn bị {len(links)} link.")

# === Nếu có queue link đã xử lý, cho phép mở toàn bộ link ===
if 'queue' in st.session_state and st.session_state.queue:
    remaining = len(st.session_state.queue)
    st.info(f"({remaining} bài cần được mở)")

    if st.button("🚀 Click để mở tất cả link ➜"):
        links_to_open = st.session_state.queue
        html_links = "\n".join(
            [f'<script>window.open("{link}", "_blank", "noopener");</script>' for link in links_to_open]
        )
        st.components.v1.html(html_links, height=0)
        st.session_state.queue = []
st.warning("⚠️Lưu ý nếu lúc sử dụng web này mà thông báo hiện biểu tượng chặn mở tab mới (như hình dưới). Hãy chọn 'Allow pop-ups' để cho phép tự động mở trang mới tài liệu. ⚠️")
st.image("a2.png", caption="Hình minh họa pop-up bị chặn", width=600)