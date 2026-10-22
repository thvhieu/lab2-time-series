# Nguồn và mô tả dữ liệu

CSV được tải theo đúng hai URL trong đề ngày 22/10/2026; byte nguồn được giữ nguyên.
`manifest.json` ghi URL, SHA256, số dòng và tên cột để kiểm tra toàn vẹn.

## Dataset 1 — a10
- [CSV](https://raw.githubusercontent.com/selva86/datasets/master/a10.csv): `date`, `value`; 204 tháng, 07/1991–06/2008.
- Chi tiêu trợ giá thuốc A10 tại Australia, đơn vị triệu đô la.
- [Mô tả chính thức fpp2](https://pkg.robjhyndman.com/fpp2/reference/a10.html).
- PDF ghi Retail Sales (US), nhưng URL trong PDF thực tế trỏ tới a10. Repo sử dụng đúng URL và phân biệt mô tả nghiệp vụ này.

## Dataset 2 — AirPassengers
- [CSV](https://raw.githubusercontent.com/jbrownlee/Datasets/master/airline-passengers.csv): `Month`, `Passengers`; 144 tháng, 01/1949–12/1960.
- Tổng hành khách hàng không quốc tế theo tháng, đơn vị nghìn hành khách.
- [Mô tả chính thức R datasets](https://stat.ethz.ch/R-manual/R-devel/library/datasets/html/AirPassengers.html).
