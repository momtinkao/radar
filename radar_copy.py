# python3.8.0 64位（python 32位要用32位的DLL/so(Linux)）
#
from ctypes import *
from Can import VCI_CAN_OBJ, VCI_CAN_OBJ_ARRAY, VCI_INIT_CONFIG
import threading
from movie_writer import AnimatedPoint
import time
import datetime
import struct
import socket
import configparser
from utlis import *

VCI_USBCAN2 = 4
STATUS_OK = 1


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
obj_list = Object_list()


rx_vci_can_obj = VCI_CAN_OBJ_ARRAY(2500)  # 结构体数组
ubyte_3array = c_ubyte * 3


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


RADAR_STATE = 0x201
OBJECT_STATUS = 0x60a
OBJECT_GENERAL = 0x60b
OBJECT_QUALITY = 0x60c
OBJECT_EXTEND = 0x60d
FILTER_STATE_HEADER = 0x203
FILTER_STATE_CFG = 0x204


def send_object(objlist: Object_list):
    objlist.mutex.acquire()
    global points
    points = [0, 0, 'None']
    now = datetime.datetime.now()
    byte = struct.pack("!IIIfI", 1, now.hour,
                       now.minute, (float)(now.second + now.microsecond / 1000000), self.length)
    for it in objlist.object_list:
        if it != None:
            points.append((it.distlat, it.distlong, type_name[it.type]))
            byte = byte + \
                struct.pack("!ddI", it.distlat, it.distlong, it.type)
    client_socket.sendto(byte, server_address)
    objlist.mutex.release()


def filling_object(data) -> Object:
    obj = Object()
    obj.get_obj_vrelong(data)
    obj.get_obj_coordinate(data)
    obj.get_obj_ID(data)
    return obj


def update_objtype(obj_list: Object_list, data):
    obj_id = obj_id = c_ubyte(
        data[0]).value
    if obj_list.object_list[obj_id]:
        obj_list.object_list[obj_id].type = (c_ubyte(
            data[3]).value
            & 0x07)


def transmit(msg):
    ret1 = canDLL.VCI_Transmit(VCI_USBCAN2, 0, 0, byref(msg), 1)


def init(parser: configparser.ConfigParser):
    radar_cfg = Radar_Config(parser)
    filters = Filters(parser)
    b = ubyte_3array(0, 0, 0)
    vci_can_obj = VCI_CAN_OBJ(0x200, 0, 0, 1, 0, 0, 8,
                              radar_cfg.buf, b)
    radarcfg_ret = canDLL.VCI_Transmit(
        VCI_USBCAN2, 0, 0, byref(vci_can_obj), 1)
    if radarcfg_ret == STATUS_OK:
        print("Radar Cfg Transmit OK")
    for filter in filters.filters:
        flag = False
        while flag == False:
            filter_obj = VCI_CAN_OBJ(0x202, 0, 0, 1, 0, 0, 8, filter.buf, b)
            transmit(filter_obj)
            time.sleep(0.5)
            ret = canDLL.VCI_Receive(VCI_USBCAN2, 0, 0, byref(rx_vci_can_obj.ADDR),
                                     2500, 0)
            if ret > 0:
                for i in range(ret):
                    if (rx_vci_can_obj.STRUCT_ARRAY[i].ID == 0x204):
                        filter_status = FilterStatus()
                        filter_status.buffer_filling(
                            rx_vci_can_obj.STRUCT_ARRAY[i].Data)
                        if filter_status.index == filter.index:
                            filter_status.GET_FilterCfg_FilterCfg_Index()
                            filter_status.Get_FilterCfg_FilterCfg_Active()
                            filter_status.GET_FilterCfg_FilterCfg_Min_Class()
                            filter_status.GET_FilterCfg_FilterCfg_Max_Class()
                            flag = True
                    else:
                        continue


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("radar.ini")
    init(config["DEFAULT"])
    animated_point = AnimatedPoint()

    def receive():
        while True:  # 一直循环查询接收。
            ret = canDLL.VCI_Receive(VCI_USBCAN2, 0, 0, byref(rx_vci_can_obj.ADDR),
                                     2500, 0)
            if ret > 0:  # 接收到数据
                for i in range(0, ret):
                    if rx_vci_can_obj.STRUCT_ARRAY[i].ID == RADAR_STATE:
                        radar_state = Radar_State()
                        radar_state.buffer_filling(
                            rx_vci_can_obj.STRUCT_ARRAY[i].Data)
                        print("output:{}, max_distance:{}".format(
                            radar_state.RadarState_OutputTypeCfg(), radar_state.RadarState_MaxDistanceCfg()))
                    if rx_vci_can_obj.STRUCT_ARRAY[i].ID == OBJECT_STATUS:
                        for it in obj_list.object_list:
                            if it != None:
                                animated_point.add_point(
                                    it.distlat, it.distlong, type_name[it.type])
                        obj_list.length = (c_ubyte(
                            rx_vci_can_obj.STRUCT_ARRAY[i].Data[0]).value)
                    if rx_vci_can_obj.STRUCT_ARRAY[i].ID == OBJECT_GENERAL:
                        obj = filling_object(
                            rx_vci_can_obj.STRUCT_ARRAY[i].Data)
                        obj_list.insert_object(obj)
                    if rx_vci_can_obj.STRUCT_ARRAY[i].ID == OBJECT_EXTEND:
                        update_objtype(obj_list)
    r = threading.Thread(target=receive)
    r.start()
    animated_point.show()
