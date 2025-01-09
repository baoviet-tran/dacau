import streamlit as st
import requests
import json
import unicodedata
from datetime import datetime

# Cấu hình GitHub
GITHUB_USER = 'your_github_username'
GITHUB_REPO = 'your_repository_name'
GITHUB_FILE_PATH = 'path/to/ranking_file.json'  # Đường dẫn đến file JSON trong repo
GITHUB_TOKEN = 'your_github_token'  # GitHub Access Token

# Hàm chuẩn hóa chuỗi (loại bỏ dấu và chuyển về chữ thường)
def normalize_name(name):
    nfkd_form = unicodedata.normalize('NFKD', name)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)]).lower()

# Hàm tải file xếp hạng từ GitHub
def load_rankings():
    url = f'https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}'
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        file_data = response.json()
        content = file_data['content']
        # Giải mã nội dung base64
        content_decoded = requests.utils.unquote(content)
        return json.loads(content_decoded)
    else:
        return []  # Trả về danh sách rỗng nếu không tìm thấy file

# Hàm lưu bảng xếp hạng lên GitHub
def save_rankings(rankings):
    url = f'https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}'
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    
    # Lấy thông tin file hiện tại từ GitHub
    file_data = requests.get(url, headers=headers).json()
    sha = file_data['sha']  # Lấy SHA của file để cập nhật
    
    # Mã hóa nội dung bảng xếp hạng thành base64
    content_encoded = requests.utils.quote(json.dumps(rankings, ensure_ascii=False, indent=4))
    
    # Cập nhật file trên GitHub
    data = {
        'message': 'Cập nhật bảng xếp hạng',
        'sha': sha,
        'content': content_encoded
    }
    
    response = requests.put(url, headers=headers, json=data)
    
    if response.status_code == 200:
        st.success("Bảng xếp hạng đã được lưu lên GitHub!")
    else:
        st.error("Lỗi khi cập nhật bảng xếp hạng trên GitHub.")

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
    
    # Nếu người thắng có vị trí cao hơn người thua, bảng xếp hạng không thay đổi
    if winner_index < loser_index:
        # Người thắng sẽ chiếm vị trí của người thua
        rankings[loser_index], rankings[winner_index] = rankings[winner_index], rankings[loser_index]
        
        # Người thua sẽ lấy vị trí ngay sau người thắng mới nhận được
        loser = rankings.pop(loser_index)
        rankings.insert(winner_index + 1, loser)
        
        # Các người khác giữa người thắng và người thua sẽ lùi xuống một bậc
        for i in range(winner_index + 1, loser_index):
            rankings[i], rankings[i + 1] = rankings[i + 1], rankings[i]
    
    return rankings
# Hàm hiển thị bảng xếp hạng
def print_rankings(rankings):
    st.write("### BẢNG XẾP HẠNG ĐỘI CẦU VĂN PHÚ")
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    st.write(f"*Cập nhật lúc: {current_time}*")
    for i, athlete in enumerate(rankings, start=1):
        st.write(f"{i}: {athlete}")

# Giao diện Streamlit
st.title("Quản lý Bảng Xếp Hạng Đội Cầu Văn Phú")

# Lưu trạng thái danh sách vận động viên
if "athletes" not in st.session_state:
    st.session_state.athletes = load_rankings() if load_rankings() else [
        "VŨ", "TÙNG", "LỘC", "CÔNG", "NGUYÊN", "NGHĨA", "DIỆN", "LONG", "DƯƠNG", "VĂN ANH", 
        "THANH", "TRƯỜNG", "VIỆT", "DŨNG", "PHÚC", "QUANG", "ĐỨC", "BÌNH", "VIỆT ANH", 
        "SƠN 73", "QUYẾT", "MẠNH", "HƯỜNG", "SƠN 96", "TUẤN", "NHÀN", "HỒI", "HẢI", "HUYÊN", "NGỌC", "QUYẾN"
    ]

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
        st.session_state.athletes = update_ranking(winner, loser, st.session_state.athletes)
        st.write("#### Bảng xếp hạng cập nhật")
        print_rankings(st.session_state.athletes)
        save_rankings(st.session_state.athletes)
    else:
        st.error("Lỗi: Vận động viên không có trong danh sách. Vui lòng kiểm tra lại.")
