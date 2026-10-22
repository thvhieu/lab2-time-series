# Quy trình làm việc

## File riêng, nhánh riêng

Làm trên notebook nội dung tương ứng trong `contributions/`; notebook tổng hợp dùng để tích hợp.
Không để nhiều người đồng thời sửa cùng một file notebook. Không chỉnh sửa CSV gốc.

```bash
git switch main
git pull --ff-only
git switch -c feature/adf
# Làm nội dung, chạy thử và viết nhận xét.
python scripts/check_notebooks.py --clear-outputs
python scripts/check_notebooks.py --require-clean
python scripts/check_data.py
git add contributions/02_adf_differencing.ipynb
git commit -m "feat: add ADF analysis"
git push -u origin feature/adf
```

Ví dụ trên dành cho nội dung ADF; đổi nhánh và file cho nội dung khác.
Sau đó mở PR vào `main`, mô tả phương pháp/kết quả và nhờ kiểm tra trước khi merge.
Notebook riêng chỉ có đề mục và TODO; phần import, đọc dữ liệu và xử lý đều cần tự viết.

## Phần nào làm song song?

```text
Dữ liệu + cùng ranh giới train/test
   ├── EDA --------------------------------------------┐
   └── ADF / sai phân (cả hai dataset)                  │
            └── ACF/PACF + cấu hình ứng viên            │
                   ├── ARIMA DS1 ── forecast/metrics ──┤
                   ├── ARIMA DS2 ──┐                   │
                   └── SARIMA DS2 ─┴── so sánh DS2 ────┤
                                                      └── tích hợp cuối
```

- EDA và ADF bắt đầu song song sau khi thống nhất dữ liệu; ADF không cần chờ nhận xét EDA.
- ACF/PACF có thể chuẩn bị code trước, nhưng kết luận p/q/P/Q cần chuỗi đã xử lý và d/D từ ADF.
- ARIMA và SARIMA chạy song song sau khi có các cấu hình tương ứng.
- Phần đánh giá viết hàm metrics, kiểm tra index và khung đồ thị trước; số liệu cuối cần forecast thật.
- So sánh Dataset 2 phải chờ cả ARIMA và SARIMA trên cùng train/test và thang đo.

## Hợp đồng dữ liệu

`src/lab2_data.py` cung cấp `load_datasets()` và `chronological_split()`.
Mọi notebook dùng `y1`, `y2`, `train1`, `test1`, `train2`, `test2`, tỷ lệ train 0.80 và chu kỳ 12.
Dataset 1: 163 train / 41 test; Dataset 2: 115 train / 29 test.
Không chọn tham số bằng test. Khi thay phép biến đổi, ghi rõ cách hoàn nguyên dự báo về thang gốc.

## Bàn giao giữa các phần

| Phần | Cần bàn giao |
|---|---|
| ADF/sai phân | Phép xử lý, d/D, kiểm định trước/sau và code tái tạo |
| ACF/PACF | Đồ thị, cấu hình ứng viên, lý do chọn p/q/P/Q |
| Mô hình | Code fit, cấu hình cuối, AIC/BIC, hội tụ/phần dư, cách tạo forecast |
| Forecast/đánh giá | Dự báo gắn ngày, metrics đúng thang đo, đồ thị và nhận xét |

Bàn giao bằng code và kết quả tái tạo được, không chỉ ảnh chụp hay biến đang tồn tại trong kernel.

## Tích hợp cuối

Chép các cell đã kiểm tra theo thứ tự vào notebook tổng hợp, thống nhất import/tên biến,
rồi Restart Kernel → Run All. Merge PR không tự ghép nội dung notebook.
Chỉ phần mô tả dữ liệu có output preview lưu sẵn; giữ nguyên tag `dataset-preview` cho các cell đó.
