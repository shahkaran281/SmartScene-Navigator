import json

def data_json(file_name):
    with open(file_name) as f:
        data = json.load(f)
    return data


data = data_json('test.json')
for key in data:
    scene_num = key
    scene_timestamp = data[key]["timestamp"]
    shots = data[key]["shots"]
    subshots = data[key]["shots"]
    
    print(scene_num , scene_timestamp)
    
    for shot in shots:
        subshots = shots[shot]["subshots"]
        print("\t" + shot , shots[shot]["timestamp"])
    
        for item in subshots:
                for key , value in item.items():
                    print("\t" , "\t" , value)
    print("\n")
        