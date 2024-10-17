import os
import json
import pysftp
from datetime import datetime

# JSON 설정 파일 로드
def load_sftp_config(config_file):
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config

def backup_data_dir():
    # SFTP 설정 불러오기
    config = load_sftp_config('sftp_config.json')

    # 오늘 날짜를 가져와서 폴더 이름에 추가
    today = datetime.now().strftime('%Y-%m-%d')
    local_backup_dir_with_date = os.path.join(config['local_backup_dir'], today)

    # pysftp 옵션 (서버의 호스트 키 검증을 무시하기 위한 옵션 - 실제 운영 환경에서는 주의가 필요)
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None  # 테스트 시 보안 위험을 피하기 위해 설정. 실제 사용 시 서버의 host key를 확인하고 설정할 것.

    # SFTP 서버에 접속
    with pysftp.Connection(config['host'], username=config['username'], password=config['password'], cnopts=cnopts) as sftp:
        print("SFTP 연결 성공")

        # 날짜가 포함된 백업 폴더 경로가 없으면 생성
        if not os.path.exists(local_backup_dir_with_date):
            os.makedirs(local_backup_dir_with_date)

        # 폴더 전체를 다운로드하는 함수
        def backup_folder(remote_path, local_path):
            if sftp.isdir(remote_path):  # 원격 경로가 폴더인지 확인
                if not os.path.exists(local_path):
                    os.makedirs(local_path)  # 로컬에 해당 폴더가 없으면 생성
                for item in sftp.listdir(remote_path):  # 원격 폴더의 파일과 하위 폴더 목록 가져오기
                    remote_item_path = f"{remote_path}/{item}"
                    local_item_path = os.path.join(local_path, item)
                    if sftp.isdir(remote_item_path):
                        # 재귀적으로 하위 폴더 백업
                        backup_folder(remote_item_path, local_item_path)
                    else:
                        # 파일이면 다운로드
                        sftp.get(remote_item_path, local_item_path)
                        print(f"파일 다운로드 완료: {remote_item_path} -> {local_item_path}")
            else:
                print(f"{remote_path}는 폴더가 아닙니다.")

        # 원격 폴더 백업 시작
        backup_folder(config['remote_dir'], local_backup_dir_with_date)
        print(f"폴더 백업 완료: {local_backup_dir_with_date}")


if __name__ == "__main__":
    backup_data_dir()