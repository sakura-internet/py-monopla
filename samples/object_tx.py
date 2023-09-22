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

#オブジェクトのリストを作って送信
objs = []
##整数
for i in range(8):
    objs.append(object.SipfObject(i, object.SipfObjectType(i), i))
##浮動小数点数
objs.append(object.SipfObject(0x10, object.SipfObjectType.FLOAT32, 1.4142135))
objs.append(object.SipfObject(0x11, object.SipfObjectType.FLOAT64, 2.2360679775))
##可変長バイナリ/文字列
objs.append(object.SipfObject(0x20, object.SipfObjectType.BIN, b"\x01\x02\x03\x04\x05"))
objs.append(object.SipfObject(0x21, object.SipfObjectType.STR_UTF8, "Hello"))

##送信
ret = object.tx(objs, auth_info)

print("OTID:" + ret.hex())
