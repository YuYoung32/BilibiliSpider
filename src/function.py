import random
import re
import urllib.request
import urllib.error
from io import BytesIO

import xlwt
import json
from bs4 import BeautifulSoup
import gzip


def getBV(spaceBaseURL):
    """
    获取全部视频的BV号
    Args:
        spaceBaseURL:

    Returns: a BV list

    """
    bvList = []
    for i in range(19):
        print("get page " + str(i + 1) + " bvid")
        url = spaceBaseURL + str(i + 1)
        pageData = askURL(url)
        pageJson = json.loads(pageData)
        for item in pageJson['data']['list']['vlist']:
            bvList.append(item['bvid'])
    return bvList


def getData(videoURL):
    """
    获取视频数据
    Args:
        videoURL:

    Returns: a data item

    """
    # region 正则表达式
    findTitle = re.compile(r'<span class="tit tr-fix">(.+?)</span>')
    findDescription = re.compile(r'<span>(.+)</span>')
    findTime = re.compile(r'<span>(.*?)</span>')
    findTotal = re.compile(r'<span class="view" title="总播放数(\d+?)">')
    findDM = re.compile(r'<span class="dm" title="历史累计弹幕数(\d+?)">')
    findLike = re.compile(r'<span class="like" title="点赞数(\d+?)">')
    findCoin = re.compile(r'<span class="coin" title="投硬币枚数(\d+?)">')
    findCollect = re.compile(r'<span class="collect" title="收藏人数(\d+?)">')
    findShare = re.compile(r'<i class="van-icon-videodetails_share"></i>(\d+)')
    # endregion

    videoHtml = askURLGzip(videoURL)
    soup = BeautifulSoup(videoHtml, 'html.parser')

    report = soup.find_all("div", id="viewbox_report")
    report = str(report)
    title = re.findall(findTitle, report)
    time = re.findall(findTime, report)
    total = re.findall(findTotal, report)
    DM = re.findall(findDM, report)

    ops = soup.find_all("div", {"class": "ops"})
    ops = str(ops)
    like = re.findall(findLike, ops)
    coin = re.findall(findCoin, ops)
    collect = re.findall(findCollect, ops)
    share = re.findall(findShare, ops)

    desc = soup.find_all("div", id="v_desc")
    description = re.findall(findDescription, str(desc))

    dataItem = [videoURL, toOne(title), toOne(description), toOne(time), toOne(total), toOne(DM), toOne(like),
                toOne(coin), toOne(collect), toOne(share)]
    return dataItem


def toOne(data):
    """
    输出一个数据
    Args:
        data:

    Returns: data[0] or "None"

    """
    if len(data) == 0:
        return "None"
    else:
        return data[0]


def getVideoURL(BV):
    """
    从BV号获得视频地址
    Args:
        BV:

    Returns: a link to the video

    """
    if len(BV) == 12:
        return "https://www.bilibili.com/video/" + BV
    else:
        print("ERROR: wrong video URL")
        print("the wrong BV is " + BV)
        return "https://www.bilibili.com/video/BV1oo4y1D7q9"


def askURL(URL):
    """
    从URL中获取返回
    Args:
        URL:

    Returns: a url back

    """
    print("ask url...")

    my_headers = [
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0"
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"
    ]
    randomHeaders = random.choice(my_headers)
    headers = {
        "User-Agent": randomHeaders
    }
    request = urllib.request.Request(URL, headers=headers)
    back = ""
    try:
        response = urllib.request.urlopen(request)
        back = response.read().decode('UTF-8')
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return back


def askURLGzip(URL):
    """
    读取压缩流
    Args:
        URL:

    Returns: a url back

    """
    global dehtml
    print("ask url...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.70"
    }
    request = urllib.request.Request(URL, headers=headers)
    try:
        response = urllib.request.urlopen(request)
        back = response.read()
        buff = BytesIO(back)
        f = gzip.GzipFile(fileobj=buff)
        dehtml = f.read().decode('utf-8')
        return dehtml
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)


def saveInitial(savePath):
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = book.add_sheet('sheet1', cell_overwrite_ok=True)  # 可以覆写
    col = ('视频链接', '视频标题', '视频详情', '发布时间', '总观看人数', '总弹幕数', '点赞数', '硬币数', '收藏数', '分享数')
    print("save ...")
    # 写入表头
    for i in range(0, 10):
        sheet.write(0, i, col[i])
    return book


def saveDataToXls(savePath, book, data, i):
    """
    保存数据到表格
    Args:
        savePath:
        datalist:

    Returns:

    """
    sheet = book.get_sheet('sheet1')
    for j in range(0, 10):
        sheet.write(i, j, data[j])
    book.save(savePath)  # 保存文件
    print("saved! file path: " + savePath)
