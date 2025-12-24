import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="見てわかる対数", layout="wide")

# 日本語フォント設定（環境に合わせて変更）
#plt.rcParams["font.family"] = "Noto Sans CJK JP"

st.title("🔍 見てわかる対数（Log Visualizer）")

# スライダー
a = st.slider("底 a を選んでください", min_value=2.0, max_value=10.0, value=2.0, step=0.1)
x = st.slider("値 x を選んでください", min_value=0.1, max_value=100.0, value=8.0, step=0.1)

# グラフ描画
fig, ax = plt.subplots(figsize=(6, 4))

X = np.linspace(0.1, 100, 400)
Y_exp = a ** (np.log(X) / np.log(a))  # = X
Y_log = np.log(X) / np.log(a)

ax.plot(X, Y_log, label=f"log_{a}(x)")
ax.set_xscale("log")
ax.set_xlabel("x")
ax.set_ylabel("log_a(x)")
ax.grid(True)
ax.legend()

st.pyplot(fig)

# 説明文
st.markdown(f"""
### 📝 対数の意味
**log_{a}({x}) = {np.log(x)/np.log(a):.3f}**  
これは「{a} を {np.log(x)/np.log(a):.3f} 回かけると {x} になる」という意味です。
""")
