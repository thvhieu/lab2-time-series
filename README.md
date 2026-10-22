# Lab 2 | Kiểm định ADF và mô hình ARIMA / SARIMA

**Nhóm:** 6 thành viên · **Hạn hoàn tất nội bộ:** 26/10/2026 · **Trạng thái:** notebook khung

Repo làm việc chung cho bài thực hành phân tích chuỗi thời gian: khám phá dữ liệu,
kiểm định tính dừng, sai phân, ACF/PACF, mô hình ARIMA và phần nâng cao SARIMA.
Nhận xét và lựa chọn mô hình được để dưới dạng `TODO` để nhóm hoàn thiện bằng kết quả thực chạy.

## Truy cập nhanh

- [Notebook tổng hợp](Lab2_ADF_ARIMA_SARIMA.ipynb)
- [Phân công và tiến độ](PHAN_CONG.md)
- [Quy trình đóng góp](CONTRIBUTING.md)
- [Nguồn dữ liệu](data/SOURCES.md)
- [Đề bài](resources/de_bai_lab2.pdf)

## Cấu trúc

```text
Lab2/
├── Lab2_ADF_ARIMA_SARIMA.ipynb   # Notebook tổng hợp do leader tích hợp
├── PHAN_CONG.md                 # Chủ nhiệm từng phần, đầu ra và deadline
├── CONTRIBUTING.md              # Nhánh, PR, quy tắc bàn giao
├── requirements.txt            # Môi trường Python
├── data/                       # CSV gốc và manifest kiểm tra toàn vẹn
├── resources/                  # Đề bài gốc
├── contributions/              # Thành viên nộp phần riêng, tránh sửa chung notebook
├── figures/                    # Hình sinh ra khi chạy, không commit mặc định
├── tables/                     # Bảng sinh ra khi chạy, không commit mặc định
├── scripts/                    # Kiểm tra notebook và dữ liệu
└── .github/                    # CI và mẫu pull request
```

## 1. Thiết lập môi trường

Sử dụng **Python 3.12**. Sau khi clone, mở terminal tại thư mục gốc repo.

### Windows / PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m jupyter lab
```

### macOS / Linux

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m jupyter lab
```

Trong VS Code: mở repo, chọn interpreter trong `.venv`, rồi chọn đúng kernel cho notebook.
CSV đã được lưu trong repo; không cần tải lại dữ liệu lúc chạy notebook.

## 2. Chạy notebook

1. Mở notebook tổng hợp, điền tên nhóm ở đầu bài.
2. Chạy từ trên xuống để đọc dữ liệu, EDA, ADF và ACF/PACF.
3. Điền tham số ở ô **CẤU HÌNH NHÓM** dựa trên kết quả trên train.
4. Đổi `RUN_MODELS = True` sau khi đã điền đủ cấu hình ARIMA và SARIMA.
5. **Restart Kernel → Run All**, kiểm tra hội tụ, đồ thị và số liệu.
6. Viết nhận xét trong các ô `TODO`; đối chiếu checklist cuối notebook.

`RUN_MODELS = False` là trạng thái mặc định của bản khung, không phải lỗi.
Các cấu hình ví dụ trong comment không phải kết luận mô hình của nhóm.

## 3. Nguyên tắc phân tích

- Chia train/test theo thời gian theo tỷ lệ 80/20, không shuffle.
- Chọn tham số và xử lý dữ liệu từ train; chỉ sử dụng test cho đánh giá cuối.
- ADF và ACF/PACF được thực hiện trên train tương ứng trước/sau sai phân.
- Fit ARIMA/SARIMA trên chuỗi train gốc với `d`/`D` tương ứng, tránh sai phân hai lần.
- Dataset 1 cần MAE, RMSE, MAPE; Dataset 2 cần MAE/RMSE và so sánh trên cùng test.
- Xác nhận tên nghiệp vụ, đơn vị Dataset 1 theo nguồn trước khi viết báo cáo.

## 4. Làm việc nhóm qua Git

**Không để 6 người cùng sửa notebook tổng hợp.** Mỗi người làm phần riêng trong
`contributions/`, gửi pull request; leader tích hợp vào notebook tổng hợp.
Nhánh, phân công review và định nghĩa hoàn thành nằm trong [CONTRIBUTING.md](CONTRIBUTING.md).

Repo chính: [thvhieu/lab2-time-series](https://github.com/thvhieu/lab2-time-series).
Thành viên clone repo này, không cần tạo repository riêng:

```bash
git clone https://github.com/thvhieu/lab2-time-series.git
cd lab2-time-series
```

Sau đó thiết lập môi trường theo mục 1 và làm việc trên nhánh phần mình theo
[CONTRIBUTING.md](CONTRIBUTING.md). Nhánh tích hợp chung là `main`.

## 5. Kiểm tra trước khi gửi PR

Chạy bằng Python trong `.venv` (trên Windows dùng `.\.venv\Scripts\python.exe`):

```bash
python scripts/check_notebooks.py --require-clean
python scripts/check_data.py
```

Để xóa output đã chạy trước khi commit:

```bash
python scripts/check_notebooks.py --clear-outputs
```

CI GitHub Actions chạy kiểm tra schema/cú pháp notebook, output sạch và hash CSV khi có push/PR.
CI này không thay thế kiểm tra **Restart Kernel → Run All** và đánh giá thống kê của nhóm.
Nếu dùng GitLab, chạy hai lệnh kiểm tra trên local; workflow trong `.github/` dành cho GitHub.

## Mốc bàn giao

| Mốc | Kết quả yêu cầu |
|---|---|
| 23/10, 20:00 | EDA, ADF, ACF/PACF và tham số ứng viên sẵn sàng |
| 24/10, 20:00 | Tất cả thành viên gửi PR có code chạy được và nhận xét |
| 25/10 | Review chéo, leader tích hợp và chạy lại |
| 26/10 | Chốt notebook, bảng/đồ thị cuối và nội dung báo cáo |

Các mốc trên là lịch nội bộ đề xuất; nhóm xác nhận giờ chốt cụ thể.
