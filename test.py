import os
from datetime import datetime, timedelta

# 테스트 폴더 경로
test_dir = 'test_backup/'

# 테스트 폴더 생성
if not os.path.exists(test_dir):
    os.makedirs(test_dir)

# 현재 날짜로부터 시작
today = datetime.today()

# 날짜 형식의 파일 생성 함수
def create_empty_file(path):
    with open(path, 'w') as f:
        pass  # 빈 파일 생성

# 테스트 파일 생성 (현재 날짜로부터 400일까지 랜덤하게 생성)
for i in range(2000):
    file_date = today - timedelta(days=i)
    file_name = file_date.strftime("%Y-%m-%d")  # 날짜 형식 파일명 'YYYY-MM-DD'
    file_path = os.path.join(test_dir, file_name)
    create_empty_file(file_path)

print(f"Generated {len(os.listdir(test_dir))} files in {test_dir}")
