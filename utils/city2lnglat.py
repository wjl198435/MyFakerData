import requests
import json


def address2latlng(address):
    # 去除换行符
    _address = address.strip('\n').replace('#',' ')
    # 去除特殊字符
    _address = _address.replace('#', ' ').replace('/',' ')

    baiduUrl = "http://api.map.baidu.com/geocoding/v3/?address=%s&output=json&ak=NlGe4ouP54DGYvlhFGKBD3DqVuY9RQAo" % (_address)

    req = requests.get(baiduUrl)
    content = req.text
    content = content.replace("renderOption&&renderOption(", "")
    # content = content[:-1]
    # print(type(content))
    # print(content["status"])
    # type(content)
    # print(content)
    baiduAddr = json.loads(content)
    # print(baiduAddr)
    # baiduAddr = json.loads(content)
    # if baiduAddr["status"] == 0:
    #     lng = baiduAddr["result"]["location"]["lng"]
    #     lat = baiduAddr["result"]["location"]["lat"]
    return baiduAddr

# with open("1.txt","r", encoding="utf-8") as fr:
#     with open("2.txt", "w", encoding="utf-8") as fw:
#         for line in fr.readlines():
#             # 去除换行符
#             line = line.strip('\n').replace('#',' ')
#             # 去除特殊字符
#             line1 = line.replace('#', ' ').replace('/',' ')
#             # 地址获取经纬度
#             # http://api.map.baidu.com/geocoding/v3/?address=北京市海淀区上地十街10号&output=json&ak=您的ak&callback=showLocation
#             baiduUrl = "http://api.map.baidu.com/geocoding/v3/?address=%s&output=json&ak=NlGe4ouP54DGYvlhFGKBD3DqVuY9RQAo&callback=showLocation" % (line1)
#             print(baiduUrl)
#             req = requests.get(baiduUrl)
#             content = req.text
#             content = content.replace("renderOption&&renderOption(", "")
#             content = content[:-1]
#             print(content)
            # baiduAddr = json.loads(content)
            # lng = baiduAddr["result"]["location"]["lng"]
            # lat = baiduAddr["result"]["location"]["lat"]
            # # 经纬度获取城市
            # baiduUrl = "http://api.map.baidu.com/geocoding/v3/?ak=NlGe4ouP54DGYvlhFGKBD3DqVuY9RQAo&callback=showLacation&address=%s,%s&output=json" % (
            #     lat, lng)
            # req = requests.get(baiduUrl)
            # content = req.text
            # content = content.replace("renderReverse&&renderReverse(", "")
            # content = content[:-1]
            # baiduAddr = json.loads(content)
            # province = baiduAddr["result"]["addressComponent"]["province"]
            # city = baiduAddr["result"]["addressComponent"]["city"]
            # district = baiduAddr["result"]["addressComponent"]["district"]
            # # 写入2.txt文件
            # new_line = line + "|" + str(lng) + "|" + str(lat) + "|" + province + "|" + city + "|" + district
            # fw.write(new_line)
            # fw.write("\n")

if __name__ == '__main__':
    address = "太极传媒有限公司"
    print(address2latlng(address))