
#python3.8.0 64位（python 32位要用32位的DLL/so(Linux)）
#
from ctypes import *
 
VCI_USBCAN2 = 4
STATUS_OK = 1
class VCI_INIT_CONFIG(Structure):  
    _fields_ = [("AccCode", c_uint),
                ("AccMask", c_uint),
                ("Reserved", c_uint),
                ("Filter", c_ubyte),
                ("Timing0", c_ubyte),
                ("Timing1", c_ubyte),
                ("Mode", c_ubyte)
                ]  
class VCI_CAN_OBJ(Structure):  
    _fields_ = [("ID", c_uint),
                ("TimeStamp", c_uint),
                ("TimeFlag", c_ubyte),
                ("SendType", c_ubyte),
                ("RemoteFlag", c_ubyte),
                ("ExternFlag", c_ubyte),
                ("DataLen", c_ubyte),
                ("Data", c_ubyte*8),
                ("Reserved", c_ubyte*3)
                ]
byte_array = c_ubyte * 8
class Radar_Config:
    def __init__(self):
        self.buf = byte_array(0,0,0,0,0,0,0,0)
        self.init_config()
    def init_config(self):
        self.Set_Radar_MaxDistance_vaild(1)
        self.Set_Radar_Sensor_ID_valid(0)
        self.RadarCfg_CtrlRelay(0)
        self.RadarCfg_CtrlRelay_valid(0)
        self.RadarCfg_MaxDistance(105)
        self.RadarCfg_OutputType(1)
        self.RadarCfg_RCS_Threshold_Valid(0)
        self.RadarCfg_RCS_Threshold(0)
        self.RadarCfg_StoreInNVM_valid(0)
        self.RadarCfg_StoreInNVM(0)
        self.RadarCfg_OutputType_valid(1)
        self.RadarCfg_RadarPower(0)
        self.RadarCfg_RadarPower_valid(0)
        self.RadarCfg_SendExtInfo(0)
        self.RadarCfg_SendExtInfo_valid(0)
        self.RadarCfg_SendQuality_valid(0)
        self.RadarCfg_SendQuality(0)
        self.RadarCfg_SensorID(0)
        self.RadarCfg_SortIndex(0)
        self.RadarCfg_SortIndex_valid(0)
    def Set_Radar_MaxDistance_vaild(self,val):
        self.buf[0] &= ~(0x01 << 0)
        self.buf[0] |= (c_ubyte(val).value) & 0x01
    def Set_Radar_Sensor_ID_valid(self,val):
        self.buf[0] &= ~(0x01 << 1)
        self.buf[0] |= (c_ubyte(val).value) & 0x01
    def RadarCfg_RCS_Threshold_Valid(self,val):
        self.buf[6] &= ~(0x01 << 0)
        self.buf[6] |= (c_ubyte(val).value) & 0x01
    def RadarCfg_RCS_Threshold(self,val):
        self.buf[6] &= ~(0x07 << 1)
        self.buf[6] |= (c_ubyte(val).value & 0x07) << 1
    def RadarCfg_StoreInNVM_valid(self,val):
        self.buf[0] &= ~(0x01 << 7)
        self.buf[0] |= (c_ubyte(val).value & 0x01) << 7
    def RadarCfg_SortIndex_valid(self,val):
        self.buf[0] &= ~(0x01 << 6)
        self.buf[0] |= (c_ubyte(val).value & 0x01) << 6
    def RadarCfg_SortIndex(self,val):
        self.buf[5] &= ~(0x07 << 4)
        self.buf[5] |= (c_ubyte(val).value & 0x07) << 4
    def RadarCfg_StoreInNVM(self,val):
        self.buf[5] &= ~(0x01 << 7)
        self.buf[5] |= (c_ubyte(val).value & 0x01) << 7
    def RadarCfg_SendExtInfo_valid(self,val):
        self.buf[0] &= ~(0x01 << 5)
        self.buf[0] |= (c_ubyte(val).value & 0x01) << 5
    def RadarCfg_SendExtInfo(self,val):
        self.buf[5] &= ~(0x01 << 3)
        self.buf[5] |= (c_ubyte(val).value & 0x01) << 3
    def RadarCfg_CtrlRelay_valid(self,val):
        self.buf[5] &= ~(0x01 << 0)
        self.buf[5] |= (c_ubyte(val).value & 0x01) << 0
    def RadarCfg_CtrlRelay(self,val):
        self.buf[5] &= ~(0x01 << 1)
        self.buf[5] |= (c_ubyte(val).value & 0x01) << 1
    def RadarCfg_SendQuality_valid(self,val):
        self.buf[0] &= ~(0x01 << 4)
        self.buf[0] |= (c_ubyte(val).value & 0x01) << 4
    def RadarCfg_SendQuality(self,val):
        self.buf[5] &= ~(0x01 << 2)
        self.buf[5] |= (c_ubyte(val).value & 0x01) << 2    
    def RadarCfg_RadarPower_valid(self,val):
        self.buf[0] &= ~(0x01 << 2)
        self.buf[0] |= (c_ubyte(val).value & 0x01) << 2
    def RadarCfg_OutputType_valid(self,val):
        self.buf[0] &= ~(0x01 << 3)
        self.buf[0] |= (c_ubyte(val).value & 0x01) << 3
    def RadarCfg_MaxDistance(self,val):
        self.buf[1] &= ~(0xff << 0)
        self.buf[1] |= ((c_ubyte(c_ushort(val).value >> 2).value) & 0xff)
        self.buf[2] &= ~(0x03 << 6)
        self.buf[2] |= (c_ubyte(val).value & 0x03) << 6
    def RadarCfg_RadarPower(self,val):
        self.buf[4] &= ~(0x07 << 5)
        self.buf[4] |= (c_ubyte(val).value & 0x07) << 5
    def RadarCfg_OutputType(self,val):
        self.buf[4] &= ~(0x03 << 3)
        self.buf[4] |= (c_ubyte(val).value & 0x03) << 3
    def RadarCfg_SensorID(self,val):
        self.buf[4] &= ~(0x07 << 0)
        self.buf[4] |= (c_ubyte(val).value & 0x07) << 0
 
#Radar_state class
class Radar_State:
    def __init__(self):
        self.buf = byte_array(0,0,0,0,0,0,0,0)
    def buffer_filling(self,data):
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
        return ((c_ubyte(self.buf[3]).value) & 0x03) << 1 | ((c_ubyte(self.buf[4]).value >> 7) & 0x01)
    def RadarState_NVMReadStatus(self):
        return (c_ubyte(self.buf[0]).value >> 6) & 0x01
    def RadarState_MaxDistanceCfg(self):
        return 2 * (((c_ushort(self.buf[1]).value & 0xff) << 2) | ((c_ubyte(self.buf[2]).value >> 6) & 0x03))
    
class Object_list:
    def __init__(self):
        self.object_list = list()
    def clear_list(self):
        self.object_list.clear()
    def insert_object(self,obj):
        self.object_list.append(obj)
    def print_object(self):
        for it in self.object_list:
            print("ID:",it.id,end=" ")
            print("long",it.distlong,end=" ")
            print("lat",it.distlat,end=" ")

    

class Object:
    def __init__(self):
        self.id = c_ubyte(0)
        self.distlong = 0
        self.distlat = 0
    def get_obj_ID(self,buf):
        self.id = (c_ubyte(buf[0]).value) & 0xff
    def get_obj_distlong(self,buf):
        self.distlong = (((c_ushort(buf[1]).value & 0xff) << 5) | ((c_ubyte(buf[2]).value >> 3) & 0x1f)) * 0.2 - 500
    def get_obj_distlat(self,buf):
        self.distlat = (((c_ushort(buf[2]).value & 0x07) << 8) | ((c_ubyte(buf[2]).value >> 0) & 0xff)) * 0.2 - 204.8


#CanDLLName = './ControlCAN.dll' #把DLL放到对应的目录下
CanDLLName = './ControlCAN.so' #把SO放到对应的目录下,LINUX
#canDLL = windll.LoadLibrary('./ControlCAN.dll')
#Linux系统下使用下面语句，编译命令：python3 python3.8.0.py
canDLL = cdll.LoadLibrary('./libcontrolcan.so')


print(CanDLLName)
 
ret = canDLL.VCI_OpenDevice(VCI_USBCAN2, 0, 0)
if ret == STATUS_OK:
    print('调用 VCI_OpenDevice成功\r\n')
if ret != STATUS_OK:
    print('调用 VCI_OpenDevice出错\r\n')
 
#初始0通道
vci_initconfig = VCI_INIT_CONFIG(0x80000008, 0xFFFFFFFF, 0,
                                 0, 0x00, 0x1C, 0)#波特率500k，正常模式
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
 
radar_config = Radar_Config()
radar_state = Radar_State()
obj_list = Object_list()
obj = Object()


config = Radar_Config()
for i in range(8):
    print(hex(config.buf[i]))
ubyte_3array = c_ubyte*3
b = ubyte_3array(0, 0 , 0)
vci_can_obj = VCI_CAN_OBJ(0x200, 0, 0, 1, 0, 0,  8, config.buf, b)#单次发送
 
ret = canDLL.VCI_Transmit(VCI_USBCAN2, 0, 0, byref(vci_can_obj), 1)
if ret == STATUS_OK:
    print('CAN1通道发送成功\r\n')
if ret != STATUS_OK:
    print('CAN1通道发送失败\r\n')

#结构体数组类
import ctypes
class VCI_CAN_OBJ_ARRAY(Structure):
    _fields_ = [('SIZE', ctypes.c_uint16), ('STRUCT_ARRAY', ctypes.POINTER(VCI_CAN_OBJ))]

    def __init__(self,num_of_structs):
                                                                 #这个括号不能少
        self.STRUCT_ARRAY = ctypes.cast((VCI_CAN_OBJ * num_of_structs)(),ctypes.POINTER(VCI_CAN_OBJ))#结构体数组
        self.SIZE = num_of_structs#结构体长度
        self.ADDR = self.STRUCT_ARRAY[0]#结构体数组地址  byref()转c地址
    
rx_vci_can_obj = VCI_CAN_OBJ_ARRAY(2500)#结构体数组

#print(ret)
while 1:#一直循环查询接收。
        ret = canDLL.VCI_Receive(VCI_USBCAN2, 0, 0, byref(rx_vci_can_obj.ADDR), 2500, 0)
        if ret > 0:#接收到数据
            for i in range(0,ret):；
                if rx_vci_can_obj.STRUCT_ARRAY[i].ID == 0x60a:
                    print('CAN1通道接收成功',end=" ")
                    print('ID：',end="")
                    print(hex(rx_vci_can_obj.STRUCT_ARRAY[i].ID),end=" ")
                    print('DataLen：',end="")
                    print(hex(rx_vci_can_obj.STRUCT_ARRAY[i].DataLen),end=" ")
                    obj_list.print_object()
                    obj_list.clear_list()
                elif rx_vci_can_obj.STRUCT_ARRAY[i].ID == 0x60b:
                    obj.get_obj_ID(rx_vci_can_obj.STRUCT_ARRAY[i].Data)
                    obj.get_obj_distlat(rx_vci_can_obj.STRUCT_ARRAY[i].Data)
                    obj.get_obj_distlong(rx_vci_can_obj.STRUCT_ARRAY[i].Data)
                    obj_list.insert_object(obj)
                print('\r')
 
#关闭
canDLL.VCI_CloseDevice(VCI_USBCAN2, 0) 



