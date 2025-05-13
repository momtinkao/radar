import math
from ctypes import *
import configparser
import threading

FILTER_NOFOBJ = 0x0
FILTER_DISTANCE = 0x1
FILTER_AZIMUTH = 0x2
FILTER_VRELONCOME = 0x3
FILTER_VRELDEPART = 0x4
FILTER_RCS = 0x5
FILTER_LIFETIME = 0x6
FILTER_SIZE = 0x7
FILTER_PROBEXISTS = 0x8
FILTER_Y = 0x9
FILTER_X = 0xa
FILTER_VYRIGHTLEFT = 0xb
FILTER_VXONCOME = 0xc
FILTER_VYLEFTRIGHT = 0xd
FILTER_VXDEPART = 0xe


class Radar_Config:
    byte_array = c_ubyte * 8

    def __init__(self, config_file):
        self.byte_array = c_ubyte * 8
        self.buf = self.byte_array(0, 0, 0, 0, 0, 0, 0, 0)
        self.cfg = config_file
        self.init_config(config_file=self.cfg)

    def init_config(self, config_file):
        self.Set_Radar_MaxDistance_vaild(int(config_file["MaxDistance_Valid"]))
        self.Set_Radar_Sensor_ID_valid(
            int(config_file["Sensor_ID_Valid"]))
        self.RadarCfg_CtrlRelay(int(config_file["CtrlRelay_Valid"]))
        self.RadarCfg_CtrlRelay_valid(int(config_file["CtrlRelay_Valid"]))
        self.RadarCfg_MaxDistance(int(config_file["MaxDistance"]))
        self.RadarCfg_OutputType(int(config_file["OutputType"]))
        self.RadarCfg_RCS_Threshold_Valid(
            int(config_file["RCS_Threshold_Valid"]))
        self.RadarCfg_RCS_Threshold(int(config_file["RCS_Threshold"]))
        self.RadarCfg_StoreInNVM_valid(int(config_file["StoreInNVM_Valid"]))
        self.RadarCfg_StoreInNVM(int(config_file["StoreInNVM"]))
        self.RadarCfg_OutputType_valid(int(config_file["OutputType_Valid"]))
        self.RadarCfg_RadarPower(int(config_file["RadarPower"]))
        self.RadarCfg_RadarPower_valid(int(config_file["RadarPower_Valid"]))
        self.RadarCfg_SendExtInfo(int(config_file["SendExtInfo"]))
        self.RadarCfg_SendExtInfo_valid(int(config_file["SendExtInfo_Valid"]))
        self.RadarCfg_SendQuality_valid(int(config_file["SendQuality_Valid"]))
        self.RadarCfg_SendQuality(int(config_file["SendQuality"]))
        self.RadarCfg_SensorID(int(config_file["Sensor_ID"]))
        self.RadarCfg_SortIndex(int(config_file["SortIndex"]))
        self.RadarCfg_SortIndex_valid(int(config_file["SortIndex_Valid"]))

    def Set_Radar_MaxDistance_vaild(self, val):
        self.buf[0] &= ~(0x01 << 0)
        self.buf[0] |= (c_ubyte(val).value) & 0x01

    def Set_Radar_Sensor_ID_valid(self, val):
        self.buf[0] &= ~(0x01 << 1)
        self.buf[0] |= (c_ubyte(val).value) & 0x01

    def RadarCfg_RCS_Threshold_Valid(self, val):
        self.buf[6] &= ~(0x01 << 0)
        self.buf[6] |= (c_ubyte(val).value) & 0x01

    def RadarCfg_RCS_Threshold(self, val):
        self.buf[6] &= ~(0x07 << 1)
        self.buf[6] |= (c_ubyte(val).value & 0x07) << 1

    def RadarCfg_StoreInNVM_valid(self, val):
        self.buf[0] &= ~(0x01 << 7)
        self.buf[0] |= (c_ubyte(val).value & 0x01) << 7

    def RadarCfg_SortIndex_valid(self, val):
        self.buf[0] &= ~(0x01 << 6)
        self.buf[0] |= (c_ubyte(val).value & 0x01) << 6

    def RadarCfg_SortIndex(self, val):
        self.buf[5] &= ~(0x07 << 4)
        self.buf[5] |= (c_ubyte(val).value & 0x07) << 4

    def RadarCfg_StoreInNVM(self, val):
        self.buf[5] &= ~(0x01 << 7)
        self.buf[5] |= (c_ubyte(val).value & 0x01) << 7

    def RadarCfg_SendExtInfo_valid(self, val):
        self.buf[0] &= ~(0x01 << 5)
        self.buf[0] |= (c_ubyte(val).value & 0x01) << 5

    def RadarCfg_SendExtInfo(self, val):
        self.buf[5] &= ~(0x01 << 3)
        self.buf[5] |= (c_ubyte(val).value & 0x01) << 3

    def RadarCfg_CtrlRelay_valid(self, val):
        self.buf[5] &= ~(0x01 << 0)
        self.buf[5] |= (c_ubyte(val).value & 0x01) << 0

    def RadarCfg_CtrlRelay(self, val):
        self.buf[5] &= ~(0x01 << 1)
        self.buf[5] |= (c_ubyte(val).value & 0x01) << 1

    def RadarCfg_SendQuality_valid(self, val):
        self.buf[0] &= ~(0x01 << 4)
        self.buf[0] |= (c_ubyte(val).value & 0x01) << 4

    def RadarCfg_SendQuality(self, val):
        self.buf[5] &= ~(0x01 << 2)
        self.buf[5] |= (c_ubyte(val).value & 0x01) << 2

    def RadarCfg_RadarPower_valid(self, val):
        self.buf[0] &= ~(0x01 << 2)
        self.buf[0] |= (c_ubyte(val).value & 0x01) << 2

    def RadarCfg_OutputType_valid(self, val):
        self.buf[0] &= ~(0x01 << 3)
        self.buf[0] |= (c_ubyte(val).value & 0x01) << 3

    def RadarCfg_MaxDistance(self, val):
        val = int(val // 2)
        self.buf[1] &= ~(0xff << 0)
        self.buf[1] |= ((c_ubyte(c_ushort(val).value >> 2).value) & 0xff)
        self.buf[2] &= ~(0x03 << 6)
        self.buf[2] |= (c_ubyte(val).value & 0x03) << 6

    def RadarCfg_RadarPower(self, val):
        self.buf[4] &= ~(0x07 << 5)
        self.buf[4] |= (c_ubyte(val).value & 0x07) << 5

    def RadarCfg_OutputType(self, val):
        self.buf[4] &= ~(0x03 << 3)
        self.buf[4] |= (c_ubyte(val).value & 0x03) << 3

    def RadarCfg_SensorID(self, val):
        self.buf[4] &= ~(0x07 << 0)
        self.buf[4] |= (c_ubyte(val).value & 0x07) << 0


class Radar_State:

    def __init__(self):
        self.byte_array = c_ubyte*8
        self.buf = self.byte_array(0, 0, 0, 0, 0, 0, 0, 0)

    def buffer_filling(self, data):
        self.buf = data

    # 回傳Voltage_Error
    def RadarState_Voltage_Error(self):
        return (c_ubyte(self.buf[2]).value >> 1) & 0x01
    # 回傳Sort方式

    def RadarState_SortIndex(self):
        return (c_ubyte(self.buf[4]).value >> 4) & 0x07
    # 回傳雷達截射面積的閥值

    def RadarState_RCS_Threshold(self):
        return (c_ubyte(self.buf[7]).value >> 2) & 0x07
    # 回傳是否有開啟傳送Quality

    def RadarState_SendQualityCfg(self):
        return (c_ubyte(self.buf[5]).value >> 4) & 0x01
    # 回傳是否有開啟額外雷達資訊的傳送

    def RadarState_SendExtInfoCfg(self):
        return (c_ubyte(self.buf[5]).value >> 5) & 0x01

    def RadarState_MotionRxState(self):
        return (c_ubyte(self.buf[5]).value >> 6) & 0x03

    # 回傳雷達是object模式或是cluster模式
    def RadarState_OutputTypeCfg(self):
        return (c_ubyte(self.buf[5]).value >> 2) & 0x03
    # 回傳雷達電源相關資訊

    def RadarState_RadarPowerCfg(self):
        return ((c_ubyte(self.buf[3]).value) & 0x03) << 1 | (
            (c_ubyte(self.buf[4]).value >> 7) & 0x01)

    def RadarState_NVMReadStatus(self):
        return (c_ubyte(self.buf[0]).value >> 6) & 0x01

    def RadarState_MaxDistanceCfg(self):
        return 2 * (((c_ushort(self.buf[1]).value & 0xff) << 2) |
                    ((c_ubyte(self.buf[2]).value >> 6) & 0x03))

    def RadarState_ExtendedRange(self):
        return (c_ubyte(self.buf[3]).value >> 1) & 0x01


class Filters:
    def __init__(self, config_file):
        self.filters = []
        self.names = [
            "Filter_NonObj", "Filter_Distance", "Filter_Azimuth", "Filter_VrelOncome", "Filter_VrelDepart", "Filter_RCS",
            "Filter_Lifetime", "Filter_Size", "Filter_ProbExists", "Filter_Y", "Filter_X", "Filter_VYRightLeft",
            "Filter_VXOncome", "Filter_VYLeftRight", "Filter_VXDepart"
        ]
        cfg = config_file
        self.init_filters(cfg)

    def init_filters(self, config_file: configparser.SectionProxy):
        for i, name in enumerate(self.names):
            if (config_file.getboolean(name+"_Valid")):
                filter = FilterCfg()
                filter.FilterCfg_FilterCfg_Index(i)
                filter.FilterCfg_FilterCfg_Valid(1)
                filter.FilterCfg_FilterCfg_Active(1)
                filter.FilterCfg_FilterCfg_Min_Class(
                    float(config_file[name+"_Min"]))
                filter.FilterCfg_FilterCfg_Max_Class(
                    float(config_file[name+"_Max"]))
                filter.FilterCfg_FilterCfg_Type(int(config_file["OutputType"]))
                self.filters.append(filter)
            else:
                filter = FilterCfg()
                filter.FilterCfg_FilterCfg_Index(i)
                filter.FilterCfg_FilterCfg_Valid(1)
                filter.FilterCfg_FilterCfg_Active(0)
                filter.FilterCfg_FilterCfg_Type(int(config_file["OutputType"]))
                self.filters.append(filter)


class FilterCfg:

    def __init__(self):
        self.byte_array = c_ubyte * 8
        self.index = 0x0
        self.buf = self.byte_array(0, 0, 0, 0, 0, 0, 0, 0)

    def FilterCfg_FilterCfg_Min_Class(self, val):
        if self.index == FILTER_SIZE:
            val = (int)(val // 0.025)
        if self.index == FILTER_DISTANCE:
            val = (int)(val // 0.1)
        if self.index == FILTER_VXONCOME:
            val = (val * 1000) / 3600
            val = (int)(val // 0.0315)
        if self.index == FILTER_VXDEPART:
            val = (val * 1000 / 3600)
            val = (int)(val // 0.0315)
        if self.index == FILTER_VRELONCOME:
            val = (val * 1000) / 3600
            val = (int)(val // 0.0315)
        if self.index == FILTER_VRELDEPART:
            val = (val * 1000) / 3600
            val = (int)(val // 0.0315)
        if self.index == FILTER_RCS:
            val = (int)((val + 50) // 0.025)
        else:
            val = (int)(val)
        self.buf[1] &= ~(0x0f)
        self.buf[1] |= (c_ubyte(c_ushort(val).value >> 8).value & 0x0f)
        self.buf[2] &= ~(0xff)
        self.buf[2] |= (c_ubyte(val).value & 0xff)

    def FilterCfg_FilterCfg_Max_Class(self, val):
        if self.index == FILTER_SIZE:
            val = (int)(val // 0.025)
        if self.index == FILTER_DISTANCE:
            val = (int)(val // 0.1)
        if self.index == FILTER_VXONCOME:
            val = (val * 1000) / 3600
            val = (int)(val // 0.0315)
        if self.index == FILTER_VXDEPART:
            val = (val * 1000 / 3600)
            val = (int)(val // 0.0315)
        if self.index == FILTER_VRELONCOME:
            val = (val * 1000) / 3600
            val = (int)(val // 0.0315)
        if self.index == FILTER_VRELDEPART:
            val = (val * 1000) / 3600
            val = (int)(val // 0.0315)
        if self.index == FILTER_RCS:
            val = (int)((val + 50) // 0.025)
        else:
            val = (int)(val)
        self.buf[3] &= ~(0x0f)
        self.buf[3] |= (c_ubyte(c_ushort(val).value >> 8).value & 0x0f)
        self.buf[4] &= ~(0xff)
        self.buf[4] |= (c_ubyte(val).value & 0xff)

    def FilterCfg_FilterCfg_Min_X(self, val):
        self.buf[1] &= ~(0x1f)
        self.buf[1] |= (c_ubyte(c_ushort(val).value >> 8).value & 0x1f)
        self.buf[2] &= ~(0xff)
        self.buf[2] |= (c_ubyte(val).value & 0xff)

    def FilterCfg_FilterCfg_Max_X(self, val):
        self.buf[3] &= ~(0x1f)
        self.buf[3] |= (c_ubyte(c_ushort(val).value >> 8).value & 0x1f)
        self.buf[3] &= ~(0xff)
        self.buf[3] |= (c_ubyte(val).value & 0xff)

    def FilterCfg_FilterCfg_Index(self, val):
        self.index = val
        self.buf[0] &= ~(0x0f << 3)
        self.buf[0] |= ((c_ubyte(val).value & 0x0f) << 3)

    def FilterCfg_FilterCfg_Type(self, val):
        self.buf[0] &= ~(0x01 << 7)
        self.buf[0] |= ((c_ubyte(val).value & 0x01) << 7)

    def FilterCfg_FilterCfg_Valid(self, val):
        self.buf[0] &= ~(0x01 << 1)
        self.buf[0] |= ((c_ubyte(val).value & 0x01) << 1)

    def FilterCfg_FilterCfg_Active(self, val):
        self.buf[0] &= ~(0x01 << 2)
        self.buf[0] |= ((c_ubyte(val).value & 0x01) << 2)


class FilterStatus:

    def __init__(self):
        self.index = 0x0
        self.byte_array = c_ubyte*8
        self.buf = self.byte_array(0, 0, 0, 0, 0, 0, 0, 0)
        self.name = [
            "NonObj", "Distance", "Azimuth", "VrelOncome", "VrelDepart", "RCS",
            "Lifetime", "Size", "ProbExists", "Y", "X", "VYRightLeft",
            "VXOncome", "VYLeftRight", "VXDepart"
        ]

    def buffer_filling(self, data):
        self.buf = data
        self.index = (c_ubyte(self.buf[0]).value >> 3) & 0x0f

    def GET_FilterCfg_FilterCfg_Min_Class(self):
        if self.index == FILTER_SIZE:
            min_size = 0.025 * (((c_ushort(self.buf[1]).value & 0x0f) << 8) |
                                (c_ubyte(self.buf[2] & 0xff).value))
            print("min size:", min_size)
        if self.index == FILTER_PROBEXISTS:
            min_prob = (((c_ushort(self.buf[1]).value & 0x0f) << 8) |
                        (c_ubyte(self.buf[2] & 0xff).value))
            print(f"min prob:{min_prob}")
        if self.index == FILTER_VXONCOME:
            min_vyrightleft = 0.0315 * ((
                (c_ushort(self.buf[1]).value & 0x0f) << 8) |
                (c_ubyte(self.buf[2] & 0xff).value)) * 3.6
            print(f"min voncocme:{min_vyrightleft}")
        if self.index == FILTER_VXDEPART:
            min_vyleftright = 0.0315 * ((
                (c_ushort(self.buf[1]).value & 0x0f) << 8) |
                (c_ubyte(self.buf[2] & 0xff).value)) * 3.6
            print(f"min vdepart:{min_vyleftright}")
        if self.index == FILTER_VRELONCOME:
            min_come_vrel = 0.0315 * ((
                (c_ushort(self.buf[1]).value & 0x0f) << 8) |
                (c_ubyte(self.buf[2]).value & 0xff)) * 3.6
            print("min come_vrel:", min_come_vrel)
        if self.index == FILTER_RCS:
            min_RCS = 0.025 * ((
                (c_ushort(self.buf[1]).value & 0x0f) << 8) |
                (c_ubyte(self.buf[2]).value & 0xff)) - 50
            print("min RCS:", min_RCS)

    def GET_FilterCfg_FilterCfg_Max_Class(self):
        if self.index == FILTER_SIZE:
            max_size = 0.025 * (((c_ushort(self.buf[3]).value & 0x0f) << 8) |
                                (c_ubyte(self.buf[4]).value & 0xff))
            print("max Size:", max_size)
        if self.index == FILTER_PROBEXISTS:
            max_prob = (((c_ushort(self.buf[3]).value & 0x0f) << 8) |
                        (c_ubyte(self.buf[4] & 0xff).value))
            print(f"min prob:{max_prob}")
        if self.index == FILTER_VXONCOME:
            max_vyrightleft = 0.0315 * ((
                (c_ushort(self.buf[3]).value & 0x0f) << 8) |
                (c_ubyte(self.buf[4]).value & 0xff)) * 3.6
            print("max voncome:", max_vyrightleft)
        if self.index == FILTER_VXDEPART:
            max_vyleftright = 0.0315 * ((
                (c_ushort(self.buf[3]).value & 0x0f) << 8) |
                (c_ubyte(self.buf[4]).value & 0xff)) * 3.6
            print("max vdepart:", max_vyleftright)
        if self.index == FILTER_VRELONCOME:
            max_come_vrel = 0.0315 * ((
                (c_ushort(self.buf[3]).value & 0x0f) << 8) |
                (c_ubyte(self.buf[4]).value & 0xff)) * 3.6
            print("max come_vrel:", max_come_vrel)
        if self.index == FILTER_VRELDEPART:
            max_dep_vrel = 0.0315 * ((
                (c_ushort(self.buf[3]).value & 0x0f) << 8) |
                (c_ubyte(self.buf[4]).value & 0xff)) * 3.6
            print("max dep_vrel:", max_dep_vrel)
        if self.index == FILTER_RCS:
            max_RCS = 0.025 * ((
                (c_ushort(self.buf[3]).value & 0x0f) << 8) |
                (c_ubyte(self.buf[4]).value & 0xff)) - 50
            print("max RCS:", max_RCS)

    def GET_FilterCfg_FilterCfg_Index(self):
        print("index: ", self.index)

    def Get_FilterCfg_FilterCfg_Active(self):
        active = (c_ubyte(self.buf[0]).value >> 2) & 0x01
        if active == 1:
            print(f"{self.name[self.index]} active")
        else:
            print(f"{self.name[self.index]} unactive")


class Object:

    def __init__(self, location = [22.99550506233693, 120.23706082899179]):
        self.loc = location
        self.id = 0
        self.geo = [1000, 1000]
        self.distance = [0, 0]
        self.vrelong = 0
        self.type = None
        self.rcs = 0
        self.state = 6
   
    def get_RCS(self,buf):
        self.rcs = (c_ubyte(buf[7]).value) * 0.5 - 64

    def get_obj_ID(self, buf):
        self.id = (c_ubyte(buf[0]).value) & 0xff

    def get_obj_coordinate(self, buf):
        lat_distance = (((c_ushort(buf[1]).value & 0xff) << 5) |
                        ((c_ubyte(buf[2]).value >> 3) & 0x1f)) * 0.2 - 500
        lon_distance = (((c_ushort(buf[2]).value & 0x07) << 8) |
                        ((c_ubyte(buf[3]).value >> 0) & 0xff)) * 0.2 - 204.6
        self.geo[:] = calculate_destination_coordinates2(self.loc[0], self.loc[1],
                                                  lat_distance, lon_distance, 179)

    def get_distance(self, buf):
        distlong = (((c_ushort(buf[1]).value & 0xff) << 5) |
                    ((c_ubyte(buf[2]).value >> 3) & 0x1f)) * 0.2 - 500
        distlat = (((c_ushort(buf[2]).value & 0x07) << 8) |
                   ((c_ubyte(buf[3]).value >> 0) & 0xff)) * 0.2 - 204.6
        ori_distlat, ori_distlong = rotate_corrdinate(distlong,distlat,5)
        #self.distance[:] = [ori_distlat, ori_distlong]
        self.distance[:] = [distlat,distlong]

    def get_obj_vrelong(self, buf):
        self.vrelong = ((((c_ushort(buf[4]).value & 0xff) << 2) |
                        ((c_ubyte(buf[5]).value >> 6) & 0x03)) * 0.25 - 128) * 3.6


class Object_list:

    def __init__(self):
        self.mutex = threading.Lock()
        self.length = 0
        self.object_list = [None] * 256

    def clear_list(self):
        self.object_list = [None] * 256

    def insert_object(self, obj):
        self.mutex.acquire()
        self.object_list[obj.id] = obj
        self.mutex.release()


def rotate_corrdinate(distlong,distlat,angle_degrees):
    angle_radians = math.radians(angle_degrees)
    ori_distlat = distlat * math.cos(angle_radians) + distlong * math.sin(angle_radians)
    ori_distlong = -distlat * math.sin(angle_radians) + distlong * math.cos(angle_radians)
    return ori_distlat, ori_distlong


def calculate_destination_coordinates2(
    lat1, lon1, relative_north, relative_east, bearing
):
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
    true_north = relative_north * math.cos(bearing_rad) - relative_east * math.sin(
        bearing_rad
    )
    true_east = relative_north * math.sin(bearing_rad) + relative_east * math.cos(
        bearing_rad
    )

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

    return [lat2, lon2]
