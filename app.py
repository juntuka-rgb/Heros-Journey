import streamlit as st
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# --- API設定 ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API KEY NOT FOUND")
    st.stop()

# --- 利用回数カウンター ---
@st.cache_resource
def get_counter():
    return {"count": 0}

counter = get_counter()

# --- 🔒 合言葉設定 ---
CORRECT_PASSWORD = "自転車日本一周20260412"

# --- 画面設定（URLを貼った時のタイトルなどはここ） ---
st.set_page_config(
    page_title="英雄の旅メーカー｜人生を物語に変えるツール",
    page_icon="🧪",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- 実際の画面上の表示（これらは消さずに残す！） ---
st.title("🧪 英雄の旅メーカー")
st.caption("あなたの物語を、英雄の旅のフォーマットに変換するアプリです。")
# --- 🔑 認証サイドバー ---
st.sidebar.write("### 🔑 認証")

# 入力欄のみを表示
input_password = st.sidebar.text_input(
    "合言葉を入力してください", 
    value="", 
    type="password"
)

if input_password != CORRECT_PASSWORD:
    st.warning("⚠️ 認証が必要です。")
    st.stop()

# --- 認証成功後 ---
st.sidebar.success("認証成功")

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

theme = st.text_area(label="物語を上書きし、「英雄の旅に変換」を押してください。", value=default_text, height=200)
tone = st.selectbox("物語のトーン:", ["普通", "少年漫画風", "SF風", "ファンタジー風", "ハードボイルド風", "ホラー風"])

if st.button("🚀 英雄の旅に変換"):
    with st.spinner("Gemini 2.0 が変換中..."):
        try:
            model = genai.GenerativeModel("gemini-2.0-flash")
            safety = {
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
            prompt = f"以下の物語を英雄の旅の12ステップに変換してください。見出しを付けて詳しく書いて。\n【トーン】：{tone}\n【ベース】：\n{theme}"
            response = model.generate_content(prompt, safety_settings=safety)
            st.session_state.story_content = response.text
            st.session_state.image_prompts = ""
            counter["count"] += 1
        except Exception as e:
            st.error("エラーが発生しました。")
            st.exception(e)

# --- 2. 修正・編集セクション ---
if st.session_state.story_content:
    st.divider()
    st.write("### 🔄 2. 物語の修正・調整")
    step_num = st.slider("修正ステップを選択", 1, 12, 1)
    update_instruction = st.text_input(f"ステップ {step_num} への修正指示")
    
    if st.button("🔄 指定したステップを修正する"):
        with st.spinner("修正中..."):
            model = genai.GenerativeModel("gemini-2.0-flash")
            refine_prompt = f"現在の物語：\n{st.session_state.story_content}\n\n指示：ステップ {step_num} を中心に修正：{update_instruction}"
            response = model.generate_content(refine_prompt)
            st.session_state.story_content = response.text

    st.text_area("変換済みテキスト（直接編集も可能）:", value=st.session_state.story_content, height=400)
    st.download_button("📥 物語をテキスト保存", st.session_state.story_content, "hero_journey.txt")

    st.divider()

    # --- 3. ビジュアル構築セクション ---
    st.write("### 🖼️ 3. ビジュアル構築")
    visual_style = st.selectbox("画像のスタイル:", ["実写写真風", "浮世絵風", "3Dアニメ風", "油絵風", "水墨画風", "サイバーパンク"])
    
    if st.button("🎨 画像プロンプト生成"):
        with st.spinner("プロンプト作成中..."):
            model = genai.GenerativeModel("gemini-2.0-flash")
            img_req = f"以下の物語に基づき、画像生成AI用の英語プロンプトを12個作成して。\n【スタイル】：{visual_style}\n\n{st.session_state.story_content}"
            response = model.generate_content(img_req)
            st.session_state.image_prompts = response.text

    if st.session_state.image_prompts:
        st.text_area("画像プロンプト:", value=st.session_state.image_prompts, height=200)
        st.download_button("📥 プロンプトを保存", st.session_state.image_prompts, "image_prompts.txt")

st.divider()
st.write(f"📊 累計誕生した英雄: **{counter['count']}**")
st.info("作者：ジュンツカ 氏 提供 / 2026.04.12 自転車日本一周 出発予定")
