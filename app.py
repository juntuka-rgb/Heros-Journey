import streamlit as st
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# --- SecretsからAPIキーを読み込む ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("エラー: Secretsに GEMINI_API_KEY が設定されていません。")
    st.stop()

# --- 画面のデザイン設定 ---
st.title("🧪 英雄の旅メーカー")
st.caption("〜 あなただけの『英雄の旅』を生成するAIツール 〜")

# サンプル文章の準備
default_text = (
    "むかしむかし、あるところにお祖父さんとお婆さんがいました。\n"
    "お爺さんは山に芝刈りに、お婆さんは川に洗濯に行きました。\n"
    "すると川の上流から大きな桃が流れてきました。\n"
    "お婆さんは桃を引き上げ、家に持って帰りました。\n"
    "中から生まれた男の子を桃太郎と名づけ、大切に育てました。\n"
    "桃太郎は逞しく育ち、遥か遠くの鬼ヶ島へ、鬼を退治する旅に出ました。"
)

# ユーザー入力欄
st.write("### 📜 1. 物語のベースを入力")
theme = st.text_area(
    label="表示されているサンプルの文章を、あなたの物語に上書きし、「物語を生成」ボタンを押してみてください。",
    value=default_text,
    height=200
)

# トーンの選択（「普通」を最初に追加しました）
st.write("### 🎨 2. 物語のトーンを選択")
tone = st.selectbox(
    "どんな雰囲気の物語にしますか？",
    ["普通（標準的な物語）", "少年漫画風（熱く、情熱的）", "SF・サイバーパンク風（未来的、メカニカル）", "ファンタジー童話風（幻想的、優しい）", "ハードボイルド風（渋い、男臭い）", "ホラー・サスペンス風（不気味、緊張感）"]
)

if st.button("物語を生成する"):
    if not theme.strip():
        st.warning("物語の種（文章）を入力してください。")
    else:
        with st.spinner(f"Geminiが「{tone}」で物語を紡いでいます..."):
            try:
                # 安全設定
                safety_settings = {
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                }
                
                # モデル名の指定を修正（404エラー対策）
                model = genai.GenerativeModel("gemini-1.5-flash")
                
                # プロンプトの構築
                prompt = (
                    f"以下の『ベースとなる話』を元に、神話学者ジョーゼフ・キャンベルの『英雄の旅（ヒーローズ・ジャーニー）』の構成に沿った物語を日本語で作成してください。\n\n"
                    f"【物語のトーン】: {tone}\n"
                    f"【ベースとなる話】:\n{theme}"
                )
                
                # 生成実行
                response = model.generate_content(prompt, safety_settings=safety_settings)
                
                if response and response.text:
                    st.subheader(f"📖 生成された物語（{tone}）")
                    st.write(response.text)
                else:
                    st.error("AIが回答を控えました。内容を変えて試してください。")
                    
            except Exception as e:
                # 最終的なエラー表示
                st.error("物語の生成中にエラーが発生しました。")
                st.exception(e)

# --- フッター情報：じゅんさんの署名 ---
st.divider()
st.info("※このアプリはユーザーネーム「ジュンツカ」の提供（APIキー）で動作しています。")
