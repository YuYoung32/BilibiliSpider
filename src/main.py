import pathlib

from function import *


def main():
    print("welcome to use this spider.")
    apiURL= getAPI(input("please input your space url or uid"))
    savePath = "../outData/data2.xls"
    bvList = getBV(apiURL)
    i = 0
    if pathlib.Path(savePath).exists():
        print("file exists, please delete it.")
        exit(1)
    book = saveInitial()
    for bv in bvList:
        i = i + 1
        videoUrl = getVideoURL(bv)
        print("第" + str(i) + "个:" + videoUrl)
        data = getData(videoUrl)
        saveDataToXls(savePath, book, data, i)
    print("爬取成功")


if __name__ == '__main__':
    main()
