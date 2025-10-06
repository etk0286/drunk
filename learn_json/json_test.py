import json


new_data = [1,2,3]
data=[]

try:
    with open("data.json", "r") as f:
        data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    data = [["start"]]  

data.append(new_data)


with open("data.json", "w") as f:
    json.dump(data, f, indent=4)  



# 3. 從 JSON 檔案讀取資料
with open("data.json", "r") as f:
    loaded_data = json.load(f)

print("📂 從 data.json 讀出來的資料：")
print(loaded_data)
print(loaded_data[1][1])


