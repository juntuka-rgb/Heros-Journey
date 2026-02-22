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
    label="表示されているサンプルの文章を書き換えるか、そのままお使いください。",
    value=default_text,
    height=200
)

# トーンの選択（ここを復活させました！）
st.write("### 🎨 2. 物語のトーンを選択")
tone = st.selectbox(
    "どんな雰囲気の物語にしますか？",
    ["少年漫画風（熱く、情熱的）", "SF・サイバーパンク風（未来的、メカニカル）", "ファンタジー童話風（幻想的、優しい）", "ハードボイルド風（渋い、男臭い）", "ホラー・サスペンス風（不気味、緊張感）"]
)

if st.button("物語を生成する"):
    if not theme.strip():
        st.warning("物語の種（文章）を入力してください。")
    else:
        with st.spinner(f"Geminiが{tone}で物語を紡いでいます..."):
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                
                # プロンプト：選択されたトーンを反映させる
                prompt = (
                    f"以下の『ベースとなる話』を元に、神話学者ジョーゼフ・キャンベルの『英雄の旅（ヒーローズ・ジャーニー）』の構成に沿った物語を日本語で作成してください。\n\n"
                    f"【物語のトーン】: {tone}\n"
                    f"【ベースとなる話】:\n{theme}"
                )
                
                response = model.generate_content(prompt)
                
                if response and response.candidates:
                    generated_text = response.text
                    if generated_text:
                        st.subheader(f"📖 生成された物語（{tone}）")
                        st.write(generated_text)
                    else:
                        st.error("AIからの返答が空でした。もう一度試してみてください。")
                else:
                    st.error("物語の生成に失敗しました。内容を少し変えて試してみてください。")
                
            except Exception as e:
                st.error("申し訳ありません。物語を生成中にエラーが発生しました。")

# --- フッター情報：じゅんさんの署名 ---
st.divider()
st.info("※このアプリはユーザーネーム「ジュンツカ」の提供（APIキー）で動作しています。")
