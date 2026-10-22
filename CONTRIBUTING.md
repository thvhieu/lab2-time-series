# Quy trình đóng góp

## Phân nhánh theo phần

| Người | Nhánh đề xuất | File bàn giao trong `contributions/` | Reviewer |
|---|---|---|---|
| Leader | `feature/eda-integration` | Notebook tổng hợp, EDA và kết luận | TV6 |
| TV2 | `feature/adf-differencing` | `tv02_adf.ipynb` + `tv02_notes.md` | TV3 |
| TV3 | `feature/acf-pacf` | `tv03_acf_pacf.ipynb` + `tv03_notes.md` | TV2 |
| TV4 | `feature/arima-diagnostics` | `tv04_arima.ipynb` + `tv04_notes.md` | TV5 |
| TV5 | `feature/forecast-metrics` | `tv05_evaluation.ipynb` + `tv05_notes.md` | TV4 |
| TV6 | `feature/sarima` | `tv06_sarima.ipynb` + `tv06_notes.md` | Leader |

Đổi TV2...TV6 thành tên thật trong bảng phân công, giữ tên file ổn định.
Không có notebook thành viên tạo sẵn; mỗi người tạo đúng file phần mình khi bắt đầu.

## Một vòng làm việc

Ví dụ với TV2 (đã clone repo và thiết lập môi trường):

```bash
git switch main
git pull --ff-only
git switch -c feature/adf-differencing
# Làm bài, kiểm tra, clear output trước khi commit.
python scripts/check_notebooks.py --clear-outputs
python scripts/check_notebooks.py --require-clean
python scripts/check_data.py
git add contributions/tv02_adf.ipynb contributions/tv02_notes.md
git commit -m "feat: add ADF and differencing analysis"
git push -u origin feature/adf-differencing
```

Nếu nhánh đã tồn tại, dùng `git switch <ten-nhanh>` thay vì tạo lại.
Sau đó mở PR vào `main`, mô tả phần làm, phép kiểm tra và gắn reviewer theo bảng.
Reviewer kiểm tra trước; leader merge, tích hợp nội dung cần thiết rồi chạy notebook tổng hợp.

## Tránh xung đột notebook

- Chỉ leader chỉnh `Lab2_ADF_ARIMA_SARIMA.ipynb` trong giai đoạn tích hợp.
- Thành viên chỉ sửa file phần mình trong `contributions/` và file đã thống nhất từ trước.
- Không copy nguyên notebook tổng hợp thành phần nộp; chỉ giữ phần được giao và cell thiết lập cần thiết.
- Notebook thành viên nằm dưới `contributions/`: dùng `PROJECT_ROOT = Path.cwd().parent`
  nếu Jupyter chạy từ thư mục này, hoặc tự tìm thư mục chứa `data/a10.csv` từ thư mục hiện tại và các thư mục cha.
- Không sửa CSV nguồn, không commit `.venv`, cache hoặc thông tin máy cá nhân.
- Clear output chỉ xóa output cell; nhận xét trong markdown và code vẫn giữ nguyên.
- Hình/bảng chạy thử trong `figures/`, `tables/` được ignore. Nếu cần lưu một kết quả cuối,
  dùng `git add -f <file-ket-qua>` cho đúng file đã review, không thêm toàn bộ thư mục hàng loạt.

## Nội dung nhận xét bàn giao

Mỗi `tvXX_notes.md` cần có: mục tiêu, dữ liệu/phân chia train-test, phép xử lý,
tham số đã chọn và lý do, kết quả chính, câu trả lời theo đề, hạn chế và phụ thuộc cho người kế tiếp.
Ghi rõ tên biến hoặc tên file đầu ra. Không viết kết luận số liệu khi chưa chạy.

## Definition of Done

- [ ] Phần được giao chạy được từ kernel mới và có nhận xét tương ứng.
- [ ] Notebook hợp lệ; không có lỗi cú pháp; output được clear trước commit.
- [ ] Không chọn tham số bằng test; ARIMA/SARIMA so sánh trên cùng Dataset 2.
- [ ] Code giữ nguyên thứ tự thời gian, thang đo và mốc dự báo.
- [ ] Người phụ thuộc đã nhận đủ cấu hình, code và giải thích.
- [ ] PR nêu cách kiểm tra và có ít nhất một reviewer đồng ý.

## Trước khi chốt 26/10

Leader điền hết TODO, cập nhật tên nhóm, chạy **Restart Kernel → Run All**,
kiểm tra hội tụ/phần dư, đối chiếu các bảng metrics và xem lại toàn bộ đồ thị.
Clear output trước commit, giữ code/nhận xét đã hoàn thiện; lưu bảng/đồ thị cuối theo thỏa thuận của nhóm.
