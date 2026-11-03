# Lab 2 | ADF, ARIMA và SARIMA

Repo thực hành và báo cáo tổng hợp phân tích chuỗi thời gian cho hai bộ dữ liệu thực tế (**Dataset 1 — a10** và **Dataset 2 — AirPassengers**). Toàn bộ 6 nhánh đóng góp của các thành viên đã được merge và tích hợp đầy đủ vào notebook báo cáo tổng.

## Phân công nhiệm vụ và trạng thái đóng góp

| Thành viên | GitHub | Nhánh / PR | Phần phụ trách | File đóng góp | Trạng thái |
|---|---|---|---|---|---|
| **Trương Hà Vũ Hiệu** (Leader) | `@thvhieu` | `feature/eda`, `main` | Bài 1 — EDA cả 2 dataset; rà soát & tích hợp báo cáo tổng | [`contributions/01_eda.ipynb`](contributions/01_eda.ipynb) | Hoàn thành |
| **Phan Khoa** | `@khoa-bbc` | `task1` | Bài 2–3 — Kiểm định ADF & sai phân ($d, D$) trên cả 2 dataset | [`contributions/02_adf_differencing.ipynb`](contributions/02_adf_differencing.ipynb) | Hoàn thành |
| **Minh Quyền** | `@mquyen-kkk` | `feature/acf-pacf` (PR #1) | Bài 4 — Phân tích ACF/PACF & đề xuất cấu hình $(p,d,q)(P,D,Q)_{12}$ | [`contributions/03_acf_pacf.ipynb`](contributions/03_acf_pacf.ipynb) | Hoàn thành |
| **Lê Ngọc Ánh** | `@lengocanh270706-maker` | `feature/arima` (PR #2) | Bài 5.1–5.3 — Mô hình ARIMA (Dataset 1 & Baseline Dataset 2), AIC/BIC, phần dư & Câu hỏi 1–5 | [`contributions/04_arima.ipynb`](contributions/04_arima.ipynb) | Hoàn thành |
| **Huy Hoàng** | `@huyhoang210` | `feature/forecast` | Bài 5.4–5.5 — Dự báo ngoài mẫu, đánh giá MAE/RMSE/MAPE, so sánh ARIMA–SARIMA & Câu hỏi 6–9 | [`contributions/05_forecast_evaluation.ipynb`](contributions/05_forecast_evaluation.ipynb) | Hoàn thành |
| **Trương Lâm Hưng** | `@lamhuwng` | `feature/sarima` (PR #3) | Phần nâng cao — Mô hình SARIMA trên Dataset 2, chẩn đoán phần dư, dự báo & đối chiếu với ARIMA | [`contributions/06_sarima.ipynb`](contributions/06_sarima.ipynb) | Hoàn thành |

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

- [Báo cáo tổng hợp (đã tích hợp toàn bộ bài làm)](Lab2_ADF_ARIMA_SARIMA.ipynb)
- [Phần 1 — EDA](contributions/01_eda.ipynb)
- [Phần 2 — ADF và sai phân](contributions/02_adf_differencing.ipynb)
- [Phần 3 — ACF/PACF](contributions/03_acf_pacf.ipynb)
- [Phần 4 — ARIMA và phần dư](contributions/04_arima.ipynb)
- [Phần 5 — Forecast và đánh giá](contributions/05_forecast_evaluation.ipynb)
- [Phần 6 — SARIMA nâng cao](contributions/06_sarima.ipynb)

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
