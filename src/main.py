from function import *


def main():
    spaceBaseURL = "https://api.bilibili.com/x/space/arc/search?mid=25910292&ps=30&tid=0&pn="
    savePath = "../outData/data.xls"
    bvList = getBV(spaceBaseURL)
    i = 0

    book = saveInitial(savePath)
    for bv in bvList:
        i = i + 1
        videoUrl = getVideoURL(bv)
        print("第" + str(i) + "个:" + videoUrl)
        data = getData(videoUrl)
        saveDataToXls(savePath, book, data, i)
    print("爬取成功")


if __name__ == '__main__':
    main()
