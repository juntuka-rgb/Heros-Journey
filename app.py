import streamlit as st
import google.generativeai as genai

# --- SecretsからAPIキーを読み込む ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("エラー: Secretsに GEMINI_API_KEY が設定されていません。")
    st.stop()

# --- 画面のデザイン設定 ---
st.title("🧪 英雄の旅メーカー")
st.caption("〜 あなただけの『英雄の旅』を生成するAIツール 〜")

# ユーザー入力
theme = st.text_input("物語のテーマやキーワードを入力してください（例：失われた記憶、魔法の自転車）")

if st.button("物語を生成する"):
    if not theme:
        st.warning("テーマを入力してください。")
    else:
        with st.spinner("Geminiが物語を紡いでいます..."):
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                prompt = f"「{theme}」をテーマに、神話学者ジョーゼフ・キャンベルの『英雄の旅（ヒーローズ・ジャーニー）』の構成に沿った短編物語を日本語で書いてください。"
                response = model.generate_content(prompt)
                
                st.subheader("📖 生成された物語")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")

# フッター情報
st.divider()
st.info("※このアプリはユーザーネーム「ジュンツカ」の提供（APIキー）で動作しています。")
