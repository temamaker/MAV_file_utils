import sys
import csv

DEBUG = True

IGNORE = [
"AHRS_TRIM_X",
"AHRS_TRIM_Y",
"ARSPD_OFFSET",
"BARO1_GND_PRESS",
"BARO2_GND_PRESS",
"COMPASS_OFS",
"INS_ACC",
"INS_GYR",
"STAT_"
]

def load_params(filepath):
    params = {}
    with open(filepath, 'r') as f:
        for line in f.readlines():
            # ArduPilot param files start lines with param name or #
            if line.startswith("#") or not (line := line.strip()):
                continue
            parts = line.split(sep=",")
            if len(parts) >= 2:
                # { "ATC_ANG_PIT_P": "4.5" }
                params[parts[0]] = parts[1]
    
    return params

def generate_diff(file_default, file_new):
    default = load_params(file_default)
    new = load_params(file_new)
    
    # Get all unique keys from both files
    all_keys = sorted(set(default.keys()) | set(new.keys()))
    
    csv_table = []
    csv_filename = "diff_output.csv"

    print(f"| Parameter | Default Value | New Value | Status | Explanation/Reasoning |")
    print(f"| :--- | :--- | :--- | :--- | :--- |")
    
    for key in all_keys:
        val_def = default.get(key, "MISSING")
        val_new = new.get(key, "MISSING")
        
        if val_def != val_new and not any(x in key for x in IGNORE):
            status = "CHANGED" if val_def != "MISSING" and val_new != "MISSING" else "NEW"
            # We only print the ones that are different or new
            print(f"| {key:<30} | {val_def:<20} | {val_new:<20} | {status:<20} | |")
            csv_table.append({'Parameter':key,
                              'Default':val_def,
                              'New':val_new, 
                              'Status':status,
                              'Explanation/Reasoning':''})
    #Save the results in CSV format   
    fieldnames = ['Parameter',
                'Default',
                'New', 
                'Status',
                'Explanation/Reasoning']
    with open(csv_filename, 'w',newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames)
        writer.writeheader()
        for row in csv_table:
            writer.writerow(row)


    print(f"Results saved as {csv_filename}")
