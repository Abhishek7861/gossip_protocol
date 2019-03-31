import json

with open("config.json", "r") as read_file:
    data = json.load(read_file)
read_file.close()

data["Server Point Address"] = [1,2,3]
hello = json.dumps(data["Access Point Address"])

# data = json.dumps(data,indent=4)

with open("config.json", "w") as read_file:
     json.dump(data,read_file)
     read_file.close()

print(data)
