import streamlit as st
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# APIキー設定
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API KEY NOT FOUND IN SECRETS")
    st.stop()

st.title("🧪 英雄の旅メーカー")

# 入力部（前回の内容を継承）
default_text = "（略）" # ここは先ほどの桃太郎の文章を適宜入れてください
theme = st.text_area("物語のベース", value=default_text, height=200)
tone = st.selectbox("トーン", ["少年漫画風", "SF風", "ファンタジー風", "ハードボイルド風", "ホラー風"])

if st.button("物語を生成する"):
    with st.spinner("Processing..."):
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            # 安全設定（最も緩い設定）
            safety = {
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }

            response = model.generate_content(
                f"トーン：{tone}\nベース：{theme}\n上記で英雄の旅を書いて。",
                safety_settings=safety
            )

            # プロ的デバッグ：レスポンスの中身を確認
            if response.candidates:
                # 候補がある場合、テキストへのアクセスを試みる
                try:
                    st.write(response.text)
                except Exception as e:
                    # テキスト化に失敗（フィルターブロック等）した場合のログ
                    st.warning("テキスト変換エラー：安全フィルターにより内容が遮断された可能性があります。")
                    st.write("Debug info (Feedback):", response.prompt_feedback)
            else:
                st.error("AIからのレスポンス候補（Candidates）が空です。")

        except Exception as e:
            # ホストコンピューター時代の腕が鳴る（？）、生の例外表示
            st.error("Runtime Error Exception")
            st.exception(e) # これで詳細なスタックトレースが出ます

st.divider()
st.info("※このアプリはユーザーネーム「ジュンツカ」の提供（APIキー）で動作しています。")
