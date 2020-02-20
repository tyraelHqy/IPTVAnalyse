import os, sys

"""
输入：lists 即将打印的列表，step 需要换行的个数
输出：无
功能：将list按照step的个数进行换行
"""
def printEveryNum(lists, step):
    list__ = [lists[i:i + step] for i in range(0, len(lists), step)]
    for list in list__:
        print(list)


"""
输入：无
输出：dictChannel，字典格式，为初始html文件提取出来的ChannelName与Url
"""
def readHtmlFile():
    path = input("请输入需要转换的相对文件路径与文件名：(例如输入iptv.html)\n")
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
    return dictChannel


"""
输入：无
输出：dictChannelSort，字典格式，为m3u文件提取出来的排好序的ChannelName与Url
"""
def getM3uSorted():
    channelNameSorts = []
    channelUrlSorts = []
    channelNameStr = "#EXTINF:-1,"
    channelUrlStr = "http://"
    txt = open(".\\iptvlist.m3u")
    lines = txt.readlines()
    txt.close()
    for line in lines:
        if channelNameStr in line:
            channelNameSorts.append(line[11:].strip())
        if channelUrlStr in line:
            channelUrlSorts.append(line[28:].strip())
    dictChannelSort = dict(zip(channelNameSorts, channelUrlSorts))
    return dictChannelSort


"""
输入：dictChannel，dictChannelSort
输出：无
功能：按照dictChannelSort的顺序，将dictChannel的数据增加至按照dictChannelSort字典中，并且输出成m3u文件。
"""
def updateDictChannelSortList(dictChannel, dictChannelSort):
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
    m3uFileOut(dictChannelSort)


"""
输入：dict
输出：无
功能：按照字典顺序输出m3u文件。
"""
def m3uFileOut(dict):
    ipAndPort = input("请输入即将写入m3u文件的udpXp监听的ip和端口地址(如192.168.1.2:4042):\n")
    # ipAndPort = "192.168.1.2:4042"
    f = open(".\iptvlist.m3u", 'w')
    f.write("#EXTM3U")
    f.write('\n' + '\n')
    for key, value in (dict.items()):
        f.write("#EXTINF:-1," + key + '\n')
        f.write("http://" + ipAndPort + "/udp/" + value + '\n')
    f.close()
    print("最后生成文件目录: " + ".\iptvlist.m3u")


"""
主函数
"""
def IPTVAnalyse():
    dictChannel = readHtmlFile()
    try:
        dictChannelSort = getM3uSorted()
    except FileNotFoundError:
        m3uFileOut(dictChannel)
        return
    updateDictChannelSortList(dictChannel, dictChannelSort)
    pass


if __name__ == '__main__':
    IPTVAnalyse()
