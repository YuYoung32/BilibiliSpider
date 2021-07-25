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

注意：不是所有视频都有以下数据，网页结构不是完全一样。

#### 视频详情
* 视频链接

* 视频标题
* 视频文案
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

  进入视频首页，在视频首页获取需要数据.

  视频首页使用压缩进行传输数据，所以无法直接解析。需要：

  ```
  gzip.GzipFile()
  ```

  进行解析才可以获得正常的HTML，否则为乱码。

* 数据项并不是全部都有，所以经过BeautifulSoup进行find_all()后需要进行判断数据项是否存在。

* 注意：B站对视频页数据具有限制措施，根据IP进行限制，一个IP在一段时间内只能请求500次。可以通过更换代理解决，此方案未在代码中体现。若不能自动更换，则每次只能获取到500条数据

### 程序结构

* main.py
  * getBV(spaceBaseURL)
  * BVList -> videoURLList
  * getData(videoURL)
  * saveInitial(savePath)
  * saveDataToXls(savePath, book, data, i)
  
* function.py
  * getBV(spaceBaseURL)
    * return BVList
  * getData(videoURLList)
    * return dataItem
  * askURL(URL)
    * return HTML
  * saveDataToXls(savePath, book, data, i)
  * ...

  

### 优化计划
等有空再做吧！
* 代码重构
  * 将bvList存放在文件中，避免测试时多次爬取
  * 其他代码重构
  
* 功能变化
  * 改变initial的运作方式，让他只运行一次
  * 增加**代理模块**让程序可以获得超过500条数据
  * 数据分析与可视化

  
