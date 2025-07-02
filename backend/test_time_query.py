#!/usr/bin/env python3
from modules.influx_query import query_oss_data
from datetime import datetime

def test_basic_time_query():
    """測試基本時間查詢"""
    print("=== 測試基本時間查詢 ===")
    try:
        # 使用你資料中的時間範圍
        time_range = ["2025-07-01 15:58:00", "2025-07-01 16:00:00"]
        
        print(f"查詢時間範圍: {time_range[0]} 到 {time_range[1]}")
        
        # 顯示轉換後的納秒時間戳
        format_string = "%Y-%m-%d %H:%M:%S"
        for i, dt_str in enumerate(time_range):
            dt = datetime.strptime(dt_str, format_string)
            timestamp_sec = dt.timestamp()
            timestamp_ns = int(timestamp_sec * 1000000000)
            print(f"  {dt_str} -> {timestamp_sec} 秒 -> {timestamp_ns} 納秒")
        
        result = query_oss_data(["UE_record"], time_range)
        
        print("✅ 查詢執行成功！")
        print(f"結果數量: {len(result.get('UE_record', []))}")
        
        if result.get('UE_record'):
            print("\n前3筆查詢結果:")
            for i, point in enumerate(result['UE_record'][:3]):
                print(f"  第{i+1}筆: {point}")
        else:
            print("⚠️ 該時間範圍內沒有資料")
            
    except Exception as e:
        print(f"❌ 查詢失敗: {e}")
        import traceback
        traceback.print_exc()

def test_exact_timestamp_query():
    """測試精確時間戳查詢"""
    print("\n=== 測試精確時間戳查詢 ===")
    try:
        # 根據你提供的資料，時間戳是 1751356698838600111
        # 對應時間是 2025-07-01T15:58:04.798000
        
        # 設定一個包含這個時間戳的範圍
        target_time = "2025-07-01 15:58:04"
        end_time = "2025-07-01 15:58:06"
        
        time_range = [target_time, end_time]
        print(f"精確查詢範圍: {target_time} 到 {end_time}")
        
        result = query_oss_data(["UE_record"], time_range)
        
        print("✅ 精確查詢執行成功！")
        print(f"結果數量: {len(result.get('UE_record', []))}")
        
        if result.get('UE_record'):
            print("\n查詢結果:")
            for i, point in enumerate(result['UE_record']):
                print(f"  第{i+1}筆:")
                print(f"    時間: {point.get('time', 'N/A')}")
                print(f"    時間戳: {point.get('timestamp', 'N/A')}")
                print(f"    SUPI: {point.get('supi', 'N/A')}")
                print(f"    gNB_id: {point.get('gNB_id', 'N/A')}")
                print(f"    連接狀態: {point.get('fgcConnectedState', 'N/A')}")
                print()
        else:
            print("⚠️ 精確時間範圍內沒有資料")
            
    except Exception as e:
        print(f"❌ 精確查詢失敗: {e}")
        import traceback
        traceback.print_exc()

def test_wider_time_range():
    """測試更寬的時間範圍"""
    print("\n=== 測試更寬的時間範圍 ===")
    try:
        # 測試整個小時的資料
        time_range = ["2025-07-01 15:00:00", "2025-07-01 16:00:00"]
        
        print(f"寬範圍查詢: {time_range[0]} 到 {time_range[1]}")
        
        result = query_oss_data(["UE_record"], time_range)
        
        print("✅ 寬範圍查詢執行成功！")
        print(f"結果數量: {len(result.get('UE_record', []))}")
        
        if result.get('UE_record'):
            print(f"\n顯示前5筆和後5筆資料:")
            
            # 前5筆
            print("前5筆:")
            for i, point in enumerate(result['UE_record'][:5]):
                print(f"  {i+1}. 時間: {point.get('timestamp', 'N/A')}, SUPI: {point.get('supi', 'N/A')}")
            
            # 如果資料超過10筆，顯示後5筆
            if len(result['UE_record']) > 10:
                print("...")
                print("後5筆:")
                for i, point in enumerate(result['UE_record'][-5:]):
                    idx = len(result['UE_record']) - 5 + i + 1
                    print(f"  {idx}. 時間: {point.get('timestamp', 'N/A')}, SUPI: {point.get('supi', 'N/A')}")
                    
        else:
            print("⚠️ 寬時間範圍內也沒有資料")
            
    except Exception as e:
        print(f"❌ 寬範圍查詢失敗: {e}")
        import traceback
        traceback.print_exc()

def test_no_time_range():
    """測試不指定時間範圍（應該獲取最近的資料）"""
    print("\n=== 測試不指定時間範圍 ===")
    try:
        result = query_oss_data(["UE_record"])
        
        print("✅ 無時間範圍查詢執行成功！")
        print(f"結果數量: {len(result.get('UE_record', []))}")
        
        if result.get('UE_record'):
            print("\n最近的3筆資料:")
            for i, point in enumerate(result['UE_record'][:3]):
                print(f"  第{i+1}筆:")
                print(f"    時間: {point.get('timestamp', 'N/A')}")
                print(f"    SUPI: {point.get('supi', 'N/A')}")
                print()
        else:
            print("⚠️ 沒有找到任何資料")
            
    except Exception as e:
        print(f"❌ 無時間範圍查詢失敗: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 開始測試時間查詢功能\n")
    
    # 執行各項時間查詢測試
    test_no_time_range()
    test_basic_time_query()
    test_exact_timestamp_query()
    test_wider_time_range()
    
    print("\n🏁 時間查詢測試完成！")
