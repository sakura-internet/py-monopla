#!/usr/bin/env python

import sys
from py_monopla import auth, object

#認証情報を取得
auth_info = auth.SipfAuth()
ret = auth.get_auth_info(auth_info)
if ret != 0:
    print("get_auth_info() failed.")
    print("return value: %d" % ret)
    sys.exit()
    #戻り値が-405(Method Not Allowed)の場合、セキュアモバイルコネクトではなく
    #インターネット経由でAPIを叩いている可能性あり

#オブジェクトを受信して表示
objs = []
ret = object.rx(objs, auth_info)
if ret is not None:
    print("OTID: %s" % ret.hex())
    for obj in objs:
        print("")
        print("tag: 0x%02x" % obj.tagid)
        print("type: %s" % obj.obj_type)
        print("value_len: %d" % obj.value_len)
        print("value: ", end="") 
        print(obj.value)
else:
    print("Empty")

