# Bilibili爬虫

能够爬取哔哩哔哩UP主的视频标题和点赞投币收藏转发数

并且进行数据分析



### 流程

```mermaid
graph LR
A(爬取数据) -->B(数据分析)
    B --> C(数据可视化)
```

* 爬取数据
  * 分析网页
  * 发送请求 askURL
  * 内容解析 getData
  * 保存数据 saveData
* 数据分析：找出四者直接的关系
  * 多元线性回归拟合？
* 数据可视化
  * 
* 撰写报告
  * 

### 数据要求
#### 视频详情
* 视频链接
* 视频文案
* 视频标题
* 发布时间

#### 量化数据
* 总播放数
* 历史累计弹幕数
* 点赞数
* 投币数
* 收藏数
* 分享数



### 项目细节
* B站UP主钟文泽，视频主页地址：

  ```https://space.bilibili.com/25910292/video?tid=0&page=1&keyword=&order=pubdate```

  page ∈ [1, 19]，每页30个视频，按发布时间从新到旧。

  但是网页数据是由动态js返回数据的，无法直接从页面源码获取，经过查看网络流，得知，从这个地址

  ```https://api.bilibili.com/x/space/arc/search?mid=25910292&ps=30&tid=0&pn=```

  获得json数据。

  从json得到BV号，把BV号存储供后续使用。

* 根据BV号寻找视频：

  ```https://www.bilibili.com/video/BV1oo4y1D7q9```

  进入视频首页，在视频首页获取需要数据

  
### 程序结构

* main.py
  * getBV(spaceBaseURL)
  * BVList -> videoURLList
  * getData(videoURLList)
  * saveDataToXls(savPath, dataItemList)
* function.py
  * getBV(spaceBaseURL)
    * return BVList
  * getData(videoURLList)
    * return dataItemList
  * getVideoURL(BV)
    * return videoURL
  * askURL(URL)
    * return HTML
  * saveDataToXls(savePath, dataItemList)

  

  