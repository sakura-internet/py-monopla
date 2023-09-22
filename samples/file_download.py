#!/usr/bin/env python

import sys
from py_monopla import auth, file 

args = sys.argv

if len(args) != 3:
    print("usage:")
    print("")
    print("  %s <file_id> <file_path>" % args[0])
    print("")
    print("  file_id  : File name for file transport function of Sakura Monoplatform.")
    print("  file_path: Path of file from download.")
    sys.exit(1)

file_id = args[1]
file_path = args[2]

#認証情報を取得
auth_info = auth.SipfAuth()
ret = auth.get_auth_info(auth_info)
if ret != 0:
    print("get_auth_info() failed.")
    print("return value: %d" % ret)
    sys.exit()
    #戻り値が-405(Method Not Allowed)の場合、セキュアモバイルコネクトではなく
    #インターネット経由でAPIを叩いている可能性あり

#ダウンロードを実行
print("download %s from %s" % (file_id, file_path))

ret = file.download(file_path, file_id, auth_info)
if (ret == 0):
    print("download successful.")
else:
    print("download faild... err=%d" % ret)

