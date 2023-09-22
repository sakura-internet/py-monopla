from enum import IntEnum
from struct import *

from . import auth
import urllib.request

SIPF_OBJECT_CONNECTOR_URL="https://connector.sipf.iot.sakura.ad.jp/v0"

class SipfObjectCmd(IntEnum):
    UP = 0x00
    UP_RETRY = 0x01
    NOTIFICATION = 0x02
    DOWN_REQUEST = 0x11
    DOWN = 0x12
    ERR = 0xff

class SipfObjectType(IntEnum):
    UINT8 = 0x00
    INT8 = 0x01
    UINT16 = 0x02
    INT16 = 0x03
    UINT32 = 0x04
    INT32 = 0x05
    UINT64 = 0x06
    INT64 = 0x07
    FLOAT32 = 0x08
    FLOAT64 = 0x09
    BIN_BASE64 = 0x10
    BIN = 0x10
    STR_UTF8 = 0x20

class SipfObject:
    obj_type = None
    tagid = None
    value_len = None
    value = None

    def __init__(self, tagid, obj_type, value):
        if not (type(obj_type) is SipfObjectType):
            raise TypeError("obj_type is invalid type")

        if (tagid < 0x00) or (tagid > 0xff):
            raise ValueError("tagid is out of range")

        # valueが妥当かチェック
        if (obj_type == SipfObjectType.UINT8) or (obj_type == SipfObjectType.INT8):     #uint8, int8
            if not (type(value) is int):
                raise TypeError("`obj_type' and `value' types do mismatch")
            value_len = 1
        elif (obj_type == SipfObjectType.UINT16) or (obj_type == SipfObjectType.INT16): #uint16, int16
            if not (type(value) is int):
                raise TypeError("`obj_type' and `value' types do mismatch")
            value_len = 2
        elif (obj_type == SipfObjectType.UINT32) or (obj_type == SipfObjectType.INT32): #uint32, int32
            if not (type(value) is int):
                raise TypeError("`obj_type' and `value' types do mismatch")
            value_len = 4
        elif (obj_type == SipfObjectType.UINT64) or (obj_type == SipfObjectType.INT64): #uint64, int64
            if not (type(value) is int):
                raise TypeError("`obj_type' and `value' types do mismatch")
            value_len = 8
        elif obj_type == SipfObjectType.FLOAT32:                                        #float32
            if not (type(value) is float):
                raise TypeError("`obj_type' and `value' types do mismatch")
            value_len = 4
        elif obj_type == SipfObjectType.FLOAT64:                                        #float64
            if not (type(value) is float):
                raise TypeError("`obj_type' and `value' types do mismatch")
            value_len = 8
        elif obj_type == SipfObjectType.BIN:                                            #bin
            if not (type(value) is bytes):
                raise TypeError("`obj_type' and `value' types do mismatch")
            value_len = len(value)
        elif obj_type == SipfObjectType.STR_UTF8:
            if not (type(value) is str):
                raise TypeError("`obj_type' and `value' types do mismatch")
            value_len = len(value)
        #メンバ変数に格納
        self.tagid = tagid
        self.obj_type = obj_type
        self.value = value    
        self.value_len = value_len

def create_payload(objs):
    buff = b''
    idx = 0

    obj_qty = len(objs)
    for obj in objs:
        if not (type(obj) is SipfObject):
            raise TypeError("objs member type is invalid")

        # add obj_type
        buff += pack("B", obj.obj_type)
        # add tagid
        buff += pack("B", obj.tagid)
        # add value_len
        buff += pack("B", obj.value_len)
        # add value
        if   obj.obj_type == SipfObjectType.UINT8:
            buff += pack("!B", obj.value)
        elif obj.obj_type == SipfObjectType.INT8:
            buff += pack("!b", obj.value)
        elif obj.obj_type == SipfObjectType.UINT16:
            buff += pack("!H", obj.value)
        elif obj.obj_type == SipfObjectType.INT16:
            buff += pack("!h", obj.value)
        elif obj.obj_type == SipfObjectType.UINT32:
            buff += pack("!I", obj.value)
        elif obj.obj_type == SipfObjectType.INT32:
            buff += pack("!i", obj.value)
        elif obj.obj_type == SipfObjectType.UINT64:
            buff += pack("!Q", obj.value)
        elif obj.obj_type == SipfObjectType.INT64:
            buff += pack("!q", obj.value)
        elif obj.obj_type == SipfObjectType.FLOAT32:
            buff += pack("!f", obj.value)
        elif obj.obj_type == SipfObjectType.FLOAT64:
            buff += pack("!d", obj.value)
        elif obj.obj_type == SipfObjectType.BIN:
            buff += obj.value
        elif obj.obj_type == SipfObjectType.STR_UTF8:
            buff += obj.value.encode('utf-8')

    return buff

def _request_sipf_object(cmd, payload, auth):
    #Basic認証ヘッダを生成
    basic_auth_header = {'Authorization': 'Basic ' + auth.basic_auth_value()}
    #エンドポイントにコマンドを投げるリクエスト
    req = urllib.request.Request(SIPF_OBJECT_CONNECTOR_URL, data=(cmd + payload), headers=basic_auth_header, method="POST")
    with urllib.request.urlopen(req) as res:
        body = res.read()

    return body

def tx(objs, auth):
    payload = create_payload(objs)
    sz_payload = len(payload)

    cmd = b''
    cmd += pack('B', SipfObjectCmd.UP)  #COMMAND_TYPE
    cmd += pack('!Q', 0)                #COMMAND_TIME
    cmd += pack('B', 0)                 #OPTION_FLAG
    cmd += pack('!H', sz_payload)       #PAYLOAD_SIZE

    ret = _request_sipf_object(cmd, payload, auth)
    if len(ret) != 30:
        raise ValueError("SIPF_OBJECT_UP respons size is invalid")
    
    res = unpack("!BQBHBB16s", ret)
    if res[0] != SipfObjectCmd.NOTIFICATION:
        raise ValueError("SIPF_OBJECT_UP: response command type is invalid command_type=0x%02x" % res[0])
    if res[4] != 0x00:
        #SIPF_OBJECT_UPコマンドの実行結果が成功じゃない
        raise ValueError("SIPF_OBJECT_UP: failed.")

    return res[6]   #OTIDを返す

def rx(objs, auth):
    cmd = b''
    cmd += pack('B', SipfObjectCmd.DOWN_REQUEST)    #COMMAND_TYPE
    cmd += pack('!Q', 0)                            #COMMAND_TIME
    cmd += pack('B', 0)                             #OPTION_FLAG
    cmd += pack('!H', 1)                            #PAYLOAD_SIZE

    payload = b'\x00'   #RESERVED

    ret = _request_sipf_object(cmd, payload, auth)

    #SIPF_DOWN(HEADER)
    res_head = unpack("!BQBH", ret[:12])
    payload_len = res_head[3]
    is_empty = (payload_len == 35)
    #SIPF_DOWN(PAYLOAD Header)
    res_payload_head = unpack("!B16sQQBB", ret[12:47])
    cmd_res = res_payload_head[0]
    otid = res_payload_head[1]

    if (is_empty) :
        return None

    #SIPF_DOWN(PYLOAD Objects)
    res_objs = ret[47:] 
    obj_qty = 0
    while True:
        typ = SipfObjectType(res_objs[0])
        tag = res_objs[1]
        sz  = res_objs[2]
        val = None
        if   typ == SipfObjectType.UINT8:
            val = unpack("!B", res_objs[3:(3+sz)])[0]
        elif typ == SipfObjectType.INT8:
            val = unpack("!b", res_objs[3:(3+sz)])[0]
        elif typ == SipfObjectType.UINT16:
            val = unpack("!H", res_objs[3:(3+sz)])[0]
        elif typ == SipfObjectType.INT16:
            val = unpack("!h", res_objs[3:(3+sz)])[0]
        elif typ == SipfObjectType.UINT32:
            val = unpack("!L", res_objs[3:(3+sz)])[0]
        elif typ == SipfObjectType.INT32:
            val = unpack("!l", res_objs[3:(3+sz)])[0]
        elif typ == SipfObjectType.UINT64:
            val = unpack("!Q", res_objs[3:(3+sz)])[0]
        elif typ == SipfObjectType.INT64:
            val = unpack("!q", res_objs[3:(3+sz)])[0]
        elif typ == SipfObjectType.FLOAT32:
            val = unpack("!f", res_objs[3:(3+sz)])[0]
        elif typ == SipfObjectType.FLOAT64:
            val = unpack("!d", res_objs[3:(3+sz)])[0]
        elif typ == SipfObjectType.BIN:
            val = res_objs[3:(3+sz)]
        elif typ == SipfObjectType.STR_UTF8:
            val = res_objs[3:(3+sz)].decode('utf-8')

        objs.append(SipfObject(tag, typ, val))

        if (3 + sz) >= len(res_objs):
            break

        res_objs = res_objs[3+sz:]
    
    return otid



