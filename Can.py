import struct
from ctypes import *
import ctypes


class VCI_INIT_CONFIG(Structure):
    _fields_ = [("AccCode", c_uint), ("AccMask", c_uint), ("Reserved", c_uint),
                ("Filter", c_ubyte), ("Timing0", c_ubyte),
                ("Timing1", c_ubyte), ("Mode", c_ubyte)]


class VCI_CAN_OBJ(Structure):
    _fields_ = [("ID", c_uint), ("TimeStamp", c_uint), ("TimeFlag", c_ubyte),
                ("SendType", c_ubyte), ("RemoteFlag", c_ubyte),
                ("ExternFlag", c_ubyte), ("DataLen", c_ubyte),
                ("Data", c_ubyte * 8), ("Reserved", c_ubyte * 3)]


class VCI_CAN_OBJ_ARRAY(Structure):
    _fields_ = [('SIZE', ctypes.c_uint16),
                ('STRUCT_ARRAY', ctypes.POINTER(VCI_CAN_OBJ))]

    def __init__(self, num_of_structs):
        # 这个括号不能少
        self.STRUCT_ARRAY = ctypes.cast((VCI_CAN_OBJ * num_of_structs)(),
                                        ctypes.POINTER(VCI_CAN_OBJ))  # 结构体数组
        self.SIZE = num_of_structs  # 结构体长度
        self.ADDR = self.STRUCT_ARRAY[0]  # 结构体数组地址  byref()转c地址
