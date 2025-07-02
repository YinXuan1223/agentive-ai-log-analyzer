from google import genai
import json


def parse_question(question):

    prompt = f"""
    你是電信業者對OSS資料提問的語意解析助手。請將使用者的問題轉成如下 JSON 格式：
    {{"need_data": true, "tables": ["UE_record", "fault management"], "time_range": "-5m", "direct_answer": ""}}
    注意，tables只有"UE_record", "fault management"這兩種選項。
    
    舉例來說，如果使用者問題是「前五分鐘系統狀況如何?」，這時需要參考UE_record和fault management兩種資料，並且時間範圍是5分鐘，請輸出:
    {{"need_data": true, "tables": ["UE_record", "fault management"], "time_range": "-5m", "direct_answer": ""}}

    如果使用者的問題是「在5G系統裡面，RU, CU, DU 是甚麼?」這個問題不用參考OSS的資料，所以可以直接就你的認知回答，請輸出:
    {{"need_data": false, "tables": [], "time_range": "", "direct_answer": "在5G網路架構中，RU、CU和DU是組成無線接取網路(RAN)的三個主要元件"}}

    使用者問題：「{question}」

    重要：請只輸出純粹的 JSON 格式，不要包含任何其他文字、標記或說明。JSON 必須是有效的格式。
    """

    client = genai.Client(api_key="AIzaSyA0r18_cGdmwGHTAQMWomSNR9OHzX25ASs")

    response = client.models.generate_content(
        model='gemini-2.5-flash', contents=prompt
    )

    print("原始回應: ", response.text)
    
    # 清理回應文本，移除各種可能的格式標記
    json_response = response.text.strip()
    
    # 移除可能的 markdown 代碼塊標記
    json_response = json_response.replace("```json", "")
    json_response = json_response.replace("```", "")
    
    # 移除可能的前綴文字
    if "response:" in json_response:
        json_response = json_response.split("response:")[-1].strip()
    
    # 尋找 JSON 開始和結束的位置
    start_idx = json_response.find("{")
    end_idx = json_response.rfind("}") + 1
    
    if start_idx != -1 and end_idx > start_idx:
        json_response = json_response[start_idx:end_idx]
    
    print("清理後的回應: ", json_response)
    
    try:
        parsed_result = json.loads(json_response)
        print("解析成功: ", parsed_result)
        return parsed_result
    except json.JSONDecodeError as e:
        print(f"JSON 解析錯誤: {e}")
        print(f"嘗試解析的文本: {json_response}")
        return {
            "need_data": False,
            "direct_answer": "解析問題失敗，請重新描述。",
            "tables": [],
            "time_range": None
        }