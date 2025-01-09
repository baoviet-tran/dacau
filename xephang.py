import unicodedata
import streamlit as st
from datetime import datetime

# Danh sách vận động viên
original_athletes = [
    "VŨ", "TÙNG", "LỘC", "CÔNG", "NGUYÊN", "NGHĨA", "DIỆN", "LONG", "DƯƠNG", "VĂN ANH", "THANH", 
    "TRƯỜNG", "VIỆT", "DŨNG", "PHÚC", "QUANG", "ĐỨC", "BÌNH", "VIỆT ANH", "SƠN 73", "QUYẾT", 
    "MẠNH", "HƯỜNG", "SƠN 96", "TUẤN", "NHÀN", "HỒI", "HẢI", "HUYÊN", "NGỌC", "QUYẾN"
]

# Hàm chuẩn hóa chuỗi (loại bỏ dấu và chuyển về chữ thường)
def normalize_name(name):
    """
    Chuyển chuỗi thành dạng không dấu và chữ thường để so sánh.
    """
    nfkd_form = unicodedata.normalize('NFKD', name)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)]).lower()

# Hàm xếp hạng lại
def update_ranking(winner, loser, rankings):
    """
    winner: tên vận động viên thắng
    loser: tên vận động viên thua
    rankings: danh sách xếp hạng hiện tại
    """
    # Chuẩn hóa tên vận động viên
    normalized_rankings = [normalize_name(a) for a in rankings]
    winner_index = normalized_rankings.index(normalize_name(winner))
    loser_index = normalized_rankings.index(normalize_name(loser))
    
    # Nếu người thua có thứ hạng cao hơn, hoán đổi vị trí
    if loser_index < winner_index:
        rankings[winner_index], rankings[loser_index] = rankings[loser_index], rankings[winner_index]
    return rankings, winner_index, loser_index

# Hàm hiển thị bảng xếp hạng
def print_rankings(rankings):
    st.write("### BẢNG XẾP HẠNG ")
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    st.write(f"*Cập nhật lúc: {current_time}*")
    for i, athlete in enumerate(rankings, start=1):
        st.write(f"{i}: {athlete}")

# Giao diện Streamlit
st.title("ĐỘI CẦU VĂN PHÚ")

# Lưu trạng thái danh sách vận động viên
if "athletes" not in st.session_state:
    st.session_state.athletes = original_athletes.copy()

# Hiển thị bảng xếp hạng
print_rankings(st.session_state.athletes)

# Nhập kết quả trận đấu
st.write("#### Nhập kết quả trận đấu")
winner = st.text_input("Người thắng").strip()
loser = st.text_input("Người thua").strip()

if st.button("Cập nhật bảng xếp hạng"):
    # Kiểm tra tính hợp lệ của tên vận động viên
    normalized_athletes = [normalize_name(a) for a in st.session_state.athletes]
    if normalize_name(winner) in normalized_athletes and normalize_name(loser) in normalized_athletes:
        st.write(f"TRẬN ĐẤU GIỮA {winner.upper()} và {loser.upper()}")
        
        # Cập nhật bảng xếp hạng và lấy vị trí cũ của người thắng và người thua
        updated_rankings, winner_index, loser_index = update_ranking(winner, loser, st.session_state.athletes)
        
        # Kiểm tra nếu người thắng cuộc có thay đổi thứ hạng
        if winner_index < loser_index:
            st.markdown(f"**Chúc mừng {winner.upper()} đã lên trình!**", unsafe_allow_html=True)
        else:
            st.markdown(f"**Chúc mừng {winner.upper()} đã giữ vững phong độ!**", unsafe_allow_html=True)
        
        # Cập nhật lại bảng xếp hạng
        st.session_state.athletes = updated_rankings
        st.write("#### Bảng xếp hạng cập nhật")
        print_rankings(st.session_state.athletes)
    else:
        st.error("Lỗi: Vận động viên không có trong danh sách. Vui lòng kiểm tra lại.")
