import mysql.connector
import os
import csv
import json
from datetime import datetime

# JSON 파일에서 데이터베이스 정보를 읽어오는 함수
def load_db_config(json_file):
    with open(json_file, 'r') as file:
        config = json.load(file)
    return config

# 데이터베이스에 연결하는 함수
def connect_to_database(config):
    connection = mysql.connector.connect(
        host=config['host'],
        user=config['user'],
        password=config['password'],
        database=config['database']
    )
    return connection

# 모든 테이블의 이름을 가져오는 함수
def get_all_tables(connection):
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    cursor.close()
    return [table[0] for table in tables]

# 특정 테이블의 데이터를 csv 파일로 백업하는 함수
def backup_table_data(connection, table_name, output_dir):
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    
    # 테이블의 열 이름(헤더) 가져오기
    column_names = [i[0] for i in cursor.description]
    
    # 백업할 디렉토리가 없다면 생성
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # csv 파일로 저장
    backup_file = os.path.join(output_dir, f"{table_name}.csv")
    with open(backup_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(column_names)  # 열 이름을 csv 파일의 첫 줄로 저장
        writer.writerows(rows)  # 테이블의 데이터를 저장

    cursor.close()
    print(f"Table {table_name} backed up successfully.")

# 데이터베이스의 모든 테이블을 백업하는 함수
def backup_all_tables(config, output_dir):
    connection = connect_to_database(config)
    
    try:
        tables = get_all_tables(connection)
        # print(tables)
        # assert False
        for table in tables:
            backup_table_data(connection, table, output_dir)
        print("All tables have been backed up successfully.")
    finally:
        connection.close()
        
def backup_all_db_tables(backup_dir):
    config_file = 'db_config.json'  # 데이터베이스 정보를 담고 있는 JSON 파일 경로
    
    # 현재 날짜를 포함하는 백업 디렉토리 이름 생성
    current_date = datetime.now().strftime("%Y-%m-%d")  # 예: "2024-10-16"
    output_dir = os.path.join(backup_dir, current_date)  # 예: "./db_backups_2024-10-16"
    
    # JSON 파일에서 데이터베이스 설정 불러오기
    config = load_db_config(config_file)
    
    # 모든 테이블 백업
    backup_all_tables(config, output_dir)
    

# 사용 예시
if __name__ == "__main__":
    backup_all_db_tables('./db_backup')
