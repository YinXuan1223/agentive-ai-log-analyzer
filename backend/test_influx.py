#!/usr/bin/env python3
from modules.influx_query import query_oss_data

if __name__ == "__main__":
    print("測試 InfluxDB 連接...")
    try:
        result = query_oss_data(["UE_record"])
        print("查詢成功！")
        print(f"結果: {result}")
    except Exception as e:
        print(f"查詢失敗: {e}")
