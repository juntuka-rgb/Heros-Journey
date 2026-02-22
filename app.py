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
    "お爺さんと食べようと思い、お婆さんは桃を引き上げ、家に持って帰りました。\n"
    "夕方、お爺さんが戻り、食べてみることにしたところ中には男の子が。\n"
    "お爺さんとお婆さんは、男の子を桃太郎と名づけ、育てることにしました。\n"
    "桃太郎はすくすくと逞しく育ち、自分の力を試すために遥か遠くの鬼ヶ島へ、鬼を退治する旅に出ました。"
)

# ユーザー入力欄：説明文を変更し、あらかじめ桃太郎の文章を入れておく
st.write("### 📜 物語を紡ぐ")
theme = st.text_area(
    label="表示されているサンプルの文章を、あなたの物語に上書きし、「物語を生成」ボタンを押してみてください。",
    value=default_text,
    height=250
)

if st.button("物語を生成する"):
    if not theme:
        st.warning("物語の種（文章）を入力してください。")
    else:
        with st.spinner("Geminiが物語を紡いでいます..."):
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                # 桃太郎の例が面白いので、プロンプトに「少年漫画風」というスパイスを少し加えても良いかもしれませんね
                prompt = f"以下の物語のあらすじをベースに、神話学者ジョーゼフ・キャンベルの『英雄の旅（ヒーローズ・ジャーニー）』の構成に沿った、熱い少年漫画風の短編物語を日本語で書いてください。\n\nベースとなる話：\n{theme}"
                
                response = model.generate_content(prompt)
                
                if response and response.text:
                    st.subheader("📖 生成された物語")
                    st.write(response.text)
                else:
                    st.error("申し訳ありません。AIがうまく物語を生成できませんでした。別の文章で試してみてください。")
                
            except Exception as e:
                st.error("物語の生成中にエラーが発生しました。別のテーマを試してみてください。")

# --- フッター情報：じゅんさんの署名 ---
st.divider()
st.info("※このアプリはユーザーネーム「ジュンツカ」の提供（APIキー）で動作しています。")
