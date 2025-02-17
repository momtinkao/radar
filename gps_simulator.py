import xml.etree.ElementTree as ET
from xml.dom import minidom
import math
import os

locations = dict()
locations2 = dict()

id = 0


def calculate_destination_coordinates2(lat1, lon1, relative_north, relative_east, bearing):
    """
    計算物體的經緯度
    :param lat1: 當前位置的緯度 (度)
    :param lon1: 當前位置的經度 (度)
    :param relative_north: 相對北方的距離 (米)
    :param relative_east: 相對東方的距離 (米)
    :param bearing: 物體相對於真實北方的方位角 (度)
    :return: 物體的緯度和經度 (度)
    """
    # 地球半徑 (米)
    R = 6371000.0

    # 將方位角轉換為弧度
    bearing_rad = math.radians(bearing)

    # 將局部座標轉換為全局座標
    true_north = relative_north * \
        math.cos(bearing_rad) - relative_east * math.sin(bearing_rad)
    true_east = relative_north * \
        math.sin(bearing_rad) + relative_east * math.cos(bearing_rad)

    # 將當前緯度轉換為弧度
    lat1_rad = math.radians(lat1)

    # 計算緯度變化
    delta_lat = true_north / R
    lat2_rad = lat1_rad + delta_lat

    # 計算經度變化
    delta_lon = true_east / (R * math.cos(lat1_rad))
    lon2_rad = math.radians(lon1) + delta_lon

    # 將弧度轉換為角度
    lat2 = math.degrees(lat2_rad)
    lon2 = math.degrees(lon2_rad)

    return lat2, lon2


obu_folder = "motor_obu"
radar_folder = "motor_radar"

obu_source = os.walk(obu_folder)
radar_source = os.walk(radar_folder)


def obu_generator(filename):
    prev_time_name = ""
    latitude = None
    longitude = None
    gpx_obu = ET.Element("gpx", version="1.1", creator="Python Script",
                         xmlns="http://www.topografix.com/GPX/1/1")
    trk_obu = ET.SubElement(gpx_obu, "trk")
    trkseg_obu = ET.SubElement(trk_obu, "trkseg")
    with open("motor_obu/"+filename, 'r') as f:
        for line in f:
            time_split = line.split()[1].split(":")
            time_name = time_split[1] + time_split[2].split(',')[0]
            if 'latitude' in line:
                latitude = float(line.split()[4])
            if 'longitude' in line:
                longitude = float(line.split()[4])
            if time_name != prev_time_name and latitude != None and longitude != None:
                locations[time_name] = (id, latitude, longitude)
                trkpt_obu = ET.SubElement(
                    trkseg_obu, "trkpt", lat=str(latitude), lon=str(longitude))
                prev_time_name = time_name
    xml_str_obu = minidom.parseString(ET.tostring(
        gpx_obu, encoding="utf-8")).toprettyxml(indent="  ")
    with open("motor_obu_gpx/"+filename+".gpx", "w", encoding="utf-8") as f:
        f.write(xml_str_obu)


def radar_generator(filename):
    prev_time_name = ""
    with open("motor_radar/"+filename) as f:
        if "south" in filename:
            coordinate = [22.995511820181395, 120.23703169670878]
            angle = 180
        elif "east" in filename:
            coordinate = [22.99565656924203, 120.2371356323031]
            angle = 90
        gpx_radar = ET.Element("gpx", version="1.1", creator="Python Script",
                               xmlns="http://www.topografix.com/GPX/1/1")
        trk_radar = ET.SubElement(gpx_radar, "trk")
        trkseg_radar = ET.SubElement(trk_radar, "trkseg")
        for line in f:
            line_split = line.split()
            time_split = line_split[1].split(":")
            time_name = time_split[1] + time_split[2].split(',')[0]
            if prev_time_name != time_name:
                prev_time_name = time_name
                lat = float(line_split[4].split(':')[1].split(',')[0])
                lon = float(line_split[3].split(':')[1].split(',')[0])
                lat, lon = calculate_destination_coordinates2(
                    coordinate[0], coordinate[1], lat, lon, angle)
                trkpt_radar = ET.SubElement(trkseg_radar, "trkpt",
                                            lat=str(lat), lon=str(lon))
        xml_str = minidom.parseString(ET.tostring(
            gpx_radar, encoding="utf-8")).toprettyxml(indent="  ")
        with open("motor_radar_gpx/"+filename+".gpx", "w", encoding="utf-8") as f:
            f.write(xml_str)


for folder, subfolders, filenames in obu_source:
    for filename in filenames:
        obu_generator(filename)

for folder, subfolders, filenames in radar_source:
    for filename in filenames:
        radar_generator(filename)
