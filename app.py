from flask import Flask, request, jsonify
import os
from groq import Groq

app = Flask(__name__)

# Groq APIキーを環境変数から取得
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
# Groqクライアントを作成
client = Groq(api_key=GROQ_API_KEY)
@app.route('/',methods = ['GET','POST'])
def initial():
    return "success"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get("user_input")
    system_content = data.get("system_content", "あなたは便利なアシスタントです。質問には簡潔に答えてください。")

    # システムプロンプトを設定
    system_prompt = {
        "role": "system",
        "content": system_content
    }

    # ユーザープロンプトを設定
    user_prompt = {
        "role": "user", "content": user_input
    }

    # チャット履歴を初期化
    chat_history = [system_prompt, user_prompt]

    # Groq APIを使用して応答を生成
    response = client.chat.completions.create(model="llama3-70b-8192",
                                              messages=chat_history,
                                              max_tokens=100,
                                              temperature=0)

    # 応答を取得
    answer = response.choices[0].message.content

    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(debug=True)
