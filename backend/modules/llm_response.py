from google import genai
import json

def generate_answer(question, data):
    print('in LLM 2')
    context = "[最近的 OSS 資料]\n"
    context += json.dumps(data)
    print(context)
    # for table, records in data.items():
    #     context += f"\n[{table}]\n"
    #     for r in records:
    #         context += f"- {r['time']} {r['field']} = {r['value']}\n"

    prompt = f"""
    你是電信業者的助手，這裡提供了OSS的資料，請根據以下資料回答問題：
    {context}
    使用者問題：{question}
    """
    print('參考資料:' , context)

    client = genai.Client(api_key="AIzaSyA0r18_cGdmwGHTAQMWomSNR9OHzX25ASs")

    response = client.models.generate_content(
        model='gemini-2.5-flash', contents=prompt
    )
    
    return response.text.strip()
