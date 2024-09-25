# python3.8.0 64位（python 32位要用32位的DLL/so(Linux)）
#
from ctypes import *
import ctypes
import threading
import logging
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import datetime
import socket
import struct
path = 'obj5.log'
f = open(path, 'w')
logging.basicConfig(level=logging.DEBUG,
                    filename='objlist.log',
                    filemode='a',
                    format='%(asctime)s - %(levelname)s : %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

VCI_USBCAN2 = 4
STATUS_OK = 1


class VCI_INIT_CONFIG(Structure):
    _fields_ = [("AccCode", c_uint), ("AccMask", c_uint), ("Reserved", c_uint),
                ("Filter", c_ubyte), ("Timing0", c_ubyte),
                ("Timing1", c_ubyte), ("Mode", c_ubyte)]


class VCI_CAN_OBJ(Structure):
    _fields_ = [("ID", c_uint), ("TimeStamp", c_uint), ("TimeFlag", c_ubyte),
                ("SendType", c_ubyte), ("RemoteFlag", c_ubyte),
                ("ExternFlag", c_ubyte), ("DataLen", c_ubyte),
                ("Data", c_ubyte * 8), ("Reserved", c_ubyte * 3)]


byte_array = c_ubyte * 8
texts = []
type_name = ["point", "car", "truck", "pedestrian",
             "motor", "bicycle", "wide", "other"]
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
message = b"hello,Server"
server_address = ('172.30.114.34', 12346)
client_address = ('172.30.112.1', 10006)
client_socket.bind(client_address)
client_socket.sendto(message, server_address)


class Radar_Config:

    def __init__(self):
        self.buf = byte_array(0, 0, 0, 0, 0, 0, 0, 0)
        self.init_config()

    def init_config(self):
        self.Set_Radar_MaxDistance_vaild(1)
        self.Set_Radar_Sensor_ID_valid(0)
        self.RadarCfg_CtrlRelay(0)
        self.RadarCfg_CtrlRelay_valid(0)
        self.RadarCfg_MaxDistance(100)
        self.RadarCfg_OutputType(1)
        self.RadarCfg_RCS_Threshold_Valid(0)
        self.RadarCfg_RCS_Threshold(0)
        self.RadarCfg_StoreInNVM_valid(0)
        self.RadarCfg_StoreInNVM(0)
        self.RadarCfg_OutputType_valid(1)
        self.RadarCfg_RadarPower(0)
        self.RadarCfg_RadarPower_valid(0)
        self.RadarCfg_SendExtInfo(1)
        self.RadarCfg_SendExtInfo_valid(1)
        self.RadarCfg_SendQuality_valid(0)
        self.RadarCfg_SendQuality(0)
        self.RadarCfg_SensorID(0)
        self.RadarCfg_SortIndex(0)
        self.RadarCfg_SortIndex_valid(0)

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


# Radar_state class
class Radar_State:

    def __init__(self):
        self.buf = byte_array(0, 0, 0, 0, 0, 0, 0, 0)

    def buffer_filling(self, data):
        self.buf = data

    def RadarState_Voltage_Error(self):
        return (c_ubyte(self.buf[2]).value >> 1) & 0x01

    def RadarState_SortIndex(self):
        return (c_ubyte(self.buf[4]).value >> 4) & 0x07

    def RadarState_RCS_Threshold(self):
        return (c_ubyte(self.buf[7]).value >> 2) & 0x07

    def RadarState_SendQualityCfg(self):
        return (c_ubyte(self.buf[5]).value >> 4) & 0x01

    def RadarState_SendExtInfoCfg(self):
        return (c_ubyte(self.buf[5]).value >> 5) & 0x01

    def RadarState_MotionRxState(self):
        return (c_ubyte(self.buf[5]).value >> 6) & 0x03

    def RadarState_OutputTypeCfg(self):
        return (c_ubyte(self.buf[5]).value >> 2) & 0x03

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


class FilterCfg:

    def __init__(self):
        self.index = 0x0
        self.buf = byte_array(0, 0, 0, 0, 0, 0, 0, 0)

    def FilterCfg_FilterCfg_Min_Class(self, val):
        if self.index == 0x1:
            val = (int)(val // 0.1)
        if self.index == 0x7:
            val = (int)(val // 0.025)
        if self.index == 0xc:
            val = (int)(val // 0.0315)
        if self.index == 0xe:
            val = (int)(val // 0.0315)
        if self.index == 0x3:
            val = (int)(val // 0.0315)
        if self.index == 0x4:
            val = (int)(val // 0.0315)
        if self.index == 0x5:
            val = (int)((val + 50) // 0.025)
        self.buf[1] &= ~(0x0f)
        self.buf[1] |= (c_ubyte(c_ushort(val).value >> 8).value & 0x0f)
        self.buf[2] &= ~(0xff)
        self.buf[2] |= (c_ubyte(val).value & 0xff)

    def FilterCfg_FilterCfg_Max_Class(self, val):
        if self.index == 0x7:
            val = (int)(val // 0.025)
        if self.index == 0x1:
            val = (int)(val // 0.1)
        if self.index == 0xc:
            val = (int)(val // 0.0315)
        if self.index == 0xe:
            val = (int)(val // 0.0315)
        if self.index == 0x3:
            val = (int)(val // 0.0315)
        if self.index == 0x4:
            val = (int)(val // 0.0315)
        if self.index == 0x5:
            val = (int)((val + 50) // 0.025)
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
        self.buf = byte_array(0, 0, 0, 0, 0, 0, 0, 0)
        self.name = [
            "NonObj", "Distance", "Azimuth", "VrelOncome", "VrelDepart", "RCS",
            "Lifetime", "Size", "ProbExists", "Y", "X", "VYRightLeft",
            "VXOncome", "VYLeftRight", "VXDepart"
        ]

    def buffer_filling(self, data):
        self.buf = data

    def GET_FilterCfg_FilterCfg_Min_Class(self):
        if self.index == 0x7:
            min_size = 0.025 * (((c_ushort(self.buf[1]).value & 0x0f) << 8) |
                                (c_ubyte(self.buf[2] & 0xff).value))
            print("min size:", min_size)
        if self.index == 0x8:
            min_prob = (((c_ushort(self.buf[1]).value & 0x0f) << 8) |
                        (c_ubyte(self.buf[2] & 0xff).value))
            print(f"min prob:{min_prob}")
        if self.index == 0xc:
            min_vyrightleft = 0.0315 * ((
                (c_ushort(self.buf[1]).value & 0x0f) << 8) |
                (c_ubyte(self.buf[2] & 0xff).value))
            print(f"min voncocme:{min_vyrightleft}")
        if self.index == 0xe:
            min_vyleftright = 0.0315 * ((
                (c_ushort(self.buf[1]).value & 0x0f) << 8) |
                (c_ubyte(self.buf[2] & 0xff).value))
            print(f"min vdepart:{min_vyleftright}")
        if self.index == 0x3:
            min_come_vrel = 0.0315 * ((
                (c_ushort(self.buf[1]).value & 0x0f) << 8) |
                (c_ubyte(self.buf[2]).value & 0xff))
            print("min come_vrel:", min_come_vrel)
        if self.index == 0x5:
            min_RCS = 0.025 * ((
                (c_ushort(self.buf[1]).value & 0x0f) << 8) |
                (c_ubyte(self.buf[2]).value & 0xff)) - 50
            print("min RCS:", min_RCS)

    def GET_FilterCfg_FilterCfg_Max_Class(self):
        if self.index == 0x7:
            max_size = 0.025 * (((c_ushort(self.buf[3]).value & 0x0f) << 8) |
                                (c_ubyte(self.buf[4]).value & 0xff))
            print("max Size:", max_size)
        if self.index == 0x8:
            max_prob = (((c_ushort(self.buf[3]).value & 0x0f) << 8) |
                        (c_ubyte(self.buf[4] & 0xff).value))
            print(f"min prob:{max_prob}")
        if self.index == 0xc:
            max_vyrightleft = 0.0315 * ((
                (c_ushort(self.buf[3]).value & 0x0f) << 8) |
                (c_ubyte(self.buf[4]).value & 0xff))
            print("max voncome:", max_vyrightleft)
        if self.index == 0xe:
            max_vyleftright = 0.0315 * ((
                (c_ushort(self.buf[3]).value & 0x0f) << 8) |
                (c_ubyte(self.buf[4]).value & 0xff))
            print("max vdepart:", max_vyleftright)
        if self.index == 0x3:
            max_come_vrel = 0.0315 * ((
                (c_ushort(self.buf[3]).value & 0x0f) << 8) |
                (c_ubyte(self.buf[4]).value & 0xff))
            print("max come_vrel:", max_come_vrel)
        if self.index == 0x4:
            max_dep_vrel = 0.0315 * ((
                (c_ushort(self.buf[3]).value & 0x0f) << 8) |
                (c_ubyte(self.buf[4]).value & 0xff))
            print("max dep_vrel:", max_dep_vrel)
        if self.index == 0x5:
            max_RCS = 0.025 * ((
                (c_ushort(self.buf[3]).value & 0x0f) << 8) |
                (c_ubyte(self.buf[4]).value & 0xff)) - 50
            print("max RCS:", max_RCS)

    def GET_FilterCfg_FilterCfg_Index(self):
        self.index = (c_ubyte(self.buf[0]).value >> 3) & 0x0f
        print("index: ", self.index)

    def Get_FilterCfg_FilterCfg_Active(self):
        active = (c_ubyte(self.buf[0]).value >> 2) & 0x01
        if active == 1:
            print(f"{self.name[self.index]} active")
        else:
            print(f"{self.name[self.index]} unactive")


points = [(0, 0, 'a')]


class Object_list:

    def __init__(self):
        self.mutex = threading.Lock()
        self.length = 0
        self.object_list = [None] * 256

    def clear_list(self):
        self.object_list = [None] * 256
        logging.info("clear-----")

    def insert_object(self, obj):
        self.mutex.acquire()
        self.object_list[obj.id] = obj
        self.mutex.release()

    def print_object(self):
        self.mutex.acquire()
        global points
        points = [(0, 0, 'None')]
        now = datetime.datetime.now()
        byte = struct.pack("!IIIfI", 1, now.hour,
                           now.minute, (float)(now.second + now.microsecond / 1000000), self.length)
        for it in self.object_list:
            if it != None:
                points.append((it.distlat, it.distlong, type_name[it.type]))
                byte = byte + \
                    struct.pack("!ddI", it.distlat, it.distlong, it.type)
        client_socket.sendto(byte, server_address)
        self.mutex.release()


class Object:

    def __init__(self):
        self.id = 0
        self.distlong = 1000
        self.distlat = 1000
        self.vrelong = 1000
        self.type = None
        self.state = 6

    def get_obj_ID(self, buf):
        self.id = (c_ubyte(buf[0]).value) & 0xff

    def get_obj_distlong(self, buf):
        self.distlong = (((c_ushort(buf[1]).value & 0xff) << 5) |
                         ((c_ubyte(buf[2]).value >> 3) & 0x1f)) * 0.2 - 500

    def get_obj_distlat(self, buf):
        self.distlat = (((c_ushort(buf[2]).value & 0x07) << 8) |
                        ((c_ubyte(buf[3]).value >> 0) & 0xff)) * 0.2 - 209.6

    def get_obj_vrelong(self, buf):
        self.vrelong = (((((c_ushort(buf[4]).value & 0xff) << 8) |
                        ((c_ubyte(buf[5]).value >> 6) & 0x03)) * 0.25 - 128) * 3.6)


def get_filterNums(buf):
    return (c_ubyte(buf[1]).value >> 3)


fig, ax = plt.subplots()

scat = ax.scatter([], [], s=100)


def init():
    ax.set_xlim(-30, 30)
    ax.set_ylim(0, 260)
    for text in texts:
        text.remove()
    texts.clear()
    return scat,


def update(frame):
    global points
    x, y, vrels = zip(*points)

    # 更新散點圖的位置
    scat.set_offsets(list(zip(x, y)))

    # 清除舊的文字標籤
    for text in texts:
        text.remove()
    texts.clear()

    # 添加新的文字標籤
    for (xi, yi, vrel) in zip(x, y, vrels):
        text = ax.text(xi, yi, f'{vrel}', fontsize=12, ha='right', va='bottom')
        texts.append(text)

    return scat, *texts


# CanDLLName = './ControlCAN.dll' #把DLL放到对应的目录下
CanDLLName = './ControlCAN.dll'  # 把SO放到对应的目录下,LINUX
# canDLL = windll.LoadLibrary('./ControlCAN.dll')
# Linux系统下使用下面语句，编译命令：python3 python3.8.0.py
canDLL = windll.LoadLibrary('./ControlCan.dll')

print(CanDLLName)

ret = canDLL.VCI_OpenDevice(VCI_USBCAN2, 0, 0)
if ret == STATUS_OK:
    print('调用 VCI_OpenDevice成功\r\n')
if ret != STATUS_OK:
    print('调用 VCI_OpenDevice出错\r\n')

# 初始0通道
vci_initconfig = VCI_INIT_CONFIG(0x80000008, 0xFFFFFFFF, 0, 0, 0x00, 0x1C,
                                 0)  # 波特率500k，正常模式
ret = canDLL.VCI_InitCAN(VCI_USBCAN2, 0, 0, byref(vci_initconfig))
if ret == STATUS_OK:
    print('调用 VCI_InitCAN1成功\r\n')
if ret != STATUS_OK:
    print('调用 VCI_InitCAN1出错\r\n')

ret = canDLL.VCI_StartCAN(VCI_USBCAN2, 0, 0)
if ret == STATUS_OK:
    print('调用 VCI_StartCAN1成功\r\n')
if ret != STATUS_OK:
    print('调用 VCI_StartCAN1出错\r\n')


class VCI_CAN_OBJ_ARRAY(Structure):
    _fields_ = [('SIZE', ctypes.c_uint16),
                ('STRUCT_ARRAY', ctypes.POINTER(VCI_CAN_OBJ))]

    def __init__(self, num_of_structs):
        # 这个括号不能少
        self.STRUCT_ARRAY = ctypes.cast((VCI_CAN_OBJ * num_of_structs)(),
                                        ctypes.POINTER(VCI_CAN_OBJ))  # 结构体数组
        self.SIZE = num_of_structs  # 结构体长度
        self.ADDR = self.STRUCT_ARRAY[0]  # 结构体数组地址  byref()转c地址


rx_vci_can_obj = VCI_CAN_OBJ_ARRAY(2500)  # 结构体数组

obj_list = Object_list()


def receive():
    global prev
    global lock
    idx = 1
    while 1:  # 一直循环查询接收。
        ret = canDLL.VCI_Receive(VCI_USBCAN2, 0, 0, byref(rx_vci_can_obj.ADDR),
                                 2500, 0)
        if ret > 0:  # 接收到数据
            for i in range(0, ret):
                '''
                if rx_vci_can_obj.STRUCT_ARRAY[i].ID == 0x201:
                    radar_status = Radar_State()
                    radar_status.buffer_filling(
                        rx_vci_can_obj.STRUCT_ARRAY[i].Data)
                    print(
                        f"radar max distance:{radar_status.RadarState_MaxDistanceCfg()}"
                    )
                '''
                if rx_vci_can_obj.STRUCT_ARRAY[i].ID == 0x201:
                    byte = bytearray(rx_vci_can_obj.STRUCT_ARRAY[i].Data)
                    f.write(
                        f"({format(time.time(),'.6f')}) can0 201#{byte.hex()}\n")
                if rx_vci_can_obj.STRUCT_ARRAY[i].ID == 0x60a:
                    obj_list.length = (c_ubyte(
                        rx_vci_can_obj.STRUCT_ARRAY[i].Data[0]).value)
                    meas_counter = (c_ushort(
                        rx_vci_can_obj.STRUCT_ARRAY[i].Data[1]).value << 8) | (
                            c_ubyte(
                                rx_vci_can_obj.STRUCT_ARRAY[i].Data[2]).value)
                    byte = bytearray(rx_vci_can_obj.STRUCT_ARRAY[i].Data[0:4])
                    f.write(
                        f"({format(time.time(),'.6f')}) can0 60A#{byte.hex()}\n")
                    obj_list.print_object()
                    obj_list.clear_list()
                if rx_vci_can_obj.STRUCT_ARRAY[i].ID == 0x60b:
                    obj = Object()
                    obj.get_obj_ID(rx_vci_can_obj.STRUCT_ARRAY[i].Data)
                    obj.get_obj_distlat(rx_vci_can_obj.STRUCT_ARRAY[i].Data)
                    obj.get_obj_distlong(rx_vci_can_obj.STRUCT_ARRAY[i].Data)
                    obj.get_obj_vrelong(rx_vci_can_obj.STRUCT_ARRAY[i].Data)
                    obj_list.insert_object(obj)
                    byte = bytearray(rx_vci_can_obj.STRUCT_ARRAY[i].Data)
                    f.write(
                        f"({format(time.time(),'.6f')}) can0 60B#{byte.hex()}\n")
                if rx_vci_can_obj.STRUCT_ARRAY[i].ID == 0x60c:
                    obj_id = obj_id = c_ubyte(
                        rx_vci_can_obj.STRUCT_ARRAY[i].Data[0]).value
                    state = (
                        c_ubyte(rx_vci_can_obj.STRUCT_ARRAY[i].Data[6]).value
                        >> 2) & 0x07
                    if obj_list.object_list[obj_id] != None:
                        obj_list.object_list[obj_id].state = state
                    byte = bytearray(rx_vci_can_obj.STRUCT_ARRAY[i].Data[0:7])
                    f.write(
                        f"({format(time.time(),'.6f')}) can0 60C#{byte.hex()}\n")
                if rx_vci_can_obj.STRUCT_ARRAY[i].ID == 0x60D:
                    obj_id = c_ubyte(
                        rx_vci_can_obj.STRUCT_ARRAY[i].Data[0]).value
                    if obj_list.object_list[obj_id] != None:
                        obj_list.object_list[obj_id].type = (c_ubyte(
                            rx_vci_can_obj.STRUCT_ARRAY[i].Data[3]).value
                            & 0x07)
                    byte = bytearray(rx_vci_can_obj.STRUCT_ARRAY[i].Data)
                    f.write(
                        f"({format(time.time(),'.6f')}) can0 60D#{byte.hex()}\n")
                if rx_vci_can_obj.STRUCT_ARRAY[i].ID == 0x203:
                    filter_nums = get_filterNums(
                        rx_vci_can_obj.STRUCT_ARRAY[i].Data)
                    print("filter_nums:", filter_nums)
                if (rx_vci_can_obj.STRUCT_ARRAY[i].ID == 0x204 and idx <= 13):
                    filter_status.buffer_filling(
                        rx_vci_can_obj.STRUCT_ARRAY[i].Data)
                    filter_status.GET_FilterCfg_FilterCfg_Index()
                    filter_status.GET_FilterCfg_FilterCfg_Min_Class()
                    filter_status.GET_FilterCfg_FilterCfg_Max_Class()
                    filter_status.Get_FilterCfg_FilterCfg_Active()
                    filter_config = FilterCfg()
                    filter_config.FilterCfg_FilterCfg_Index(idx)
                    idx += 1
                    filter_config.FilterCfg_FilterCfg_Type(1)
                    filter_config.FilterCfg_FilterCfg_Min_Class(0)
                    filter_config.FilterCfg_FilterCfg_Max_Class(0)
                    filter_config.FilterCfg_FilterCfg_Valid(0)
                    filter_config.FilterCfg_FilterCfg_Active(0)
                    filter_object = VCI_CAN_OBJ(
                        0x202, 0, 0, 1, 0, 0, 8, filter_config.buf, b)

                    t = threading.Thread(target=transmit,args=(filter_object,))
                    t.start()
                    t.join()


lock = threading.Lock()


def transmit(msg):
    global lockl
    lock.acquire()
    ret1 = canDLL.VCI_Transmit(VCI_USBCAN2, 0, 0, byref(msg), 1)
    lock.release()


r = threading.Thread(target=receive)
r.start()

# size Filter
filter_status = FilterStatus()
filter_config_size = FilterCfg()
filter_config_size.FilterCfg_FilterCfg_Index(0xc)
filter_config_size.FilterCfg_FilterCfg_Type(1)
filter_config_size.FilterCfg_FilterCfg_Min_Class(3)
filter_config_size.FilterCfg_FilterCfg_Max_Class(30)
filter_config_size.FilterCfg_FilterCfg_Valid(1)
filter_config_size.FilterCfg_FilterCfg_Active(1)

# 信賴率filter
filter_config_dist = FilterCfg()
filter_config_dist.FilterCfg_FilterCfg_Index(0x8)
filter_config_dist.FilterCfg_FilterCfg_Type(1)
filter_config_dist.FilterCfg_FilterCfg_Min_Class(3)
filter_config_dist.FilterCfg_FilterCfg_Max_Class(7)
filter_config_dist.FilterCfg_FilterCfg_Valid(1)
filter_config_dist.FilterCfg_FilterCfg_Active(0)

config = Radar_Config()

ubyte_3array = c_ubyte * 3
b = ubyte_3array(0, 0, 0)
vci_can_obj = VCI_CAN_OBJ(0x200, 0, 0, 1, 0, 0, 8, config.buf, b)  # 单次发送
vci_can_obj2 = VCI_CAN_OBJ(0x202, 0, 0, 1, 0, 0, 8, filter_config_size.buf, b)
vci_can_obj3 = VCI_CAN_OBJ(0x202, 0, 0, 1, 0, 0, 8, filter_config_dist.buf, b)
ret = canDLL.VCI_Transmit(VCI_USBCAN2, 0, 0, byref(vci_can_obj), 1)

if ret == STATUS_OK:
    print('CAN1通道发送成功\r\n')
    ret2 = canDLL.VCI_Transmit(VCI_USBCAN2, 0, 0, byref(vci_can_obj2), 1)
'''
if ret2 == STATUS_OK:
    print("Filter1 OK")
    ret = canDLL.VCI_Transmit(VCI_USBCAN2,0,0,byref(vci_can_obj3),1)
if ret == STATUS_OK:
    print("Filter2 OK\r\n")
'''
ani = animation.FuncAnimation(fig, update, init_func=init, interval=75)

plt.show()
