# Lấy thông tin các doanh nghiệp tại Việt Nam

https://thongtindoanhnghiep.co/rest-api
## FILE APP
- app_v1.py: chạy ok
- app.py: chạy 5 thread một lúc

## RUN
```cmd
# Nếu ở trên server - chạy ngầm
bash start_script.sh

# Nếu ở client
python app.py
```

## FILE .sh
```sh
source /home/thanh/zrrm/zrrm_venv/bin/activate
cd /home/thanh/craw-info-vn-company
python3 app_v2_2thread.py >> log_file.log 2>&1 &
```