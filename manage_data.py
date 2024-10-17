import os
from datetime import datetime, timedelta
from collections import defaultdict

def delete_old_data(backup_dir):
    # # 백업 데이터 폴더 경로
    # backup_dir = 'test_backup/'

    # 현재 날짜
    today = datetime.today()

    # 30일 전, 1년 전 날짜 계산
    thirty_days_ago = today - timedelta(days=30)
    one_year_ago = today - timedelta(days=365)

    # 파일 이름에서 날짜 추출하는 함수 (파일 이름 형식이 '2024-10-16'으로 되어 있다고 가정)
    def extract_date_from_filename(filename):
        try:
            return datetime.strptime(filename, "%Y-%m-%d")
        except ValueError:
            return None

    # 백업 데이터 파일들의 날짜별로 분류
    all_files = os.listdir(backup_dir)
    date_to_files = defaultdict(list)

    for file in all_files:
        file_date = extract_date_from_filename(file)
        if file_date:
            date_to_files[file_date].append(file)

    # 30일 이내의 파일은 모두 유지
    files_to_keep = set()

    # 30일 이후 파일 처리: 1달 단위로 1개, 12달 이전은 1년 단위로 1개
    monthly_files = defaultdict(list)
    yearly_files = defaultdict(list)

    for date, files in date_to_files.items():
        if date > thirty_days_ago:
            files_to_keep.update(files)  # 30일 이내의 파일은 모두 유지
        elif date > one_year_ago:
            # 30일 이전 ~ 1년 이내의 파일은 1달 단위로 1개씩만 유지
            monthly_key = (date.year, date.month)
            monthly_files[monthly_key].append((date, files))
        else:
            # 1년 이전의 파일은 1년 단위로 1개씩만 유지
            yearly_key = date.year
            yearly_files[yearly_key].append((date, files))

    # 1달 단위로 가장 최신 파일만 유지
    for files in monthly_files.values():
        latest_date, latest_files = max(files, key=lambda x: x[0])
        files_to_keep.update(latest_files)

    # 1년 단위로 가장 최신 파일만 유지
    for files in yearly_files.values():
        latest_date, latest_files = max(files, key=lambda x: x[0])
        files_to_keep.update(latest_files)

    # 삭제할 파일 리스트 구하기
    files_to_delete = set(all_files) - files_to_keep

    # 파일 삭제
    for file in files_to_delete:
        file_path = os.path.join(backup_dir, file)
        os.remove(file_path)
        print(f"Deleted: {file}")

if __name__ == "__main__":
    delete_old_data('test_backup/')