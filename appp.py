from flask import Flask, render_template, request, jsonify
import time
from datetime import datetime, timedelta, timezone
JST = timezone(timedelta(hours=+9), 'JST')

appp = Flask(__name__)

memory = {}

log_file_path = "ai__yuki_log.txt"

def yuki_reply(user_input, memory):
    user_input = user_input.strip().replace("。", "").replace("？", "?") 
    now = datetime.now()
    now_ts = time.time()
    timestamp = datetime.now(JST).strftime("%Y/%m/%d %H:%M:%S")

    name = memory.get("name")
    last_talk_time = memory.get("last_time", 0)
    LONG_TIME = 6 * 60 * 60
    reply = ""

    with open(log_file_path, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}]対話者：{user_input}\n")

        if user_input == "おはよう":
            if name and (now_ts - last_talk_time) >= LONG_TIME:
                reply = f"雪:{name}さん、おはようございます"
            else:
                reply = "雪:おはようございます"
            memory["last_time"] = now_ts

        elif user_input == "はじめまして":
            reply = "雪:はじめまして。お名前を教えてください。"

        elif user_input == "こんにちは":
            reply = "雪:こんにちは"

        
        elif "時間" in user_input or "何時" in user_input:
            reply = f"雪:今は {now.year}年{now.month}月{now.day}日 {now.hour + 9}時{now.minute}分{now.second}秒 です。"

        elif user_input == "おやすみ":
            reply = "雪:おやすみなさい"

        else:
            reply = "雪:……"

        f.write(f"[{timestamp}]{reply}\n")

    memory["last_topic"] = user_input
    
    return reply

@appp.route("/")
def html():
    initial_chat = [
        {"type": "bot", "text": "雪:入力待機中"}
    ]
    return render_template("html.html", initial_chat=initial_chat)

@appp.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    bot_message = yuki_reply(user_message, memory)
    return jsonify({"reply": bot_message})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    appp.run(host="0.0.0.0", port=port)