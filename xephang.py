import unicodedata
import streamlit as st
import json
import requests
from datetime import datetime

# Danh sách vận động viên
original_athletes = [
    "VŨ", "TÙNG", "LỘC", "CÔNG", "NGUYÊN", "NGHĨA", "DIỆN", "LONG", "DƯƠNG", "VĂN ANH", "THANH", 
    "TRƯỜNG", "VIỆT", "DŨNG", "PHÚC", "QUANG", "ĐỨC", "BÌNH", "VIỆT ANH", "SƠN 73", "QUYẾT", 
    "MẠNH", "HƯỜNG", "SƠN 96", "TUẤN", "NHÀN", "HỒI", "HẢI", "HUYÊN", "NGỌC", "QUYẾN"
]

# Thông tin GitHub (thay bằng thông tin của bạn)
GITHUB_TOKEN = 'your_github_token'
GITHUB_USER = 'your_github_username'
GITHUB_REPO = 'your_repository_name'
GITHUB_FILE_PATH = 'path/to/your/ranking_file.json'

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
    
    # Nếu người thắng có vị trí thấp hơn người thua, người thắng sẽ chiếm vị trí người thua
    if winner_index > loser_index:
        # Người thắng sẽ lấy vị trí của người thua, người thua sẽ lùi một bậc
        rankings[loser_index], rankings[winner_index] = rankings[winner_index], rankings[loser_index]
        rankings.insert(loser_index + 1, rankings.pop(winner_index + 1))
    
    # Nếu người thắng có vị trí cao hơn người thua, không thay đổi bảng xếp hạng
    return rankings

# Hàm hiển thị bảng xếp hạng
def print_rankings(rankings):
    st.write("### BẢNG XẾP HẠNG ĐỘI CẦU VĂN PHÚ")
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    st.write(f"*Cập nhật lúc: {current_time}*")
    for i, athlete in enumerate(rankings, start=1):
        st.write(f"{i}: {athlete}")

# Hàm tải file từ GitHub
def get_github_file():
    url = f'https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}'
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        file_info = response.json()
        content = file_info['content']
        return json.loads(requests.utils.unquote(content))
    else:
        st.error(f"Lỗi tải file từ GitHub: {response.status_code}, {response.text}")
        return original_athletes

# Hàm cập nhật file lên GitHub
def update_github_file(rankings):
    url = f'https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}'
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    
    # Lấy SHA của file hiện tại
    file_info = get_github_file()
    if file_info is None:
        return
    
    sha = file_info['sha']
    
    # Mã hóa nội dung thành Base64
    encoded_content = requests.utils.quote(json.dumps(rankings))
    
    data = {
        'message': 'Cập nhật bảng xếp hạng',
        'content': encoded_content,
        'sha': sha
    }
    
    response = requests.put(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        st.success("Bảng xếp hạng đã được cập nhật lên GitHub!")
    else:
        st.error(f"Lỗi khi cập nhật file lên GitHub: {response.status_code}, {response.text}")

# Giao diện Streamlit
#st.title("Quản lý Bảng Xếp Hạng Đội Cầu Văn Phú")

# Lưu trạng thái danh sách vận động viên
if "athletes" not in st.session_state:
    st.session_state.athletes = get_github_file()

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
        
        # Cập nhật danh sách lên GitHub
        update_github_file(st.session_state.athletes)
    else:
        st.error("Lỗi: Vận động viên không có trong danh sách. Vui lòng kiểm tra lại.")
