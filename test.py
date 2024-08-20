from ctypes import *
byte_array = c_ubyte*8
class Radar_Config:
    def __init__(self):
        self.buf = byte_array(0,0,0,0,0,0,0,0)
        self.init_config()
    def init_config(self):
        self.Set_Radar_MaxDistance_vaild(1)
        self.Set_Radar_Sensor_ID_valid(0)
        self.RadarCfg_CtrlRelay(0)
        self.RadarCfg_CtrlRelay_valid(0)
        self.RadarCfg_MaxDistance(522)
        self.RadarCfg_OutputType(0)
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
class Radar_State:
    def __init__(self):
        self.buf = byte_array(0,0,0,0,0,0,0,0)
    def buffer_filling(self,data):
        self.buf = data
    def RadarState_Voltage_Error(self,val):
        return (c_ubyte(self.buf[2]).value >> 1) & 0x01
    def RadarState_SortIndex(self,val):
        return (c_ubyte(self.buf[4]).value >> 4) & 0x07
    def RadarState_RCS_Threshold(self,val):
        return (c_ubyte(self.buf[7]).value >> 2) & 0x07
    def RadarState_SendQualityCfg(self,val):
        return (c_ubyte(self.buf[5]).value >> 4) & 0x01
    def RadarState_SendExtInfoCfg(self,val):
        return (c_ubyte(self.buf[5]).value >> 5) & 0x01
    def RadarState_MotionRxState(self,val):
        return (c_ubyte(self.buf[5]).value >> 6) & 0x03
    def RadarState_OutputTypeCfg(self,val):
        return (c_ubyte(self.buf[5]).value >> 2) & 0x03
    def RadarState_RadarPowerCfg(self,val):
        return ((c_ubyte(self.buf[3]).value) & 0x03) << 1 | ((c_ubyte(self.buf[4]).value >> 7) & 0x01)
    def RadarState_NVMReadStatus(self,val):
        return (c_ubyte(self.buf[0]).value >> 6) & 0x01
    def RadarState_MaxDistanceCfg(self,val):
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




        
config = Radar_Config()
for i in range(8):
    print(hex(config.buf[i]))

