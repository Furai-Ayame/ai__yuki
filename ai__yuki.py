#2026.01.01
import os
import random
import time
from datetime import datetime, timedelta, timezone

JST = timezone(timedelta(hours=+9), 'JST')
timestamp = datetime.now(JST).strftime("%Y/%m/%d %H:%M:%S")

log_file_path = "ai__yuki_log.txt"  

def yuki_reply(user_input, memory):
    user_input = user_input.strip()
    now = datetime.now()
    user_input = user_input.strip().replace("。", "").replace("？", "?")

    now = datetime.now()
    now_ts = time.time()
    timestamp = time.strftime("%Y-%m-%d-%H-%M-%S")
    
    name = memory.get("name")
    last_talk_time = memory.get("last_time", 0)
    waiting_name = memory.get("waiting_name", False)  
    LONG_TIME = 6 * 60 * 60                                                           #時間経過
    reply = ""

    with open(log_file_path, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}]対話者：{user_input}\n")
        
        if waiting_name:
            memory["name"] = user_input
            memory["waiting_name"] = False
            reply = f"雪:{user_input}さんですね。よろしくお願いします"
            f.write(f"[{timestamp}]{reply}\n")
            return reply
        
        if user_input == "おはよう":
            if name and (now_ts - last_talk_time) >= LONG_TIME:
                reply = f"雪:{name}さん、おはようございます"
            else:
                reply = "雪:おはようございます"
            memory["last_time"] = now_ts

        elif user_input == "はじめまして":
            reply = "雪:はじめまして。お名前を教えてください。\n対話者"
            memory["waiting_name"] = True

        elif user_input == "お名前は何ですか？":
            reply = "雪:雪です"

        elif user_input == "こんにちは":
            reply = "雪:こんにちは"

        elif "時間" in user_input or "何時" in user_input:
            reply = f"雪:今は {now.year}年{now.month}月{now.day}日 {now.hour}時{now.minute}分{now.second}秒 です。"

        elif user_input == "おやすみ":
            reply = "雪:おやすみなさい"

        else:
            reply = "雪:……"

        f.write(f"[{timestamp}]{reply}\n")

    memory["last_topic"] = user_input
    
    return reply

def ask_external(prompt):
    timestamp = time.strftime("%Y-%m-%d-%H-%M-%S")
    return f"[{timestamp}]雪:こんにちは"