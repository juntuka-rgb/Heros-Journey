import streamlit as st
import google.generativeai as genai

# アプリのタイトルと説明
st.set_page_config(page_title="JUNTSUKA QUEST Generator", page_icon="🧪")
st.title("🧪 JUNTSUKA QUEST：英雄の旅メーカー")
st.write("あなたのアイデアを、AIが12ステップの物語と画像プロンプトに変換します。")

# サイドバーでAPIキーを設定（公開時はここを隠す設定も可能）
with st.sidebar:
    api_key = st.text_input("Gemini API Keyを入力してください", type="password")
    st.info("APIキーは [Google AI Studio](https://aistudio.google.com/app/apikey) で取得できます。")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')

    # --- 物語生成セクション ---
    st.header("1. 物語の生成")
    user_input = st.text_area("元となる台本やアイデア:", placeholder="例：還暦のサイクリストがケミカルXを作って旅に出る...", height=150)
    tone = st.selectbox("物語のトーン:", ["標準", "熱血・少年漫画風", "エモい（感情的）"])

    if st.button("🚀 12ステップ物語を生成"):
        with st.spinner("AIが構成を考えています..."):
            p = f"英雄の旅（12ステップ）に構成してください。トーン:{tone}。内容:{user_input}"
            response = model.generate_content(p)
            st.session_state['story'] = response.text
            st.success("完成しました！")

    if 'story' in st.session_state:
        st.text_area("生成された物語:", st.session_state['story'], height=300)

        # --- 画像プロンプト生成セクション ---
        st.divider()
        st.header("2. 画像プロンプトの作成")
        style = st.selectbox("画風を選択:", ["Japanese Anime Style", "Cinematic Realistic Style", "Dreamy Watercolor Style"])
        
        if st.button("🎨 プロンプトを一括生成"):
            with st.spinner("プロンプトを作成中..."):
                p = f"以下の物語の各ステップに対し、画像生成AI用プロンプト（英語）を12個作成。画風:{style}。必ず'Glowing bottle of Chemical X'を含めること。内容:\n{st.session_state['story']}"
                response = model.generate_content(p)
                st.session_state['prompts'] = response.text
                st.success("プロンプトが完成しました！")

        if 'prompts' in st.session_state:
            st.text_area("英語プロンプト（ナノバナナ用）:", st.session_state['prompts'], height=200)
            st.download_button("プロンプトを保存", st.session_state['prompts'], file_name="prompts.txt")
else:
    st.warning("左側のサイドバーにAPIキーを入力してください。")