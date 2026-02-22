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
st.caption("〜 あなただけの『英雄の旅』を生成・編集・出力するフルセットAIツール 〜")

# サンプル文章
default_text = (
    "むかしむかし、あるところにお祖父さんとお婆さんがいました。\n"
    "お爺さんは山に芝刈りに、お婆さんは川に洗濯に行きました。\n"
    "すると川の上流から大きな桃が流れてきました。\n"
    "お婆さんは桃を引き上げ、家に持って帰りました。\n"
    "中から生まれた男の子を桃太郎と名づけ、大切に育てました。\n"
    "桃太郎は逞しく育ち、遥か遠くの鬼ヶ島へ、鬼を退治する旅に出ました。"
)

# 1. 入力セクション
st.write("### 📜 1. 物語のベースを入力")
theme = st.text_area("物語のあらすじ:", value=default_text, height=150)

st.write("### 🎨 2. 物語のトーンを選択")
tone = st.selectbox(
    "雰囲気を選択:",
    ["普通（標準的な物語）", "少年漫画風（熱く、情熱的）", "SF・サイバーパンク風（未来的、メカニカル）", "ファンタジー童話風（幻想的、優しい）", "ハードボイルド風（渋い、男臭い）", "ホラー・サスペンス風（不気味、緊張感）"]
)

# セッション状態の初期化（物語を保持するため）
if "story_content" not in st.session_state:
    st.session_state.story_content = ""
if "image_prompts" not in st.session_state:
    st.session_state.image_prompts = ""

if st.button("🚀 物語と画像プロンプトを生成"):
    with st.spinner("Gemini 2.0 が全行程を構築中..."):
        try:
            model = genai.GenerativeModel("gemini-2.0-flash")
            safety = {HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                      HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                      HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                      HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE}

            # 物語生成用のプロンプト
            story_prompt = (
                f"以下の話をベースに、ジョーゼフ・キャンベルの『英雄の旅（12のステップ）』に沿った詳細な物語を書いてください。\n"
                f"トーン：{tone}\nベース：{theme}\n"
                f"出力形式：各ステップにタイトルを付け、それぞれの内容を詳しく記述してください。"
            )
            
            res_story = model.generate_content(story_prompt, safety_settings=safety)
            st.session_state.story_content = res_story.text

            # 画像プロンプト生成
            image_prompt_req = (
                f"以下の物語の各シーンに合う、画像生成AI（Midjourney等）用の英語プロンプトを12個作成してください。\n"
                f"トーン：{tone}\n内容：\n{st.session_state.story_content}"
            )
            res_image = model.generate_content(image_prompt_req, safety_settings=safety)
            st.session_state.image_prompts = res_image.text

        except Exception as e:
            st.error("生成中にエラーが発生しました。")
            st.exception(e)

# --- 生成後の表示・編集・出力エリア ---
if st.session_state.story_content:
    st.divider()
    
    # 3. 納得いくまで修正できる編集エリア
    st.write("### 📝 3. 物語の確認と修正")
    edited_story = st.text_area("生成された物語（ここで自由に編集できます）:", value=st.session_state.story_content, height=400)
    st.session_state.story_content = edited_story

    # 4. 物語のテキストファイル出力
    st.download_button(
        label="📥 物語をテキスト保存",
        data=st.session_state.story_content,
        file_name="hero_story.txt",
        mime="text/plain"
    )

    st.divider()

    # 5. 画像生成用プロンプトエリア
    st.write("### 🖼️ 4. 画像生成用プロンプト（英語）")
    edited_prompts = st.text_area("各ステップのビジュアル指示:", value=st.session_state.image_prompts, height=300)
    st.session_state.image_prompts = edited_prompts

    # 6. 画像プロンプトのテキストファイル出力
    st.download_button(
        label="📥 画像プロンプトをテキスト保存",
        data=st.session_state.image_prompts,
        file_name="image_prompts.txt",
        mime="text/plain"
    )

# --- フッター ---
st.divider()
st.info("※このアプリはユーザーネーム「ジュンツカ」の提供（APIキー）で動作しています。")
