import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.font_manager as fm

# Ricty Diminished Discord を読み込む（フォントファイルが同ディレクトリにある前提）
font_path = 'RictyDiminishedDiscord-Regular.ttf'
font_prop = fm.FontProperties(fname=font_path)
# matplotlib のデフォルトフォント設定（環境によっては動作しない場合あり）
plt.rcParams['font.family'] = font_prop.get_name()

matplotlib.use("Agg")

st.set_page_config(page_title="見てわかる対数（任意底）", layout="wide")
st.title("🔍 見てわかる対数：底を変えて見る Log Visualizer")

# -------------------------
# ユーザー入力
# -------------------------
x = st.slider("値 x を選んでください", min_value=0.1, max_value=10000.0, value=50.0, step=0.1)

# 底 b を連続的に変えられるスライダー（1 より大きい実数）
b = st.slider("底 b を選んでください（連続値）", min_value=1.1, max_value=16.0, value=10.0, step=0.1)

# 表示に使う整数基数（b を丸めたもの）を明示
b_int = max(2, int(round(b)))
st.caption(f"※ 表示用の進数表記は整数に丸めた基数 b_int = {b_int} を使用します（スライダーは実数）。")

# 計算
logb_value = np.log(x) / np.log(b)   # log_b(x)
ln_value = np.log(x)                 # natural log (積分の面積)

# -------------------------
# ヘルパー: 整数を基数変換
# -------------------------
def int_to_base(n: int, base: int) -> str:
    if n == 0:
        return "0"
    digits = []
    neg = n < 0
    n = abs(n)
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    while n > 0:
        digits.append(chars[n % base])
        n //= base
    if neg:
        digits.append('-')
    return ''.join(reversed(digits))

def frac_to_base(frac: float, base: int, max_digits: int = 6) -> str:
    # frac in [0,1)
    digits = []
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    f = frac
    for _ in range(max_digits):
        f *= base
        d = int(f)
        digits.append(chars[d])
        f -= d
        if f == 0:
            break
    return ''.join(digits) if digits else "0"

# 表示用の b 進表記（整数部と小数部）
x_int = int(np.floor(x))
x_frac = x - x_int
int_repr = int_to_base(x_int, b_int)
frac_repr = frac_to_base(x_frac, b_int, max_digits=6)
if x_frac > 0:
    base_repr = f"{int_repr}.{frac_repr}_{b_int}"
else:
    base_repr = f"{int_repr}_{b_int}"

# -------------------------
# レイアウト：左右カラム
# -------------------------
col1, col2 = st.columns(2)

# ---------------------------------------------------------
# ① 桁の感覚（digit bands） -- 底 b に対応
# ---------------------------------------------------------
with col1:
    fig1, ax1 = plt.subplots(figsize=(7, 5))
    ax1.set_facecolor('#fff8e7')
    ax1.set_yticks([])

    # 境界を b^0=1 から作る（b は実数なので float のべき乗）
    max_display = max(10, x * 10)
    boundaries = [1.0]
    i = 1
    while True:
        val = (b ** i)
        if val > max_display * 10:  # 十分先まで作る
            break
        boundaries.append(val)
        i += 1

    # 桁帯の描画（ラベルは整数基数 b_int を表示）
    for i in range(len(boundaries) - 1):
        left = boundaries[i]
        right = boundaries[i+1]
        ax1.axvspan(left, right, alpha=0.0)
        ax1.text(
            (left + right) / 2,
            0.5,
            f"{i+1}桁（{b_int}進）",
            ha="center",
            va="center",
            fontsize=14,
            alpha=0.8,
            transform=ax1.get_xaxis_transform(),
            fontproperties=font_prop
        )

    # x の位置
    ax1.axvline(x, color="red", linewidth=1)
    ax1.text(x, 0.1, f"x = {x}", rotation=80, color="red")

    ax1.set_xscale("log")
    ax1.set_xlabel(f"x は {b:.2f} の何乗か（表示は {b_int} 進の桁）", fontproperties=font_prop)
    ax1.set_title(f"log_{b:.2f}(x) ≈ {logb_value:.3f}", fontproperties=font_prop)
    ax1.grid(True)

    st.pyplot(fig1)

    st.markdown(f"""
    ### 📝 {b:.2f} を底とした桁の意味（表示は {b_int} 進）
    **log₍{b:.2f}₎({x}) = {logb_value:.6f}**

    **{x} の {b_int} 進表記（整数部＋小数部6桁まで）:**  
    **{base_repr}**
    """)

# ---------------------------------------------------------
# ② 面積で理解する log（積分の意味） -- log_b に対応
# ---------------------------------------------------------
with col2:
    fig2, ax2 = plt.subplots(figsize=(7, 5))

    # 積分区間は [1, x]（x が 1 未満のときは逆向きに扱う）
    if x >= 1:
        T = np.linspace(1, x, 400)
    else:
        # x < 1 の場合は 400 点で 1 -> x（降順）を作る
        T = np.linspace(x, 1, 400)

    Y = 1.0 / T

    # 曲線
    ax2.plot(T, Y, color="blue", label="y = 1/t")

    # 面積（塗りつぶし）
    ax2.fill_between(T, Y, color="skyblue", alpha=0.4)

    # x の位置
    ax2.axvline(x, color="red", linestyle="--")
    ax2.text(x, 1.0 / max(x, 1e-12), f"x = {x}", rotation=80, color="red")

    ax2.set_xlabel("t", fontproperties=font_prop)
    ax2.set_ylabel("1/t", fontproperties=font_prop)
    ax2.set_title("面積で理解する log：log(x) = ∫₁ˣ 1/t dt", fontproperties=font_prop)
    ax2.grid(True)

    st.pyplot(fig2)

    st.markdown(f"""
    ### 📝 面積としての対数（底 {b:.2f} に換算）
    - 自然対数（面積）: **∫₁^{x} 1/t dt = ln({x}) = {ln_value:.6f}**
    - 底 {b:.2f} の対数への換算: **log₍{b:.2f}₎({x}) = ln({x}) / ln({b:.2f}) = {logb_value:.6f}**

    つまり、曲線 \(1/t\) の下の面積（ln）はそのまま計算し、**その値を \(\ln b\) で割る**と底 \(b\) の対数になります。
    """)

# -------------------------
# 補足（任意）
# -------------------------
st.markdown("""
---
**補足メモ**
- スライダーで底 b を連続的に動かすと、`log_b(x)` の値は滑らかに変化しますが、**進数表記は整数基数に丸めて表示**しています（非整数基数での「桁表記」は一般に定義が複雑なため）。
- もし進数表記も厳密に「整数のみ」にしたい場合は、`b` を整数スライダーに変更できます。希望があればそのバージョンも用意します。
""")
