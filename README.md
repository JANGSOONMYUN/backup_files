# Data and Database Backup System

## Overview

This project automates the backup of both database tables and important data files on a server. It performs periodic backups to ensure that critical data and databases are preserved safely. Additionally, it manages older backups by deleting them to free up storage space.

## Project Structure

- **backup_db.py**: Contains the function `backup_all_db_tables(db_dir)` to back up all tables in the database to the specified directory.
- **backup_data.py**: Contains the function `backup_data_dir(data_dir)` to back up important data files from a source directory to a backup location.
- **manage_data.py**: Contains the function `delete_old_data(dir_path)` that deletes old backup files from the specified directory.
- **run.py**: The main script (`run()`) that manages the sequence of operations: deleting old backups, backing up database tables, and backing up the data directory.

## Setup

1. Clone the repository to your server:

   ```bash
   git clone https://github.com/your-repository/data-backup-system.git
   cd data-backup-system
   ```

2. Install required dependencies (if any):

   ```bash
   pip install -r requirements.txt
   ```

3. Make sure the necessary backup directories exist:

   - For database backups: `/home/user/data_backup/db_backup/`
   - For data backups: `/home/user/data_backup/data_backup/`

   Adjust the paths in `run.py` if your directories are different.

4. Ensure you have permission to read from the database and data directories and to write to the backup locations.

## Usage

To execute the backup, simply run the script:

```bash
python run.py
```

The script will:

1. Delete old backups in the specified directories.
2. Back up all database tables to `/home/user/data_backup/db_backup/`.
3. Back up the data directory to `/home/user/data_backup/data_backup/`.

You can automate this process by scheduling it with tools like `cron`.

## Example Crontab Entry
```bash
crontab -e
```

- Run at 4:00 AM
```bash
0 4 * * * /bin/bash -c "source /home/user/anaconda3/bin/activate base && python /home/user/data_backup/run.py"
```