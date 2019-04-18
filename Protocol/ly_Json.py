import json
import re

g_cnt = 0

def subStrToJson(data):
    if data == None:
        return None
    # 原因在于：字符串里用单引号来标识字符
    data = re.sub('\'', '\"', data)
    data = re.sub('\n', '', data)

    # 字符串 转 json
    try:
        data_json = json.loads(data)
    except:
        print(data)
        return None
    # addr = data_json['DataValue']['04A20208']
    # print(addr)
    return data_json

def JsonParse(data):
    if (data['Len']):
        if (data['Cmd']):
            if (data['SN']):
                if (data['DataTime']):
                    if (data['CRC']):
                        if (data['DataValue']):
                            return [data['DataValue']]
    return [False]

def JsonDealFrame(recvframe, senddata, answer):
    json_frame = recvframe # subStrToJson(recvframe)
    json_senddata = senddata # subStrToJson(senddata)

    # 接收帧 去除头部结构
    if "recvData" in json_frame:
        json_frame = json_frame["recvData"]

    if json_frame is not None and json_senddata is not None:
        if json_senddata["Cmd"] == json_frame["Cmd"]:
            if json_senddata["DataValue"].keys() ==  json_frame["DataValue"].keys():
                value = list(json_frame["DataValue"].values())[0]
                if value == answer:
                    return 1, value
    return -1, None


# CRC16/IBM x16 + x15 + x2 + 1
def crc16(x, invert):
    a = 0
    b = 0xA001
    for byte in x:
        a ^= ord(byte)
        for i in range(8):
            last = a % 2
            a >>= 1
            if last == 1:
                a ^= b
    s = hex(a).upper()
    return s[4:6] + s[2:4] if invert == True else s[2:4] + s[4:6]


def JsonMakeFrame(Value):
    global g_cnt
    g_cnt = g_cnt + 1
    data = {"Len":"312","Cmd":Value[0],"SN":str(g_cnt),"DataTime":"180706121314","CRC":"FFFF",
            "DataValue":Value[1]}

    dv = str(Value[1])[1:-1].replace(" ", "")  # 去大括号和空格
    dv = "0000" + crc16(dv, False)
    data["CRC"] = dv[-4:]

    # 将python对象data转换json对象
    data_json = json.dumps(data, ensure_ascii=False)

    # 将json对象转换成python对象
    # data_python = json.loads(data_json)

    return data_json

'''
def JsonMakeValue(DIlist):
    for i in DIlist:
        Value =
'''

if __name__ == '__main__':
    Value = {"05060102":"", "05060103":"123456"}

    # 数据项和内容
    cmd = 'Set'
    DIList = ['05060101', '05060102', '05060103']
    ValueList = ['000000.00', '123.14', '778899']
    List = dict(zip(DIList, ValueList))

    MakeFramePara = []
    MakeFramePara += [cmd]
    MakeFramePara += [List]

    # 元组转json
    #DIValue = json.loads(data_python)

    # json 转 字符串
    data_python = JsonMakeFrame(MakeFramePara)
    print(data_python)

    # 字符串 转 json
    data = json.loads(data_python)
    JsonDealFrame(data_python, data, "000000.00")



    # a = JsonParse(data)
    '''
    for key in a:
        print(key)
    # print(a.key())
    #for key in a.iterkeys():
    print(a.values())
    for value in a.values():
        print(value)
    '''
