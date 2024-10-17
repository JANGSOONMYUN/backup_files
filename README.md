# scheduler crontab
```
crontab -e
```

- Run at 4:00 AM
```
0 4 * * * /bin/bash -c "source /home/user/anaconda3/bin/activate base && python /home/user/data_backup/run.py"
```