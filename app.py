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
st.caption("あなたの物語を、英雄の旅のフォーマットに変換するアプリです。")

# --- セッション状態の初期化 ---
if "story_content" not in st.session_state:
    st.session_state.story_content = ""
if "image_prompts" not in st.session_state:
    st.session_state.image_prompts = ""

# --- 1. 入力セクション ---
st.write("### 📜 1. 物語のベースを入力")
default_text = (
    "むかしむかし、あるところにお祖父さんとお婆さんがいました。\n"
    "お爺さんは山に芝刈りに、お婆さんは川に洗濯に行きました。\n"
    "すると川の上流から大きな桃が流れてきました。\n"
    "お爺さんと食べようと思い、お婆さんは桃を引き上げ、家に持って帰りました。\n"
    "夕方、お爺さんが戻り、食べてみることにしたところ中には男の子が。\n"
    "お爺さんとお婆さんは、男の子を桃太郎と名づけ、育てることにしました。\n"
    "桃太郎はすくすくと逞しく育ち、自分の力を試すために遥か遠くの鬼ヶ島へ、鬼を退治する旅に出ました。"
)

theme = st.text_area(
    label="入力欄にあなたの物語を上書きし、「英雄の旅に変換」ボタンを押してください。",
    value=default_text,
    height=200
)

tone = st.selectbox("物語のトーンを選択:", ["普通", "少年漫画風", "SF風", "ファンタジー風", "ハードボイルド風", "ホラー風"])

if st.button("🚀 英雄の旅に変換"):
    with st.spinner("変換中..."):
        try:
            model = genai.GenerativeModel("gemini-2.0-flash")
            safety = {
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
            prompt = (
                f"以下の物語をベースに、英雄の旅（ヒーローズ・ジャーニー）の12ステップの構成で詳細な物語に変換してください。\n"
                f"各ステップに見出しをつけてください。\n"
                f"【トーン】：{tone}\n"
                f"【ベース】：\n{theme}"
            )
            response = model.generate_content(prompt, safety_settings=safety)
            st.session_state.story_content = response.text
            # 物語が新しくなったら画像プロンプトは一旦クリア
            st.session_state.image_prompts = ""
        except Exception as e:
            st.error("エラーが発生しました。")
            st.exception(e)

# --- 2. 修正指示セクション（物語生成後のみ表示） ---
if st.session_state.story_content:
    st.divider()
    st.write("### 🔄 2. 物語の修正・調整")
    
    # 修正するステップをスライダで指定
    step_num = st.slider("修正したいステップを選択してください", 1, 12, 1)
    update_instruction = st.text_input(f"ステップ {step_num} への修正指示（例：もっと緊迫感を出して）")
    
    if st.button("🔄 指定したステップを修正する"):
        with st.spinner(f"ステップ {step_num} を修正中..."):
            try:
                model = genai.GenerativeModel("gemini-2.0-flash")
                refine_prompt = (
                    f"現在の物語：\n{st.session_state.story_content}\n\n"
                    f"指示：上記の物語のうち、ステップ {step_num} を中心に以下の指示通り修正し、全体の整合性を保った物語を再出力してください。\n"
                    f"修正内容：{update_instruction}"
                )
                response = model.generate_content(refine_prompt)
                st.session_state.story_content = response.text
            except Exception as e:
                st.error("修正中にエラーが発生しました。")

    # 編集・表示エリア
    st.session_state.story_content = st.text_area("変換済みテキスト（直接編集も可能）:", value=st.session_state.story_content, height=400)
    st.download_button("📥 物語をテキスト保存", st.session_state.story_content, "hero_journey.txt")

    st.divider()

    # --- 3. 画像プロンプト生成 ---
    st.write("### 🖼️ 3. ビジュアル構築")
    if st.button("🎨 全12ステップの画像プロンプトを生成"):
        with st.spinner("プロンプト作成中..."):
            model = genai.GenerativeModel("gemini-2.0-flash")
            img_req = f"以下の12ステップの物語に基づき、画像生成AI用の英語プロンプトを各ステップ1つずつ、計12個作成して。 \n\n{st.session_state.story_content}"
            response = model.generate_content(img_req)
            st.session_state.image_prompts = response.text

    if st.session_state.image_prompts:
        st.session_state.image_prompts = st.text_area("画像プロンプト:", value=st.session_state.image_prompts, height=200)
        st.download_button("📥 プロンプトを保存", st.session_state.image_prompts, "image_prompts.txt")

# フッター
st.divider()
st.info("※このアプリはユーザーネーム「ジュンツカ」の提供（APIキー）で動作しています。")
