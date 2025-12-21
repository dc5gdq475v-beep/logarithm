import streamlit as st
import numpy as np
import pandas as pd
import math

st.title("📘 インタラクティブ常用対数表（log10）")

st.write("任意の範囲を指定して、常用対数 log10(x) を計算できます。")

# --- Sidebar inputs ---
st.sidebar.header("設定")
start = st.sidebar.number_input("開始値", value=1.0, step=0.1)
end = st.sidebar.number_input("終了値", value=10.0, step=0.1)
step = st.sidebar.number_input("ステップ", value=0.1, step=0.1)

if start <= 0:
    st.error("開始値は 0 より大きい必要があります。")
elif end <= start:
    st.error("終了値は開始値より大きくしてください。")
elif step <= 0:
    st.error("ステップは正の値にしてください。")
else:
    # --- Generate table ---
    x_values = np.arange(start, end + step, step)
    log_values = np.log10(x_values)

    df = pd.DataFrame({
        "x": x_values,
        "log10(x)": log_values
    })

    st.subheader("📋 常用対数表")
    st.dataframe(df, use_container_width=True)

    # --- Plot ---
    st.subheader("📈 グラフ表示")
    st.line_chart(df.set_index("x"))
