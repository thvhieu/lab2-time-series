import sys
sys.stdout.reconfigure(encoding="utf-8")   # in tiếng Việt an toàn trên console Windows
import matplotlib
matplotlib.use("Agg")   # chạy không cần cửa sổ đồ họa
import pandas as pd
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 30)

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "figures"
TABLE_DIR = ROOT / "tables"
sys.path.insert(0, str(ROOT))
from src.lab2_data import load_datasets, chronological_split, SEASON_LENGTH

# 1. Đọc và chia tập train/test theo đúng chuẩn 80/20 theo thời gian
raw1, raw2, y1, y2 = load_datasets()
train1, test1 = chronological_split(y1)
train2, test2 = chronological_split(y2)

print(f"Dataset 1 (a10)       : total={len(y1)}, train={len(train1)}, test={len(test1)}, {train1.index[0]:%Y-%m} -> {train1.index[-1]:%Y-%m}")
print(f"Dataset 2 (Passengers): total={len(y2)}, train={len(train2)}, test={len(test2)}, {train2.index[0]:%Y-%m} -> {train2.index[-1]:%Y-%m}")

# 2. Kiểm tra chất lượng dữ liệu (Data Quality Check)
def check_quality(raw_df, series, name, target_col, unit):
    return {
        "Dataset": name,
        "Cột mục tiêu": target_col,
        "Đơn vị": unit,
        "Tổng N": len(series),
        "Thời gian bắt đầu": f"{series.index[0]:%Y-%m}",
        "Thời gian kết thúc": f"{series.index[-1]:%Y-%m}",
        "N (Train)": len(series) - int(len(series) * 0.2),
        "N (Test)": int(len(series) * 0.2),
        "Thiếu (NaN)": int(series.isna().sum()),
        "Trùng lặp ngày": bool(raw_df.iloc[:, 0].duplicated().any()),
        "Chu kỳ liên tục (MS)": series.index.freqstr == "MS",
        "Tăng đơn điệu": bool(series.index.is_monotonic_increasing),
    }

quality_df = pd.DataFrame([
    check_quality(raw1, y1, "Dataset 1 (a10)", "value", "Triệu AUD (trợ giá thuốc)"),
    check_quality(raw2, y2, "Dataset 2 (AirPassengers)", "Passengers", "Nghìn hành khách quốc tế"),
])
print("\n--- BẢNG KIỂM TRA CHẤT LƯỢNG DỮ LIỆU ---")
print(quality_df.to_string(index=False))

# 3. Thống kê mô tả trên tập Train
desc_df = pd.DataFrame({
    "D1 a10 (Train)": train1.describe(),
    "D2 Passengers (Train)": train2.describe(),
})
print("\n--- THỐNG KÊ MÔ TẢ TRÊN TẬP TRAIN ---")
print(desc_df)

# 4. Phân tích chu kỳ mùa vụ theo từng tháng
monthly_avg = pd.DataFrame({
    "D1 Trung bình theo tháng": train1.groupby(train1.index.month).mean(),
    "D2 Trung bình theo tháng": train2.groupby(train2.index.month).mean(),
}, index=range(1, 13))
monthly_avg.index.name = "Tháng"
print("\n--- TRUNG BÌNH THEO TỪNG THÁNG TRÊN TẬP TRAIN ---")
print(monthly_avg.T)

# 5. Vẽ biểu đồ EDA trực quan hóa tập Train
fig, axes = plt.subplots(3, 2, figsize=(15, 12))

# Subplot 1: D1 Chuỗi Train gốc + Rolling Mean 12 tháng
axes[0, 0].plot(train1.index, train1.values, label="Train gốc (a10)", color="#1f77b4", lw=1.5)
axes[0, 0].plot(train1.index, train1.rolling(12).mean(), label="Rolling Mean (12 tháng)", color="#d62728", lw=2)
axes[0, 0].set_title("Dataset 1 (a10) — Xu hướng và chuỗi Train gốc")
axes[0, 0].set_ylabel("Triệu AUD")
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# Subplot 2: D2 Chuỗi Train gốc + Rolling Mean 12 tháng
axes[0, 1].plot(train2.index, train2.values, label="Train gốc (Passengers)", color="#2ca02c", lw=1.5)
axes[0, 1].plot(train2.index, train2.rolling(12).mean(), label="Rolling Mean (12 tháng)", color="#d62728", lw=2)
axes[0, 1].set_title("Dataset 2 (Passengers) — Xu hướng và chuỗi Train gốc")
axes[0, 1].set_ylabel("Nghìn hành khách")
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# Subplot 3: D1 Độ lệch chuẩn trượt (Rolling Std 12 tháng) thể hiện phương sai thay đổi
axes[1, 0].plot(train1.index, train1.rolling(12).std(), color="#ff7f0e", lw=1.8, label="Rolling Std (12 tháng)")
axes[1, 0].set_title("Dataset 1 (a10) — Độ lệch chuẩn trượt (Biên độ dao động tăng dần)")
axes[1, 0].set_ylabel("Std (Triệu AUD)")
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

# Subplot 4: D2 Độ lệch chuẩn trượt (Rolling Std 12 tháng)
axes[1, 1].plot(train2.index, train2.rolling(12).std(), color="#9467bd", lw=1.8, label="Rolling Std (12 tháng)")
axes[1, 1].set_title("Dataset 2 (Passengers) — Độ lệch chuẩn trượt (Phương sai thay đổi)")
axes[1, 1].set_ylabel("Std (Nghìn khách)")
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

# Subplot 5: D1 Phân bố mùa vụ theo tháng qua từng năm (Seasonal Month Plot)
for year, group in train1.groupby(train1.index.year):
    axes[2, 0].plot(group.index.month, group.values, marker="o", ms=3, alpha=0.5, label=str(year) if year in [1992, 1998, 2004] else None)
axes[2, 0].set_title("Dataset 1 (a10) — Mùa vụ: Đỉnh nhọn tháng 1, đáy sâu tháng 2")
axes[2, 0].set_xlabel("Tháng trong năm")
axes[2, 0].set_ylabel("Triệu AUD")
axes[2, 0].set_xticks(range(1, 13))
axes[2, 0].legend(title="Năm tiêu biểu")
axes[2, 0].grid(True, alpha=0.3)

# Subplot 6: D2 Phân bố mùa vụ theo tháng qua từng năm
for year, group in train2.groupby(train2.index.year):
    axes[2, 1].plot(group.index.month, group.values, marker="s", ms=3, alpha=0.5, label=str(year) if year in [1949, 1953, 1957] else None)
axes[2, 1].set_title("Dataset 2 (Passengers) — Mùa vụ: Đỉnh du lịch hè (T7–T8), đáy T11")
axes[2, 1].set_xlabel("Tháng trong năm")
axes[2, 1].set_ylabel("Nghìn khách")
axes[2, 1].set_xticks(range(1, 13))
axes[2, 1].legend(title="Năm tiêu biểu")
axes[2, 1].grid(True, alpha=0.3)

fig.tight_layout()
FIG_DIR.mkdir(exist_ok=True)
fig_path = FIG_DIR / "fig_01_eda.png"
fig.savefig(fig_path, dpi=120)
print(f"\nĐã lưu biểu đồ EDA vào: {fig_path}")

# 6. Bảng tổng hợp nhận xét EDA bàn giao cho các bước sau
eda_summary = pd.DataFrame([
    {
        "Dataset": "D1 a10",
        "Xu hướng (Trend)": "Tăng trưởng dài hạn mạnh mẽ (Upward trend)",
        "Mùa vụ (Seasonality)": "Chu kỳ 12 tháng: Đỉnh nhọn T1 (11.41M), đáy sâu T2 (6.41M)",
        "Phương sai (Variance)": "Tăng dần theo thời gian (Multiplicative)",
        "Đánh giá tính dừng": "Không dừng (Non-stationary)",
        "Khuyến nghị mô hình": "Cần sai phân d>=1 và sai phân mùa vụ D>=1 (m=12)",
    },
    {
        "Dataset": "D2 Passengers",
        "Xu hướng (Trend)": "Tăng trưởng tuyến tính ổn định",
        "Mùa vụ (Seasonality)": "Chu kỳ 12 tháng: Đỉnh hè T7 (304.6K), đáy đông T11 (192.4K)",
        "Phương sai (Variance)": "Biên độ dao động tăng tỷ lệ thuận với xu hướng",
        "Đánh giá tính dừng": "Không dừng (Non-stationary)",
        "Khuyến nghị mô hình": "Cần SARIMA với d=1, D=1, chu kỳ mùa vụ m=12",
    },
])
print("\n--- BẢNG ĐÁNH GIÁ ĐẶC TRƯNG EDA VÀ ĐỊNH HƯỚNG BÀN GIAO ---")
print(eda_summary.to_string(index=False))

TABLE_DIR.mkdir(exist_ok=True)
quality_df.to_csv(TABLE_DIR / "eda_quality_summary.csv", index=False)
eda_summary.to_csv(TABLE_DIR / "eda_characteristics_summary.csv", index=False)
print(f"Đã lưu các bảng tổng hợp vào: {TABLE_DIR}")
