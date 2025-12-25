import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import font_manager

# Ricty Diminished Discord を読み込む
font_manager.fontManager.addfont("logarithm/fonts/RictyDiminishedDiscord-Regular.ttf")
plt.rcParams["font.family"] = "Ricty Diminished Discord"
matplotlib.use("Agg")

st.set_page_config(page_title="見てわかる対数", layout="wide")

st.title("🔍 見てわかる対数：桁と面積で理解する Log Visualizer")

# スライダー
x = st.slider("値 x を選んでください", min_value=0.1, max_value=10000.0, value=50.0, step=0.1)

log10_value = np.log10(x)

# レイアウト
col1, col2 = st.columns(2)

# ---------------------------------------------------------
# ① 桁の感覚（digit bands）
# ---------------------------------------------------------
with col1:
    fig1, ax1 = plt.subplots(figsize=(7, 5))

    # 桁の境界
    boundaries = [1, 10, 100, 1000, 10000]
    colors = ["#f0f8ff", "#e6f7ff", "#e8ffe6", "#fff5e6"]

    # 桁帯の描画
    for i in range(len(boundaries) - 1):
        ax1.axvspan(boundaries[i], boundaries[i+1], color=colors[i % len(colors)], alpha=0.5)
        ax1.text(
            (boundaries[i] + boundaries[i+1]) / 2,
            0.5,
            f"{i+1}桁",
            ha="center",
            va="center",
            fontsize=14,
            alpha=0.7,
            transform=ax1.get_xaxis_transform()
        )

    # x の位置
    ax1.axvline(x, color="red", linewidth=2)
    ax1.text(x, 0.1, f"x = {x}", rotation=90, color="red")

    ax1.set_xscale("log")
    ax1.set_xlabel("x（対数スケール）")
    ax1.set_title("📏 桁の感覚：log₁₀(x) は『桁の位置』を表す")
    ax1.grid(True)

    st.pyplot(fig1)

    st.markdown(f"""
    ### 📝 桁の意味
    **log₁₀({x}) = {log10_value:.3f}**

    これは  
    **「x が 10 の何乗に近いか（何桁か）」**  
    を表しています。

    - 1〜9 → 1桁  
    - 10〜99 → 2桁  
    - 100〜999 → 3桁  

    x の位置がどの桁帯にあるかが一目でわかります。
    """)

# ---------------------------------------------------------
# ② 面積で理解する log（積分の意味）
# ---------------------------------------------------------
with col2:
    fig2, ax2 = plt.subplots(figsize=(7, 5))

    T = np.linspace(1, x, 400)
    Y = 1 / T

    # 曲線
    ax2.plot(T, Y, color="blue", label="y = 1/t")

    # 面積（塗りつぶし）
    ax2.fill_between(T, Y, color="skyblue", alpha=0.4)

    # x の位置
    ax2.axvline(x, color="red", linestyle="--")
    ax2.text(x, 1/x, f"x = {x}", rotation=90, color="red")

    ax2.set_xlabel("t")
    ax2.set_ylabel("1/t")
    ax2.set_title("📐 面積で理解する log：log(x) = ∫₁ˣ 1/t dt")
    ax2.grid(True)

    st.pyplot(fig2)

    st.markdown(f"""
    ### 📝 面積としての対数
    **log({x}) = ∫₁^{x} 1/t dt = {np.log(x):.3f}**

    つまり  
    **1/t の曲線の下の面積が log(x)**  
    です。

    - x が大きくなるほど面積は増える  
    - でも 1/t が小さくなるので増え方はゆっくり  

    これが「対数はゆっくり増える」理由です。
    """)
