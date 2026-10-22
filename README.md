# Lab 2 | ADF, ARIMA và SARIMA

Notebook khung để thực hành phân tích chuỗi thời gian. Phần đầu đã có **mô tả dataset,
bảng xem trước và đồ thị dữ liệu thật**; các phần bài làm chỉ chứa `TODO`, chưa có lời giải.

## Bắt đầu

```bash
git clone https://github.com/thvhieu/lab2-time-series.git
cd lab2-time-series
python -m venv .venv
```

Windows / PowerShell:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m jupyter lab
```

macOS / Linux:

```bash
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m jupyter lab
```

Trong VS Code, chọn interpreter và kernel trong `.venv`. CSV đã có sẵn trong repo.

## Notebook

- [Notebook tổng hợp và xem trước dataset](Lab2_ADF_ARIMA_SARIMA.ipynb)
- [EDA](contributions/01_eda.ipynb)
- [ADF và sai phân](contributions/02_adf_differencing.ipynb)
- [ACF/PACF](contributions/03_acf_pacf.ipynb)
- [ARIMA và phần dư](contributions/04_arima.ipynb)
- [Forecast và đánh giá](contributions/05_forecast_evaluation.ipynb)
- [SARIMA](contributions/06_sarima.ipynb)

Notebook riêng chỉ có đề mục và TODO, chưa điền import hoặc code đọc CSV.
Chỉ phần mô tả/xem trước dữ liệu trong notebook tổng hợp được thực hiện sẵn; các phần phân tích cần tự hoàn thiện.
Không có bảng phân công hoặc tên người phụ trách trong notebook.

## Dữ liệu và cấu trúc

- `data/`: hai CSV gốc, [mô tả nguồn](data/SOURCES.md) và manifest hash.
- `src/lab2_data.py`: đọc dữ liệu và chia 80/20 theo thời gian thống nhất.
- `contributions/`: notebook riêng theo nội dung.
- `resources/de_bai_lab2.pdf`: đề bài gốc.
- `figures/`, `tables/`: đầu ra chạy local, được Git bỏ qua mặc định.
- `scripts/`, `.github/`: công cụ kiểm tra và CI.

Lưu ý: đường dẫn Dataset 1 trong PDF là a10, dù phần mô tả trong PDF ghi Retail Sales.
Repo giữ đúng CSV theo URL và đối chiếu mô tả với nguồn chính thức trong notebook.

## Làm việc và tích hợp

Dùng file riêng và nhánh riêng; gửi pull request rồi tích hợp các cell vào notebook tổng hợp.
Xem [CONTRIBUTING.md](CONTRIBUTING.md) để biết quy trình và phụ thuộc giữa các phần.
Merge PR đưa file vào repo, không tự ghép nội dung các notebook.

## Kiểm tra

Chạy bằng Python đã cài thư viện trong `.venv`:

```bash
python scripts/check_notebooks.py --require-clean
python scripts/check_data.py
```

Output có tag `dataset-preview` trong notebook tổng hợp được giữ để GitHub hiển thị bảng/hình.
Output bài làm thông thường có thể xóa trước commit bằng:

```bash
python scripts/check_notebooks.py --clear-outputs
```

Lệnh này bảo toàn phần preview; thêm `--clear-previews` nếu chủ động muốn xóa cả preview.
CI kiểm tra cấu trúc/cú pháp, output lỗi và hash dữ liệu; không thay thế đánh giá thống kê.
