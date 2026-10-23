import sys
sys.stdout.reconfigure(encoding="utf-8")   # in tiếng Việt an toàn trên console Windows
import matplotlib
matplotlib.use("Agg")   # không cần cửa sổ đồ họa
import pandas as pd
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 30)

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller

ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "figures"
sys.path.insert(0, str(ROOT))
from src.lab2_data import load_datasets, chronological_split, SEASON_LENGTH

_, _, y1, y2 = load_datasets()
train1, test1 = chronological_split(y1)   # test chỉ để kiểm tra kích thước, không dùng chọn d/D
train2, test2 = chronological_split(y2)
print(f'Dataset 1 (a10)       : train={len(train1)}, test={len(test1)}, {train1.index[0]:%Y-%m} -> {train1.index[-1]:%Y-%m}')
print(f'Dataset 2 (Passengers): train={len(train2)}, test={len(test2)}, {train2.index[0]:%Y-%m} -> {train2.index[-1]:%Y-%m}')

ALPHA = 0.05


def adf_row(series, name, regression='c'):
    """ADF với autolag='AIC' (maxlag mặc định của statsmodels), trả về một dòng bảng kết quả."""
    s = series.dropna()
    stat, p, usedlag, nobs, crit, _ = adfuller(s, regression=regression, autolag='AIC', result_object=False)
    return {
        'Chuỗi': name, 'n': int(nobs) + usedlag + 1, 'regression': regression,
        'ADF stat': round(stat, 4), 'p-value': round(p, 4), 'lag (AIC)': usedlag,
        'crit 1%': round(crit['1%'], 3), 'crit 5%': round(crit['5%'], 3),
        'Kết luận (α=0.05)': 'Dừng (bác bỏ H0)' if p < ALPHA else 'Chưa dừng (không bác bỏ H0)',
    }


adf_orig = pd.DataFrame([
    adf_row(train1, 'D1 a10 - gốc'),
    adf_row(train2, 'D2 Passengers - gốc'),
])
print(
adf_orig
)


def diff1(s):
    return s.diff(1).dropna()


def diff_season(s, m=SEASON_LENGTH):
    return s.diff(m).dropna()


def diff_both(s, m=SEASON_LENGTH):
    return s.diff(1).diff(m).dropna()      # (1-B)(1-B^12) y_t; thứ tự giao hoán nên không ảnh hưởng kết quả


# Dataset 1: sai phân bậc 1 theo đề; thêm sai phân mùa vụ để đối chiếu (a10 có mùa vụ rất rõ)
t1 = {
    'D1 d=1': diff1(train1),
    'D1 D=1 (m=12)': diff_season(train1),
    'D1 d=1, D=1': diff_both(train1),
}
# Dataset 2: sai phân thường, mùa vụ, và cả hai
t2 = {
    'D2 d=1': diff1(train2),
    'D2 D=1 (m=12)': diff_season(train2),
    'D2 d=1, D=1': diff_both(train2),
}
transformed = {**t1, **t2}

adf_diff = pd.DataFrame([adf_row(s, n) for n, s in transformed.items()])
print(adf_diff)

# Số điểm mất do sai phân (NaN bị loại bằng dropna, index giữ nguyên theo thời gian)
loss = pd.DataFrame({
    'n gốc': [len(train1)] * 3 + [len(train2)] * 3,
    'n sau xử lý': [len(s) for s in transformed.values()],
    'bắt đầu từ': [f'{s.index[0]:%Y-%m}' for s in transformed.values()],
    'std': [round(s.std(), 3) for s in transformed.values()],   # std tăng khi sai phân thêm => dấu hiệu sai phân thừa
}, index=transformed.keys())
print(loss)

# Độ nhạy của kết luận ADF (p-value) theo cách chọn lag và thành phần tất định
def adf_p(s, **kw):
    return round(adfuller(s.dropna(), result_object=False, **kw)[1], 3)


all_series = {'D1 gốc': train1, 'D2 gốc': train2, **transformed}
adf_sens = pd.DataFrame({
    'AIC (mặc định)': {n: adf_p(s, autolag='AIC') for n, s in all_series.items()},
    'BIC': {n: adf_p(s, autolag='BIC') for n, s in all_series.items()},
    'AIC, maxlag=24': {n: adf_p(s, autolag='AIC', maxlag=24) for n, s in all_series.items()},
    "AIC, regression='ct'": {n: adf_p(s, autolag='AIC', regression='ct') for n, s in all_series.items()},
})
print(adf_sens)

fig, axes = plt.subplots(4, 2, figsize=(14, 12))
for col, (orig, group, title) in enumerate([(train1, t1, 'Dataset 1 (a10)'), (train2, t2, 'Dataset 2 (Passengers)')]):
    axes[0, col].plot(orig); axes[0, col].set_title(f'{title} - train gốc')
    for row, (name, s) in enumerate(group.items(), start=1):
        axes[row, col].plot(s); axes[row, col].axhline(0, color='grey', lw=0.8, ls='--')
        axes[row, col].set_title(name)
fig.tight_layout()
FIG_DIR.mkdir(exist_ok=True)
fig.savefig(FIG_DIR / 'fig_02_differencing.png', dpi=120)
print('Đã lưu hình:', FIG_DIR / 'fig_02_differencing.png')


# Kết luận d/D dựa trên bảng ADF ở trên (chỉ dùng train). Điền sau khi xem kết quả.
FINAL = {
    'D1': {'d': 1, 'D': 1, 'm': SEASON_LENGTH},
    'D2': {'d': 1, 'D': 1, 'm': SEASON_LENGTH},
}


def make_stationary(series, d, D, m=SEASON_LENGTH):
    """Tái tạo chuỗi đã xử lý: sai phân thường d lần rồi sai phân mùa vụ D lần (lag m), bỏ NaN đầu chuỗi."""
    out = series.copy()
    for _ in range(d):
        out = out.diff(1)
    for _ in range(D):
        out = out.diff(m)
    return out.dropna()


stat1 = make_stationary(train1, FINAL['D1']['d'], FINAL['D1']['D'])
stat2 = make_stationary(train2, FINAL['D2']['d'], FINAL['D2']['D'])

# Kiểm tra tái tạo khớp với phép biến đổi ở mục 2
assert stat1.equals(transformed['D1 d=1, D=1'])
assert stat2.equals(transformed['D2 d=1, D=1'])

summary = pd.DataFrame([
    {'Dataset': 'D1 a10', **FINAL['D1'], 'n': len(stat1), 'index': f'{stat1.index[0]:%Y-%m} -> {stat1.index[-1]:%Y-%m}',
     'ADF p-value': adf_row(stat1, 'D1')['p-value']},
    {'Dataset': 'D2 Passengers', **FINAL['D2'], 'n': len(stat2), 'index': f'{stat2.index[0]:%Y-%m} -> {stat2.index[-1]:%Y-%m}',
     'ADF p-value': adf_row(stat2, 'D2')['p-value']},
])
print(summary)

# Lưu chuỗi đã xử lý (có index thời gian) để phần ACF/PACF đọc lại; tables/ được Git bỏ qua
out_dir = ROOT / 'tables'
out_dir.mkdir(exist_ok=True)
stat1.rename('stationary_d1').to_csv(out_dir / 'stationary_dataset1_train.csv', index_label='date')
stat2.rename('stationary_d2').to_csv(out_dir / 'stationary_dataset2_train.csv', index_label='date')
pd.concat([adf_orig, adf_diff]).to_csv(out_dir / 'adf_results_02.csv', index=False)
print('Đã lưu vào', out_dir)
