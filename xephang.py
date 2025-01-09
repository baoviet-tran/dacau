import unicodedata
import streamlit as st
from datetime import datetime
import requests
import json

# Thông tin GitHub (thay bằng thông tin của bạn)
GITHUB_TOKEN = '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'
GITHUB_USER = 'baoviet-tran'
GITHUB_REPO = 'dacau'
GITHUB_FILE_PATH = 'ranking_file.json'  # Đường dẫn tới file chứa danh sách xếp hạng

# Danh sách vận động viên mặc định
original_athletes = [
    "VŨ", "TÙNG", "LỘC", "CÔNG", "NGUYÊN", "NGHĨA", "DIỆN", "LONG", "DƯƠNG", "VĂN ANH", "THANH", 
    "TRƯỜNG", "VIỆT", "DŨNG", "PHÚC", "QUANG", "ĐỨC", "BÌNH", "VIỆT ANH", "SƠN 73", "QUYẾT", 
    "MẠNH", "HƯỜNG", "SƠN 96", "TUẤN", "NHÀN", "HỒI", "HẢI", "HUYÊN", "NGỌC", "QUYẾN"
]

# Hàm chuẩn hóa chuỗi (loại bỏ dấu và chuyển về chữ thường)
def normalize_name(name):
    nfkd_form = unicodedata.normalize('NFKD', name)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)]).lower()

# Hàm xếp hạng lại
def update_ranking(winner, loser, rankings):
    normalized_rankings = [normalize_name(a) for a in rankings]
    winner_index = normalized_rankings.index(normalize_name(winner))
    loser_index = normalized_rankings.index(normalize_name(loser))
    
    if loser_index < winner_index:
        rankings[winner_index], rankings[loser_index] = rankings[loser_index], rankings[winner_index]
         # Người thua sẽ lấy vị trí ngay sau người thắng mới nhận được
        loser = rankings.pop(loser_index)
        rankings.insert(winner_index + 1, loser)
        # Các người khác nằm giữa người thắng và người thua sẽ lùi xuống một bậc
        #for i in range(winner_index + 1, loser_index - 1):
            #rankings[i], rankings[i + 1] = rankings[i + 1], rankings[i]
    return rankings, winner_index, loser_index

# Hàm hiển thị bảng xếp hạng
def print_rankings(rankings):
    st.write("### BẢNG XẾP HẠNG ĐỘI CẦU VĂN PHÚ")
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    st.write(f"*Cập nhật lúc: {current_time}*")
    for i, athlete in enumerate(rankings, start=1):
        st.write(f"{i}: {athlete}")

# Hàm tải danh sách xếp hạng từ GitHub
def load_rankings_from_github():
    url = f'https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}'
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        file_content = response.json()['content']
        rankings = json.loads(requests.utils.unquote(file_content))
        return rankings
    else:
        st.error("Không thể tải dữ liệu từ GitHub, sử dụng danh sách mặc định.")
        return original_athletes.copy()

# Hàm cập nhật danh sách lên GitHub
def update_rankings_on_github(rankings):
    url = f'https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}'
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    
    # Lấy thông tin file hiện tại
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        file_info = response.json()
        sha = file_info['sha']  # Lấy sha của file hiện tại để cập nhật
        
        # Cập nhật nội dung mới
        content = json.dumps(rankings)
        encoded_content = requests.utils.quote(content)
        
        data = {
            'message': 'Cập nhật bảng xếp hạng',
            'content': encoded_content,
            'sha': sha
        }
        
        # Gửi yêu cầu PUT để cập nhật file
        response = requests.put(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            st.success("Bảng xếp hạng đã được cập nhật lên GitHub!")
        else:
            st.error("Lỗi khi cập nhật bảng xếp hạng lên GitHub.")
    else:
        st.error("Không thể tải thông tin file từ GitHub.")

# Giao diện Streamlit
if "athletes" not in st.session_state:
    st.session_state.athletes = load_rankings_from_github()

# Hiển thị bảng xếp hạng
print_rankings(st.session_state.athletes)

# Nhập kết quả trận đấu
st.write("#### Nhập kết quả trận đấu")
winner = st.text_input("Người thắng").strip()
loser = st.text_input("Người thua").strip()

if st.button("Cập nhật bảng xếp hạng"):
    normalized_athletes = [normalize_name(a) for a in st.session_state.athletes]
    if normalize_name(winner) in normalized_athletes and normalize_name(loser) in normalized_athletes:
        st.write(f"TRẬN ĐẤU GIỮA {winner.upper()} và {loser.upper()}")
        
        updated_rankings, winner_index, loser_index = update_ranking(winner, loser, st.session_state.athletes)
        
        if winner_index < loser_index:
            st.markdown(f"**Chúc mừng {winner.upper()} đã giữ vững phong độ!**", unsafe_allow_html=True)
        else:
            st.markdown(f"**Chúc mừng {winner.upper()} đã lên trình!**", unsafe_allow_html=True)
        
        st.session_state.athletes = updated_rankings
        st.write("#### Bảng xếp hạng cập nhật")
        print_rankings(st.session_state.athletes)
        
        # Cập nhật danh sách lên GitHub
        update_rankings_on_github(st.session_state.athletes)
    else:
        st.error("Lỗi: Vận động viên không có trong danh sách. Vui lòng kiểm tra lại.")
