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

if __name__ == "__main__":
    run()