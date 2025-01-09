import unicodedata
import streamlit as st
import json
from datetime import datetime

# Danh sách vận động viên
original_athletes = [
    "VŨ", "TÙNG", "LỘC", "CÔNG", "NGUYÊN", "NGHĨA", "DIỆN", "LONG", "DƯƠNG", "VĂN ANH", "THANH", 
    "TRƯỜNG", "VIỆT", "DŨNG", "PHÚC", "QUANG", "ĐỨC", "BÌNH", "VIỆT ANH", "SƠN 73", "QUYẾT", 
    "MẠNH", "HƯỜNG", "SƠN 96", "TUẤN", "NHÀN", "HỒI", "HẢI", "HUYÊN", "NGỌC", "QUYẾN"
]

# Đường dẫn file xếp hạng
RANKING_FILE_PATH = 'ranking_file.json'

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
    
    # Nếu người thắng có vị trí thấp hơn người thua, người thắng sẽ chiếm vị trí của người thua
    if winner_index < loser_index:
        # Lưu vị trí của người thua trước khi đấu
        original_loser_index = loser_index
        
        # Người thắng chiếm vị trí của người thua, người thua sẽ lùi một bậc
        rankings[loser_index], rankings[winner_index] = rankings[winner_index], rankings[loser_index]
        
        # Người thua lùi một bậc so với vị trí trước khi đấu
        rankings.insert(original_loser_index + 1, rankings.pop(winner_index + 1))
    
    # Nếu người thắng có vị trí cao hơn người thua, không thay đổi bảng xếp hạng
    return rankings

# Hàm hiển thị bảng xếp hạng
def print_rankings(rankings):
    st.write("### BẢNG XẾP HẠNG ĐỘI CẦU VĂN PHÚ")
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    st.write(f"*Cập nhật lúc: {current_time}*")
    for i, athlete in enumerate(rankings, start=1):
        st.write(f"{i}: {athlete}")

# Hàm tải file xếp hạng từ hệ thống
def load_rankings():
    try:
        with open(RANKING_FILE_PATH, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return original_athletes

# Hàm lưu bảng xếp hạng lên hệ thống
def save_rankings(rankings):
    with open(RANKING_FILE_PATH, 'w', encoding='utf-8') as file:
        json.dump(rankings, file, ensure_ascii=False, indent=4)

# Giao diện Streamlit
#st.title("Quản lý Bảng Xếp Hạng Đội Cầu Văn Phú")

# Lưu trạng thái danh sách vận động viên
if "athletes" not in st.session_state:
    st.session_state.athletes = load_rankings()

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
        
        # Cập nhật bảng xếp hạng
        st.session_state.athletes = update_ranking(winner, loser, st.session_state.athletes)
        
        # Hiển thị bảng xếp hạng cập nhật
        st.write("#### Bảng xếp hạng cập nhật")
        print_rankings(st.session_state.athletes)
        
        # Hiển thị thông báo chúc mừng
        winner_index = normalized_athletes.index(normalize_name(winner))
        loser_index = normalized_athletes.index(normalize_name(loser))
        
        if winner_index < loser_index:
            st.markdown(f"**Chúc mừng {winner.upper()} đã giữ vững phong độ!**")
        else:
            st.markdown(f"**Chúc mừng {winner.upper()} đã lên trình!**")
        
        # Lưu bảng xếp hạng mới vào file
        save_rankings(st.session_state.athletes)
        st.success("Bảng xếp hạng đã được lưu!")
    else:
        st.error("Lỗi: Vận động viên không có trong danh sách. Vui lòng kiểm tra lại.")
