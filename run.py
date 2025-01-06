import schedule
import time
from datetime import datetime
from backup_db import backup_all_db_tables
from backup_data import backup_data_dir
from manage_data import delete_old_data

def run():
    db_dir = '/home/user/data_backup/db_backup/'
    data_dir = '/home/user/data_backup/data_backup/'

    # delete_old_data('/home/user/data_backup/test_backup/')
    
    delete_old_data(db_dir)
    delete_old_data(data_dir)

    backup_all_db_tables(db_dir)
    backup_data_dir()

# 매일 오전 4시에 run 함수를 실행하는 작업 예약
schedule.every().day.at("04:00").do(run)

if __name__ == "__main__":
    while True:
        schedule.run_pending()  # 예약된 작업 실행
        time.sleep(1)  # 1초 대기 후 다시 확인