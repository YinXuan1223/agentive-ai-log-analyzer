import os
import requests
from flask import Blueprint, request, jsonify
from services.analysis import analyze_log
from dotenv import load_dotenv

load_dotenv()

api_blueprint = Blueprint("api", __name__)

API_TOKEN = "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"
API_URL = "https://router.huggingface.co/novita/v3/openai/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

@api_blueprint.route("/ask", methods=["POST"])
def ask():
    print('++++ 啟動 API 呼叫 ++++')

    user_question = request.json.get("question", "")
    timestamp_range = request.json.get("timestamp_range", None)
    log_summary = analyze_log(timestamp_range)

    # Few-shot examples + prompt 組裝
    few_shot_examples = """
        【範例 1】
        使用者問題：「這段時間 throughput 為什麼下降？」
        log 摘要：Throughput = 35 Mbps, SNR = 2.5 dB, UE 數量 = 85
        回答：SNR 過低且 UE 數量偏多，造成干擾與訊號品質下降，導致 throughput 明顯降低。
    """

    user_prompt = f"""
        {few_shot_examples}

        【實際問題】
        使用者問題：「{user_question}」
        log 摘要：Throughput = {log_summary['average_throughput']} Mbps,
        RSRP = {log_summary['average_rsrp']} dBm,
        SNR = {log_summary['average_snr']} dB,
        樣本數量 = {log_summary['sample_count']}

        請依照範例風格與邏輯回答。
    """

    payload = {
        "model": "deepseek/deepseek-v3-0324",
        "messages": [
            {
                "role": "system",
                "content": "你是一位專業的 5G 網路分析助理，請根據基站log的資訊和使用者的提問給出回復。"
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    }

    response = requests.post(
        API_URL,
        headers=HEADERS,
        json=payload
    )

    print("response.status_code：", response.status_code)
    print("response.text: ", response.text)

    if response.status_code != 200:
        return jsonify({"answer": f"呼叫 HF inference api 失敗。 code : {response.status_code}, text : {response.text}"})

    result = response.json()
    answer = result["choices"][0]["message"]["content"]
    return jsonify({"answer": answer})

