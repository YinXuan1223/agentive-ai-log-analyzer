# from influxdb import InfluxDBClient

# client = InfluxDBClient(
#     host = "140.113.144.121",
#     port = 2981,
#     username = "root",
#     password = "root",
#     database = "wisdon-cell"
# )
# print('start to get data')
# tables = ["UE_record"]
# def query_oss_data(tables, time_range):
    
#     result = {}
#     table_name_in_db = {"UE_record": "ueList_test", "fault management": "fm_test"}
#     for table in tables:
#         query = f'''
#             select * from {table_name_in_db[table]} limit  5
#         '''
#         output = client.query(query)
#         print(output.get_points())
#         # result[table] = []
#         # for table_result in output:
#         #     for record in table_result.records:
#         #         result[table].append({
#         #             "time": record.get_time().isoformat(),
#         #             "value": record.get_value(),
#         #             "field": record.get_field()
#         #         })
#     client.close()
#     # return result

# # from influxdb import InfluxDBClient

# # client = InfluxDBClient(
# #     host="140.113.144.121",
# #     port=2981,
# #     username="root",
# #     password="root",
# #     database="wisdon-cell"
# # )

# # # 測試 ping（是否連得上）
# # try:
# #     pong = client.ping()
# #     print(f"[連線成功] InfluxDB 回應: {pong}")
# # except Exception as e:
# #     print(f"[連線失敗] 錯誤：{e}")
# #     exit(1)

# # # 查詢最近的 5 筆資料
# # query = 'SELECT * FROM "ueList_test" LIMIT 5'
# # result = client.query(query)

# # points = list(result.get_points())
# # if not points:
# #     print("[⚠️ 沒有資料] 查詢成功但結果為空")
# # else:
# #     print(f"[✅ 查詢成功] 共 {len(points)} 筆資料")
# #     for i, point in enumerate(points, 1):
# #         print(f"{i}. {point}")

# # client.close()

from influxdb import InfluxDBClient

client = InfluxDBClient(
    host="140.113.144.121",
    port=2981,
    username="root",
    password="root",
    database="wisdon-cell"
)

def query_oss_data(tables, time_range=None):

    result = {}
    table_name_in_db = {"UE_record": "ueList_test", "fault management": "fm_test"}

    for table in tables:
        query = f'SELECT * FROM {table_name_in_db[table]} limit 5'
        output = client.query(query)

        result[table] = []
        for point in output.get_points():
            # print(point)          # 印出每筆資料
            result[table].append(point)
    # print(result)
    client.close()
    return result


