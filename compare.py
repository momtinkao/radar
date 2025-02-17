import os

obu_folder = "motor_obu"
radar_folder = "motor_radar"

obu_source = os.walk(obu_folder)
radar_source = os.walk(radar_folder)


def compare(filename: str):
    lines_obu = dict()
    lines_radar = dict()
    radar_filename = filename.replace("obu", "radar")
    output_filename = filename.replace("_obu.log", "")
    with open(obu_folder + "/" + filename, 'r') as f:
        for line in f:
            if 'speed' in line:
                line_spilt = line.split()
                time_spilt = line_spilt[1].split(":")
                time_name = time_spilt[1] + time_spilt[2].split(',')[0]
                lines_obu[time_name] = float(line_spilt[4]) * 3.6
    prev_time_name = ""
    file_data = ""
    difference = 0
    count = 0
    with open(radar_folder+"/"+radar_filename, 'r') as f:
        for line in f:
            line_split = line.split()
            time_split = line_split[1].split(":")
            time_name = time_split[1] + time_split[2].split(',')[0]
            if prev_time_name != time_name:
                prev_time_name = time_name
                radar_speed = abs(float(line_split[5].split(':')[1]))
                if time_name in lines_obu:
                    difference += abs(lines_obu[time_name] - radar_speed)
                    count += 1
                    if abs(lines_obu[time_name] - radar_speed) < 5:
                        file_data += f"speed is similar at time {time_name}, obu speed is {lines_obu[time_name]}, radar speed is {radar_speed}\n"
                    else:
                        file_data += f"not similar at time {time_name}, obu is {lines_obu[time_name]}, radar is {radar_speed}\n"
    difference_avg = difference / count
    file_data += f"average difference is {difference_avg}km/h"
    f = open("motor_compare/"+output_filename, "w", encoding="utf-8")
    f.write(file_data)


for folder, subfolders, filenames in obu_source:
    for filename in filenames:
        compare(filename)
