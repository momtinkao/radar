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
        self.RadarCfg_MaxDistance(1023)
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
    def RadarState_Temporary_Error(self,val)
    def RadarState_Temperature_Error(self,val)
    def RadarState_Interference(self,val)
    def RadarState_Persistent_Error(self,val)
    def RadarState_SortIndex(self,val)
    def RadarState_RCS_Threshold(self,val)
    def RadarState_CtrlRelayCfg(self,val)
    def RadarState_SendQualityCfg(self,val)
    def RadarState_SendExtInfoCfg(self,val)
    def RadarState_MotionRxState(self,val)
    def RadarState_SensorID(self,val)
    def RadarState_OutputTypeCfg(self,val):
        return (c_ubyte(self.buf[5]).value >> 2) & 0x03
    def RadarState_RadarPowerCfg(self,val)
    def RadarState_NVMReadStatus(self,val)
    def RadarState_NVMwriteStatus(self,val)
    def RadarState_MaxDistanceCfg(self,val):
        return ((c_ushort(self.buf[1]).value & 0xff) << 2) | ((c_ubyte(self.buf[2]).value >> 6) & 0x03)
        
        
config = Radar_Config()
for i in range(8):
    print(hex(config.buf[i]))

