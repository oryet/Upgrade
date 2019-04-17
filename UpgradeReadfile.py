#!/usr/bin/python
# -*- coding: UTF-8 -*-

def ByteToHex(bins):
    return ''.join(["%02X" % x for x in bins]).strip()


def ReadBinFile(file):
    sendlist = []
    # 打开文件
    fo = open(file, "rb")  # 读取二进制文件用 rb
    print ("文件名为: ", fo.name)

    try:
        while 1:
            c = fo.read(128)
            if not c:
                break
            else:
                strsend = ByteToHex(c)
                # print(strsend)
                sendlist += [strsend]
    finally:
        fo.close()
    return sendlist
