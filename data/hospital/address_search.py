# address_search.py
# 使用百度地图API进行地址搜索

# import pandas as pd
# from geopy.geocoders import Nominatim
# from geopy.exc import GeocoderTimedOut
# import time
# import os

import requests
import pandas as pd
import time
import os

# # 初始化Nominatim Geocoder
# geolocator = Nominatim(user_agent="hndfzhanghui@qq.com")

# # 查询函数，包含超时处理
# def get_lat_lon(address):
#     try:
#         location = geolocator.geocode(address, timeout=10)
#         if location:
#             return location.latitude, location.longitude
#         else:
#             return None, None
#     except GeocoderTimedOut:
#         time.sleep(1)  # 避免超时连续发生
#         return get_lat_lon(address)

# 替换为你的百度地图API密钥
API_KEY = "YYm23GMe7yrVJGcFYlthwCf4piJTxRWy"

# 查询函数
def get_lat_lon(address):
    base_url = "http://api.map.baidu.com/geocoding/v3/"
    params = {
        "address": address,
        "output": "json",
        "ak": API_KEY
    }
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        if data['status'] == 0:  # 状态码0表示成功
            location = data['result']['location']
            return location['lat'], location['lng']
        else:
            print(f"Error for address '{address}': {data['msg']}")
            return None, None
    except Exception as e:
        print(f"Request failed for address '{address}': {e}")
        return None, None


# 读取地址列表
# 获取当前脚本所在的目录路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 构建addresses.txt的完整路径
addresses_file = os.path.join(current_dir, "addresses.txt")

# 读取文件
addresses = []
try:
    with open(addresses_file, "r", encoding="utf-8") as file:
        addresses = file.readlines()
except FileNotFoundError:
    print(f"错误：找不到文件 {addresses_file}")
    print("请确保在脚本同目录下创建addresses.txt文件")
    exit(1)

# 去掉换行符
addresses = [addr.strip() for addr in addresses]

# 创建DataFrame以保存结果
results = {"Address": [], "Latitude": [], "Longitude": []}

# 查询每个地址的经纬度
for address in addresses:
    lat, lon = get_lat_lon(address)
    results["Address"].append(address)
    results["Latitude"].append(lat)
    results["Longitude"].append(lon)
    print(f"Processed: {address} -> Lat: {lat}, Lon: {lon}")
    time.sleep(0.5)  # 每处理一个地址后暂停0.5秒

# 保存为CSV文件
df = pd.DataFrame(results)
output_file = os.path.join(current_dir, "geocoded_addresses.csv")
df.to_csv(output_file, index=False, encoding="utf-8")

print("Geocoding completed and saved to geocoded_addresses.csv")