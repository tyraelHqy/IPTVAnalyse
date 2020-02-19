import os, sys


def printEveryNum(lists, step):
    list__ = [lists[i:i + step] for i in range(0, len(lists), step)]
    for list in list__:
        print(list)


def IPTVAnalyse():
    path = input("请输入需要转换的相对文件路径与文件名：(例如输入iptv.html)\n")

    ipAndPort = input("udpXp监听的ip和端口地址(如192.168.1.2:4042):\n")
    # ipAndPort = "192.168.1.2:4042"
    f = open(".\\" + path)
    # f = open(".\iptv.html")
    lines = f.readlines()
    strs = "jsSetConfig('Channel'"
    iptvs = []
    for line in lines:
        if strs in line:
            iptvs.append(line)

    strChannelName = "ChannelName="
    strChannelURL = "ChannelURL="
    channelNameLists = []
    strChannelURLLists = []
    for iptv in iptvs:
        iptvlist = iptv.split(",")
        for values in iptvlist:  # 循环输出列表值
            if strChannelName in values:
                channelNameLists.append(values.replace("十", "+").strip('"')[13:])
            if strChannelURL in values:
                if len(values.strip('"')[19:]) < 50:
                    strChannelURLLists.append(values.strip('"')[19:])
    dictChannel = dict(zip(channelNameLists, strChannelURLLists))
    print("从html一共获取了: " + str(len(channelNameLists)) + " 条数据")

    channelNameSorts = []
    channelUrlSorts = []
    channelNameStr = "#EXTINF:-1,"
    channelUrlStr = "http://"

    txt = open(".\iptvlist.m3u")
    lines = txt.readlines()
    txt.close()
    for line in lines:
        if channelNameStr in line:
            channelNameSorts.append(line[11:].strip())
        if channelUrlStr in line:
            channelUrlSorts.append(line[28:].strip())
    dictChannelSort = dict(zip(channelNameSorts, channelUrlSorts))

    updateList = []
    insertList = []
    for key, value in dictChannel.items():
        try:
            if dictChannelSort[key] != dictChannel[key]:
                dictChannelSort[key] = dictChannel[key]
                updateList.append(key)
        except:
            dictChannelSort[key] = value
            insertList.append(key)
    print("更新了: ")
    printEveryNum(updateList, 10)
    print("一共更新了: " + str(len(updateList)) + " 条数据\n")
    print("更新了: ")
    printEveryNum(insertList, 10)
    print("一共增加了: " + str(len(insertList)) + " 条数据\n")

    f = open(".\iptvlist.m3u", 'w')
    f.write("#EXTM3U")
    f.write('\n' + '\n')
    for key, value in (dictChannelSort.items()):
        f.write("#EXTINF:-1," + key + '\n')
        f.write("http://" + ipAndPort + "/udp/" + value + '\n')
    f.close()
    print("最后生成文件目录: " + ".\iptvlist.m3u")


if __name__ == '__main__':
    IPTVAnalyse()
