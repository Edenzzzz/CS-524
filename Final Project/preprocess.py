import json
data = json.load(open("e2e_scaling_efficiency.json"))
filtered_data = []
realistic_num_steps = 25
for entry in data:
    entry["avg_e2e_time"]  = entry["avg_e2e_time"] / entry["steps"] * realistic_num_steps
    entry["e2e_time"] = entry["e2e_time"] / entry["steps"] * realistic_num_steps
    entry["steps"] = realistic_num_steps
    if entry["bs"] == 1:
        filtered_data.append(entry)
json.dump(filtered_data, open("e2e_scaling_efficiency_bs1.json", "w"), indent=4)