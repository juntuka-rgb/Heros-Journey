import streamlit as st
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# --- API設定 ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API KEY NOT FOUND")
    st.stop()

st.title("🧪 英雄の旅メーカー")
st.caption("〜 納得いくまで練り上げ、ビジュアルへ繋げる 〜")

# --- セッション状態の初期化 ---
if "story_content" not in st.session_state:
    st.session_state.story_content = ""
if "image_prompts" not in st.session_state:
    st.session_state.image_prompts = ""

# --- 1. 入力設定 ---
with st.expander("📝 1. 物語の種とトーンを設定", expanded=True):
    default_text = "むかしむかし、あるところにお祖父さんとお婆さんがいました。..." # 略（実際は前回の桃太郎の文章を入れてください）
    theme = st.text_area("ベースとなる話:", value=default_text, height=150)
    tone = st.selectbox("トーン:", ["普通", "少年漫画風", "SF風", "ファンタジー風", "ハードボイルド風", "ホラー風"])

# --- 2. 物語生成・修正セクション ---
st.write("### 📜 2. 物語の構築")
col1, col2 = st.columns(2)

with col1:
    if st.button("🚀 新規物語を生成"):
        with st.spinner("生成中..."):
            model = genai.GenerativeModel("gemini-2.0-flash")
            prompt = f"「{theme}」をベースに、英雄の旅（12ステップ）の構成で詳細な物語を書いて。トーン：{tone}"
            response = model.generate_content(prompt)
            st.session_state.story_content = response.text

with col2:
    update_instruction = st.text_input("修正指示（例：第3章をもっと悲劇的にして）")
    if st.button("🔄 物語を修正する"):
        if st.session_state.story_content:
            with st.spinner("修正中..."):
                model = genai.GenerativeModel("gemini-2.0-flash")
                refine_prompt = f"現在の物語：\n{st.session_state.story_content}\n\n指示：{update_instruction}\n上記指示に従って物語を書き直して。"
                response = model.generate_content(refine_prompt)
                st.session_state.story_content = response.text
        else:
            st.warning("先に物語を生成してください。")

# 物語の表示と編集
if st.session_state.story_content:
    st.session_state.story_content = st.text_area("物語の内容（直接編集も可能）:", value=st.session_state.story_content, height=300)
    
    st.download_button("📥 物語をテキスト保存", st.session_state.story_content, "story.txt")

    st.divider()

    # --- 3. 画像プロンプト生成セクション ---
    st.write("### 🖼️ 3. 画像生成用プロンプト")
    if st.button("🎨 画像プロンプトを生成（物語確定後）"):
        with st.spinner("プロンプト作成中..."):
            model = genai.GenerativeModel("gemini-2.0-flash")
            img_prompt_req = f"以下の物語の各シーンに合う、画像生成AI用の英語プロンプトを12個作成して。\n\n{st.session_state.story_content}"
            response = model.generate_content(img_prompt_req)
            st.session_state.image_prompts = response.text

    if st.session_state.image_prompts:
        st.session_state.image_prompts = st.text_area("画像プロンプト:", value=st.session_state.image_prompts, height=200)
        st.download_button("📥 プロンプトを保存", st.session_state.image_prompts, "image_prompts.txt")

st.divider()
st.info("※このアプリはユーザーネーム「ジュンツカ」の提供で動作しています。")
