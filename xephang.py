# Danh sách vận động viên ban đầu
athletes = ["Athlete1", "Athlete2", "Athlete3", "Athlete4", "Athlete5", 
            "Athlete6", "Athlete7", "Athlete8", "Athlete9", "Athlete10"]

# Hàm xếp hạng lại
def update_ranking(winner, loser, rankings):
    """
    winner: tên vận động viên thắng
    loser: tên vận động viên thua
    rankings: danh sách xếp hạng hiện tại
    """
    # Tìm vị trí của người thắng và người thua
    winner_index = rankings.index(winner)
    loser_index = rankings.index(loser)
    
    # Nếu người thua có thứ hạng cao hơn, hoán đổi vị trí
    if loser_index < winner_index:
        rankings[winner_index], rankings[loser_index] = rankings[loser_index], rankings[winner_index]
    return rankings

# Hàm hiển thị bảng xếp hạng
def print_rankings(rankings):
    print("\nBẢNG XẾP HẠNG ĐỘI CẦU VĂN PHÚ")
    print("-" * 30)
    for i, athlete in enumerate(rankings, start=1):
        print(f"{i}: {athlete}")
    print("-" * 30)

# Hiển thị thứ hạng ban đầu
print_rankings(athletes)

# Cập nhật xếp hạng
while True:
    print("\nTRẬN ĐẤU GIỮA HAI VẬN ĐỘNG VIÊN")
    print("Nhập kết quả trận đấu:")
    winner = input("Người thắng: ").strip()
    loser = input("Người thua: ").strip()
    
    if winner.lower() == "exit" or loser.lower() == "exit":
        break
    
    if winner in athletes and loser in athletes:
        print(f"\nTRẬN ĐẤU GIỮA {winner.upper()} và {loser.upper()}")
        athletes = update_ranking(winner, loser, athletes)
        print("\nBẢNG XẾP HẠNG CẬP NHẬT")
        print_rankings(athletes)
    else:
        print("Lỗi: Vận động viên không có trong danh sách. Vui lòng nhập lại.")

print("\nKẾT THÚC CHƯƠNG TRÌNH. CẢM ƠN!")
