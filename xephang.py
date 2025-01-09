import unicodedata
import streamlit as st

# Danh sách vận động viên
athletes = [
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
    return rankings

# Hàm hiển thị bảng xếp hạng
def print_rankings(rankings):
    st.write("### BẢNG XẾP HẠNG ĐỘI CẦU VĂN PHÚ")
    for i, athlete in enumerate(rankings, start=1):
        st.write(f"{i}: {athlete}")

# Giao diện Streamlit
st.title("Quản lý Bảng Xếp Hạng Đội Cầu Văn Phú")

# Hiển thị bảng xếp hạng ban đầu
st.write("#### Bảng xếp hạng ban đầu")
print_rankings(athletes)

# Nhập kết quả trận đấu
st.write("#### Nhập kết quả trận đấu")
winner = st.text_input("Người thắng").strip()
loser = st.text_input("Người thua").strip()

if st.button("Cập nhật bảng xếp hạng"):
    # Kiểm tra tính hợp lệ của tên vận động viên
    normalized_athletes = [normalize_name(a) for a in athletes]
    if normalize_name(winner) in normalized_athletes and normalize_name(loser) in normalized_athletes:
        st.write(f"TRẬN ĐẤU GIỮA {winner.upper()} và {loser.upper()}")
        athletes = update_ranking(winner, loser, athletes)
        st.write("#### Bảng xếp hạng cập nhật")
        print_rankings(athletes)
    else:
        st.error("Lỗi: Vận động viên không có trong danh sách. Vui lòng kiểm tra lại.")
