# 课表生成手机日历小工具

[![](https://img.shields.io/github/stars/BarryZZJ/ucas_course_to_calendar.svg)](https://github.com/barryZZJ/ucas_course_to_calendar)

## 效果展示

- 脚本运行过程：

  <img src="/demo/demo.jpg" style="zoom:67%;" />

- 导入手机后的效果：

  <img src="/demo/demo2.jpg" style="width:300px;" />



## 简介

本脚本会根据课表信息，自动生成`.ics`文件（[iCalendar](https://baike.baidu.com/item/iCal/10119576), 一种日历格式标准），安卓与苹果通用，可以直接导入到手机日历。

## 使用方法

### 获取cookie

需要`jwxk.ucas.ac.cn`域名下名为`JSESSIONID`的cookie，获取方法：

1. 浏览器进入选课系统
2. 按`F12`打开开发者工具
3. 如图（以chrome为例），依次找到`Application - Cookies - JSESSIONID`（注意对应的域名要选`jwxk.ucas.ac.cn`的）：
![](/demo/cookie.jpg)



### 运行脚本

1. 进入[releases页面](https://github.com/barryZZJ/ucas_course_to_calendar/releases)下载可执行文件；
2. 启动后根据提示分别输入本学期第一天的年月日，以及JSESSIONID的值。
    可选参数：`-o FILE`，可指定输出文件名，默认为`courses.ics`。
3. 脚本同目录下获得`courses.ics`文件。

### 导入手机

- **苹果：** 把`.ics`文件发送给手机（必须以**邮件**的方式发送给自己，并用**系统自带的邮件APP**打开），在邮件中打开附件，即可导入。
- **安卓：** 把`.ics`文件发送给手机，并使用系统自带的日历程序打开（如华为系统叫"华为日历"），即可导入。

### 提示

导入时建议新建一个日历账户，这样可以跟自己手动添加的日程区分开，方便统一隐藏或删除，还能设置不同颜色。

## 使用Python运行

### 配置环境

```sh
pip install requests
pip install beautifulsoup4
```

### 运行脚本

```sh
python3 main.py
```

## Cahngelog

`v1.3`: 增加可选参数`-o FILE`

`v1.2`: 修复了第12节课时长显示出错的BUG。

`v1.1`: 降低使用门槛，获取用户信息写在了运行脚本之后。

`v1.0`: 初版

## 结语

[![](https://img.shields.io/github/followers/BarryZZJ.svg?style=social&label=Follow&maxAge=2592000)](https://github.com/barryZZJ) 关注我，方便获取最新脚本动态~
