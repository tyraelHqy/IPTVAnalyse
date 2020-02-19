def IPTVAnalyseWithoutM3u():
    path = input("请输入需要转换的相对文件路径与文件名：(例如输入iptv.html)\n")
    ipAndPort = input("udpXp监听的ip和端口地址(如192.168.1.2:4042):\n")
    f = open(".\\" + path)
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

    f = open(".\iptvlistNew.m3u", 'w')
    f.write("#EXTM3U")
    f.write('\n' + '\n')
    for key, value in (sorted(dictChannel.items())):
        f.write("#EXTINF:-1," + key + '\n')
        f.write("http://" + ipAndPort + "/udp/" + value + '\n')
    f.close()
    print("最后生成文件目录: " + ".\iptvlistNew.m3u")


if __name__ == '__main__':
    IPTVAnalyseWithoutM3u()
