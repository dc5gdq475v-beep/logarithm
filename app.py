import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.font_manager as fm

# フォント（必要に応じてファイル名を変更）
font_path = 'RictyDiminishedDiscord-Regular.ttf'
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()

matplotlib.use("Agg")

st.set_page_config(page_title="見てわかる対数（任意整数底）", layout="wide")
st.title("🔍 見てわかる対数：整数底で桁を可視化（重なり回避付き）")

# -------------------------
# ユーザー入力（整数底）
# -------------------------
x = st.slider("値 x を選んでください", min_value=1, max_value=100000, value=256, step=1)
b_int = st.slider("基数 b を選んでください（底）", min_value=2, max_value=36, value=10, step=1)

# 計算
logb_value = np.log(x) / np.log(b_int)
ln_value = np.log(x)

# 進数表記（整数部と小数部6桁まで）
def int_to_base(n: int, base: int) -> str:
    if n == 0:
        return "0"
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    neg = n < 0
    n = abs(n)
    digits = []
    while n > 0:
        digits.append(chars[n % base])
        n //= base
    if neg:
        digits.append('-')
    return ''.join(reversed(digits))

def frac_to_base(frac: float, base: int, max_digits: int = 6) -> str:
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    f = frac
    digits = []
    for _ in range(max_digits):
        f *= base
        d = int(f)
        digits.append(chars[d])
        f -= d
        if f == 0:
            break
    return ''.join(digits) if digits else "0"

x_int = int(np.floor(x))
x_frac = x - x_int
int_repr = int_to_base(x_int, b_int)
frac_repr = frac_to_base(x_frac, b_int, max_digits=6)
base_repr = f"{int_repr}.{frac_repr}_{b_int}" if x_frac > 0 else f"{int_repr}_{b_int}"

# -------------------------
# レイアウト
# -------------------------
col1, col2 = st.columns(2)

# ---------------------------------------------------------
# ① 桁の感覚（digit bands） with overlap avoidance + ticks as b^k
# ---------------------------------------------------------
with col1:
    fig1, ax1 = plt.subplots(figsize=(7, 5))
    ax1.set_facecolor('#fff8e7')
    ax1.set_yticks([])

    # 表示範囲の目安
    x_min = max(0.9, min(1.0, x / 10.0))
    x_max = max(10.0, x * 10.0)

    # b^k の境界を作る（十分先まで）
    boundaries = []
    k = 0
    while True:
        val = (b_int ** k)
        if val > x_max * 10:
            break
        boundaries.append(val)
        k += 1
    if len(boundaries) < 2:
        boundaries = [1.0, float(b_int)]

    # ラベル重なり回避のための閾値（log10 空間での最小距離）
    min_log_dist = 0.12
    last_label_logx = -1e9
    stagger_y = [0.55, 0.25]  # 交互に配置する y 座標（軸変換を使う）
    stagger_idx = 0

    for i in range(len(boundaries) - 1):
        left = boundaries[i]
        right = boundaries[i+1]
        mid = (left + right) / 2.0

        # 描画（桁帯は透明）
        ax1.axvspan(left, right, alpha=0.0)

        # 重なり判定（log10 空間）
        mid_log = np.log10(mid)
        if last_label_logx == -1e9 or (mid_log - last_label_logx) >= min_log_dist:
            y_pos = stagger_y[stagger_idx % 2]
            label = f"{i+1}桁"
            ax1.text(
                mid,
                y_pos,
                label,
                ha="center",
                va="center",
                fontsize=12,
                alpha=0.9,
                transform=ax1.get_xaxis_transform(),
                fontproperties=font_prop,
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.7, edgecolor="none")
            )
            last_label_logx = mid_log
            stagger_idx += 1
        else:
            # 間引く（必要なら小さなマークだけ残す）
            pass

    # x の位置
    ax1.axvline(x, color="red", linewidth=1)
    ax1.text(x, 0.05, f"x = {x}", rotation=80, color="red", transform=ax1.get_xaxis_transform())

    # 対数スケールと目盛（b^k 表記）
    ax1.set_xscale("log")
    ax1.set_xlim(left=boundaries[0]*0.9, right=boundaries[-1]*1.1)

    # ticks と labels を作る（間引き）
    ticks = boundaries
    # 自動間引き：最大表示数を 8 程度に制限
    max_ticks = 8
    step = max(1, int(np.ceil(len(ticks) / max_ticks)))
    display_ticks = ticks[::step]
    display_labels = [f"{b_int}^{i}" for i in range(0, len(ticks), step)]

    ax1.set_xticks(display_ticks)
    ax1.set_xticklabels(display_labels, fontsize=10, rotation=0, fontproperties=font_prop)
    ax1.tick_params(axis="x", which="major", pad=8)

    ax1.set_xlabel(f"x は {b_int} の何乗か", fontproperties=font_prop)
    ax1.set_title(f"log_{b_int}(x) = {logb_value:.6f}", fontproperties=font_prop)
    ax1.grid(True, which="both", ls="--", alpha=0.5)

    # --- グラフ内にプレーンテキスト注釈（左上） ---
    k_val = logb_value
    k_floor = int(np.floor(k_val))
    k_frac = k_val - k_floor
    r = (b_int ** k_frac)
    text_lines = [
        f"x ≈ {b_int}^{k_val:.4f}",
        f"{x} = {b_int}^{k_floor} × {r:.4f}",
        f"{b_int}進表記: {base_repr}"
    ]
    text_block = "\n".join(text_lines)
    ax1.text(
        0.02,
        0.98,
        text_block,
        transform=ax1.transAxes,
        fontsize=10,
        va="top",
        ha="left",
        fontproperties=font_prop,
        bbox=dict(facecolor="white", alpha=0.9, edgecolor="none", pad=6)
    )

    st.pyplot(fig1)

    st.markdown(f"""
    ### 📝 {b_int}進数における桁の意味
    **log₍{b_int}₎({x}) = {logb_value:.6f}**

    **{x} の {b_int} 進表記（）:**  
    **{base_repr}**
    """)

# ---------------------------------------------------------
# ② 面積で理解する log（積分の意味） -- log_b に対応
# ---------------------------------------------------------
with col2:
    fig2, ax2 = plt.subplots(figsize=(7, 5))

    if x >= 1:
        T = np.linspace(1, x, 400)
    else:
        T = np.linspace(x, 1, 400)
    Y = 1.0 / T

    ax2.plot(T, Y, color="blue", label="y = 1/t")
    ax2.fill_between(T, Y, color="skyblue", alpha=0.4)

    ax2.axvline(x, color="red", linestyle="--")
    ax2.text(x, 1.0 / max(x, 1e-12), f"x = {x}", rotation=80, color="red")

    ax2.set_xlabel("t", fontproperties=font_prop)
    ax2.set_ylabel("1/t", fontproperties=font_prop)
    ax2.set_title("面積で理解する log：log(x) = ∫₁ˣ 1/t dt", fontproperties=font_prop)
    ax2.grid(True, ls="--", alpha=0.5)

    st.pyplot(fig2)

    st.markdown(f"""
    ### 📝 面積としての対数（底 {b_int} に換算）
    - 自然対数（面積）: **∫₁^{x} 1/t dt = ln({x}) = {ln_value:.6f}**
    - 底 {b_int} の対数への換算: **log₍{b_int}₎({x}) = ln({x}) / ln({b_int}) = {logb_value:.6f}**
    """)

st.markdown("""
---
**調整可能な点(プログラム用)**
- `max_ticks`（現在は 8）を変えると x 軸目盛の密度を調整できます。  
- 注釈の行数やフォントサイズを減らせばさらにコンパクトにできます。  
- 目盛ラベルを LaTeX 風にしたい場合は `display_labels = [rf"${b_int}^{{{i}}}$" ...]` に変更してください（環境によって見え方が変わります）。
""")
