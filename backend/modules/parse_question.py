from google import genai
from datetime import datetime
import json


def parse_question(question):
    
    # now = datetime.now()
    # formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")

    prompt = f"""
    你是電信業者對OSS資料提問的語意解析助手。請將使用者的問題轉成如下 JSON：
    {{
      "need_data": true/false,
      "tables": ["UE_record", "fault management"],
      "time_range": ["start_time", "end_time"],
      "direct_answer": "如果 need_data=false，請提供直接回答。"
    }}
    舉例來說，如果使用者問題是「前五分鐘系統狀況如何?」，這時需要參考UE_record和fault management兩種資料，並且時間範圍是10分鐘，請把10分鐘前的時刻和現在的時刻列在time_range裡，時間的格式為2025-06-10 15:30:10，請輸出:
    {{
      "need_data": true,
      "tables": ["UE_record", "fault management"],
      "time_range": ["前十分鐘的時間","現在的時間"],
      "direct_answer": ""
    }}
    如果使用者的問題是「在5G系統裡面，RU, CU, DU 是甚麼?」這個問題不用參考OSS的資料，所以可以直接就你的認知回答，請輸出:
    {{
      "need_data":false,
      "tables": [],
      "time_range": "",
      "direct_answer": "在5G網路架構中，RU、CU和DU是組成無線接取網路(RAN)的三個主要元件"
    }}
    使用者問題：「{question}」
    現在時間 : 2025-07-01 16:02:07
    請只輸出 JSON，你輸出的結果要讓我用json.loads成功轉成dictionary。
    """

    client = genai.Client(api_key="AIzaSyA0r18_cGdmwGHTAQMWomSNR9OHzX25ASs")

    response = client.models.generate_content(
        model='gemini-2.5-flash', contents=prompt
    )

    print("response: ", response.text)

    # response.text 長這樣 他是 string 不是 json 格式，所以
    # ```json{
    # "need_data": true,
    # "tables": ["fault management"],
    # "time_range": "-1h",
    # "direct_answer": ""
    # }
    # ```

    json_response = response.text.replace("```json", "")
    json_response = json_response.replace("```", "")
    print("response: ", json.loads(json_response))

    try:
        return json.loads(json_response)
    except Exception as e:
        return {
            "need_data": False,
            "direct_answer": "出現問題，應該是json的格式有錯。",
            "tables": [],
            "time_range": None
        }