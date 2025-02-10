import math


def convert_local_to_geographic(reference_lat, reference_lon, lat_distance, lon_distance, angle_degrees):
    """
    Transform rotated coordinates back to the original coordinate system

    Args:
    x_new (float): x-coordinate in the rotated system
    y_new (float): y-coordinate in the rotated system
    angle_degrees (float): rotation angle in degrees

    Returns:
    tuple: (x_original, y_original)
    """
    # Convert angle to radians
    angle_radians = math.radians(angle_degrees)
    print(angle_radians)

    # Calculate original coordinates
    lon_original = lon_distance * math.cos(angle_radians) + \
        lat_distance * math.sin(angle_radians)
    lat_original = -lon_distance * math.sin(angle_radians) + \
        lat_distance * math.cos(angle_radians)
    # Earth's radius in meters
    EARTH_RADIUS = 6371000  # meters
    # Convert distances to angular changes
    # 1 degree of latitude ≈ 111,320 meters
    # 1 degree of longitude varies based on latitude
    lat_change = lat_original / (EARTH_RADIUS * (180 / math.pi))
    lon_change = lon_original / \
        ((EARTH_RADIUS * math.cos(math.radians(reference_lat))) * (180 / math.pi))
    new_latitude = reference_lat + lat_change
    new_longitude = reference_lon + lon_change
    print(new_latitude)
    return [new_latitude, new_longitude]


def calculate_destination_coordinates(lat1, lon1, east_distance, south_distance):
    """
    使用 Haversine 公式計算物體的經緯度
    :param lat1: 當前位置的緯度 (度)
    :param lon1: 當前位置的經度 (度)
    :param east_distance: 東方距離 (米)
    :param south_distance: 南方距離 (米)
    :return: 物體的緯度和經度 (度)
    """
    # 地球半徑 (米)
    R = 6371000.0

    # 將當前緯度和經度轉換為弧度
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)

    # 計算總距離和方位角
    total_distance = math.sqrt(east_distance**2 + south_distance**2)
    bearing = math.atan2(east_distance, -south_distance)  # 南方為負

    # 計算目的物的緯度和經度
    lat2_rad = math.asin(
        math.sin(lat1_rad) * math.cos(total_distance / R) +
        math.cos(lat1_rad) * math.sin(total_distance / R) * math.cos(bearing)
    )

    lon2_rad = lon1_rad + math.atan2(
        math.sin(bearing) * math.sin(total_distance / R) * math.cos(lat1_rad),
        math.cos(total_distance / R) - math.sin(lat1_rad) * math.sin(lat2_rad)
    )

    # 將弧度轉換為角度
    lat2 = math.degrees(lat2_rad)
    lon2 = math.degrees(lon2_rad)

    return lat2, lon2


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


if __name__ == "__main__":
    distance = (4.214859797496196**2 + 223.9932922140471**2) ** 0.5 / 1000
    a1, a2 = calculate_destination_coordinates2(
        22.99566312020239, 120.23714440863701, 223.9932922140471, 4.214859797496196, 89)
    print(a1, a2)
