import requests
import json
import time
import os
from datetime import datetime, timedelta, timezone

# 基礎設定
base_url = "http://140.113.144.117:31089"
Influx_post_url = "http://140.113.144.121:2980/Influx/wisdon-cell"

# 對於需帶入 gnbId 的 API，請設定 gnb id 清單（依實際環境調整）
gnb_ids = [1, 2]

# pm raw API 的 measurement 名稱清單
measurement_names = [
    "accessibility-drbAccessibility",
    "retainability-drbRetain",
    "availability-cellAvailability",
    "mobility-granHoS",
    "prbutilization-dlPrbUtilization",
    "prbutilization-ulPrbUtilization",
    "energySaving-drbPdcpSduVolDl",
    "energySaving-drbPdcpSduVolUl",
]

# 設定存放日誌的根目錄與各 API 子目錄
log_dir = "./log/day_log"
api_dirs = {
    "ueList": os.path.join(log_dir, "ueList"),
    "pm_raw": os.path.join(log_dir, "pm_raw"),
    "ueConnectedCount": os.path.join(log_dir, "ueConnectedCount"),
    "fm": os.path.join(log_dir, "fm"),
}
for d in api_dirs.values():
    os.makedirs(d, exist_ok=True)

# 共用 Header (可根據需要調整)
headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJleHAiOjkzMTIwODE4NjY1LCJ1c2VybmFtZSI6Im9hbS1yZXBvcnRlciJ9.o2kBfYESgH3CZXYNITzCehCgJ2Jbt9ATeDQw8QVWDYwBhDysxxYQGqguDRNCKmblVpMdT2LxZuEuLpJCsiuQ-g",
}

# 每秒執行一次資料蒐集
# next_time = datetime.utcnow() deprecated
next_time = datetime.now(timezone.utc)
loop_count = 0  # 新增一個統計變數
while True:
    current_time = datetime.now(timezone.utc)
    if current_time < next_time:
        time.sleep((next_time - current_time).total_seconds())

    # 設定統一的查詢時間區間：從 15 秒前到 14 秒前的 1 秒區間
    start_time_ms = int((current_time - timedelta(seconds=15)).timestamp() * 1000)
    end_time_ms = int((current_time - timedelta(seconds=14)).timestamp() * 1000)

    date_str = current_time.strftime("%Y-%m-%d")
    timestamp = end_time_ms

    # 定義各 API 檔案路徑
    file_paths = {
        "ueList": os.path.join(api_dirs["ueList"], f"{date_str}_ueList.json"),
        "pm_raw": os.path.join(api_dirs["pm_raw"], f"{date_str}_pm_raw.json"),
        "ueConnectedCount": os.path.join(
            api_dirs["ueConnectedCount"], f"{date_str}_ueConnectedCount.json"
        ),
        "fm": os.path.join(api_dirs["fm"], f"{date_str}_fm.json"),
    }

    # 1. API: /v1/gnb/{gnbId}/ueList
    ueList_record = {"timestamp": timestamp, "data": {}}
    for gnb in gnb_ids:
        url_ueList = f"{base_url}/v1/gnb/{gnb}/ueList"
        params = {"_startTime": start_time_ms, "_endTime": end_time_ms}
        try:
            resp = requests.get(url_ueList, headers=headers, params=params)
            if resp.status_code == 200:
                ueList_record["data"][str(gnb)] = resp.json()
                # print(str(gnb), ueList_record["data"][str(gnb)], '\n')
            else:
                ueList_record["data"][str(gnb)] = {
                    "error": f"HTTP {resp.status_code}",
                    "response": resp.text,
                }
        except Exception as e:
            ueList_record["data"][str(gnb)] = {"error": str(e)}
        
        print(ueList_record)
        for gNB_id, ue_list in ueList_record["data"].items():
            for ue_data in ue_list:

                uedata_json = [
                    {   
                        "measurement": "ueList_test",
                        "tags": {
                            "timestamp" : datetime.fromtimestamp(int(ueList_record['timestamp']) / 1000).isoformat(),
                            "gNB_id" : gNB_id,
                            "supi" : ue_data["supi"]
                        },
                        
                        "fields": {
                            "ranRegisteredState" : ue_data["ranRegisteredState"],
                            "fgcConnectedState" : ue_data["fgcConnectedState"],
                            "CellRadioNetworkTemp_id" : ue_data["crnti"],
                            "PhysicalCell_id": ue_data["pci"],
                            "TrackingAreaCode": ue_data["tac"],
                            "DataNetworkName": ue_data["dnn"],
                            "dl_sinr": ue_data["dl_sinr"],
                            "dl_rsrp": ue_data["dl_rsrp"],
                            "nrCellId": ue_data["nrCellId"],
                            "dlThroughputBps": ue_data["dlThroughputBps"],
                            "ulThroughputBps": ue_data["ulThroughputBps"]
                        },
                        
                        
                        # "time": datetime.now(timezone.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
                    }
                ]

                influx_headers = {
                    'accept': 'application/json'
                }

                json_data = json.dumps(uedata_json)
                response = requests.post(Influx_post_url, headers=influx_headers, data=json_data)
                print(f"Response status code: {response.status_code}")
                # print(f"Response content: {response.text}")
                print('Done ueList post')
                print('-----')
        

    with open(file_paths["ueList"], "a") as f:
        f.write(json.dumps(ueList_record, ensure_ascii=False) + "\n")

    # 2. API: /v1/report/ric/pm/raw － 針對所有 measurement
    pm_raw_record = {"timestamp": timestamp, "data": {}}
    url_pm_raw = f"{base_url}/v1/report/ric/pm/raw"
    for measurement in measurement_names:
        params = {
            "measurementName": measurement,
            "_startTime": start_time_ms,
            "_endTime": end_time_ms,
            "_size": 500,
            "_sort": "time DESC",
        }
        try:
            resp = requests.get(url_pm_raw, headers=headers, params=params)
            if resp.status_code == 200:
                data = resp.json()
                # 如果回傳為物件且有 content 欄位，取 content；否則存整個回傳結果
                if isinstance(data, dict) and "content" in data:
                    pm_raw_record["data"][measurement] = data["content"]
                else:
                    pm_raw_record["data"][measurement] = data
            else:
                pm_raw_record["data"][measurement] = {
                    "error": f"HTTP {resp.status_code}",
                    "response": resp.text,
                }
        except Exception as e:
            pm_raw_record["data"][measurement] = {"error": str(e)}

    with open(file_paths["pm_raw"], "a") as f:
        f.write(json.dumps(pm_raw_record, ensure_ascii=False) + "\n")

    # 3. API: /v1/gnb/{gnbId}/ueConnectedCount （每兩秒呼叫一次）
    if loop_count % 1 == 0:  # 每兩次迴圈執行一次
        ueConnectedCount_record = {"timestamp": timestamp, "data": {}}
        for gnb in gnb_ids:
            url_ueConn = f"{base_url}/v1/gnb/{gnb}/ueConnectedCount"
            params = {"_startTime": start_time_ms, "_endTime": end_time_ms}
            try:
                resp = requests.get(url_ueConn, headers=headers, params=params)
                if resp.status_code == 200:
                    ueConnectedCount_record["data"][str(gnb)] = resp.json()
                else:
                    ueConnectedCount_record["data"][str(gnb)] = {
                        "error": f"HTTP {resp.status_code}",
                        "response": resp.text,
                    }
            except Exception as e:
                ueConnectedCount_record["data"][str(gnb)] = {"error": str(e)}

        with open(file_paths["ueConnectedCount"], "a") as f:
            f.write(json.dumps(ueConnectedCount_record, ensure_ascii=False) + "\n")

    # 4. API: /v1/report/ric/fm
    fm_record = {"timestamp": timestamp}
    url_fm = f"{base_url}/v1/report/ric/fm"
    params = {
        "_startTime": start_time_ms,
        "_endTime": end_time_ms,
        "_size": 100,
        "_sort": "time DESC",
    }
    try:
        resp = requests.get(url_fm, headers=headers, params=params)
        if resp.status_code == 200:
            fm_record["data"] = resp.json()
        else:
            fm_record["data"] = {
                "error": f"HTTP {resp.status_code}",
                "response": resp.text,
            }
    except Exception as e:
        fm_record["data"] = {"error": str(e)}
    
    if "content" in fm_record['data']:

        if fm_record["data"]["content"]:
    
            fmdata_json = [
                {   
                    "measurement": "fm_test",
                    "tags": {
                        "timestamp" : datetime.fromtimestamp(int(fm_record['timestamp']) / 1000).isoformat(),
                        
                    },
                    
                    "fields": {
                        "alarmType" : data['data']['content'][0]['alarmType'],
                        "description" : data['data']['content'][0]['description'],
                        "SOP" : data['data']['content'][0]['sop'],
                        
                    }
                    
                    
                    # "time": datetime.now(timezone.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
                }
            ]

            influx_headers = {
                'accept': 'application/json'
            }

            fm_json_data = json.dumps(fmdata_json)
            response = requests.post(Influx_post_url, headers=influx_headers, data=fm_json_data)
            print(f"Response status code: {response.status_code}")
            # print(f"Response content: {response.text}")
            print('Done fm_test post')
            print('-----')

    with open(file_paths["fm"], "a") as f:
        f.write(json.dumps(fm_record, ensure_ascii=False) + "\n")

    # 設定下一次執行時間（每秒）
    next_time = datetime.now(timezone.utc) + timedelta(seconds=1)
    loop_count += 1
    print(loop_count)
