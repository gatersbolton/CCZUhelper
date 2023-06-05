# 常大小助手

帮助常大学子更加便捷的获取自己的教务系统的信息。

## 软件介绍

随着信息技术的发展，学校教务系统已经成为学生、教师、教务管理人员必不可少的工具。但是，由于不同学校教务系统的差异，使用不便的情况也时有发生。为了解决这一问题，我们计划开发一个基于Python爬虫技术的学校教务系统接入工具，方便用户使用。

## 下载安装

- 系统要求:Windows
- 下载地址:  https://github.com/gatersbolton/CCZUhelper
- 解压后双击 `CCZU助手` 即可运行

## 使用方法

### 	1.**Windows平台**

1. 输入常州大学教务系统的账户和密码，点击登录
2. 登陆成功后
   1. 教务系统查分
      1. 点击后出现所有科目的分数
      2. 点击保存即可保存成绩单
   2. 图书馆预约
      1. 勾选`今天`或`明天`
      2. 下拉选择开始时间
      3. 下拉选择时长，最多时长4小时
      4. 填写座位号

### 	2.QQ用户

1. 查询QQ号,添加好友
2. 根据一下命令行输入选择功能

```
lib -a 1 -c 1 # 取消预约
lib -t 18 -d 1 -a 1 -s 1 # -t 18 表示 预约时间为 18.00
						 # -d 1  表示	预约	今天
						 # -a 1  表示 使用的预约账户为第一个
						 # -s 1  表示 预约的座位号是1号
						 # 我们默认的位置是：武进校区的三楼阅读空的位置
						 
						 
# 下面是有关QQ BOT的命令行
喜报 ***  # 生成一张带有***的喜报的表情包
拍 ***    # 生成一张拍某某QQ头像的表情包
```

![image-20230605161620010](C:\Users\fred\AppData\Roaming\Typora\typora-user-images\image-20230605161620010.png)

![image-20230605162512167](C:\Users\fred\AppData\Roaming\Typora\typora-user-images\image-20230605162512167.png)

### 	2.微信用户

1. 通过扫码添加好友，或者搜索公众号关注
2. 发送一下关键词，



![img](file:///C:/Users/fred/AppData/Local/Temp/msohtmlclip1/01/clip_image002.jpg)



## 更新日志

- 1.0.0版本:
  - 实现基本功能
  - QQ BOT和Windows版本的开发可以初步投入使用

## 局限与问题

- 公众号的前端还没有和后端接入，

- 一开始定的目标功能还没有完全实现

- 用户界面过于粗糙

  

## 参与贡献

欢迎通过以下渠道参与改进:

- 在 GitHub 上fork 并提交 Pull Request
- 给项目提供建议和Issue
- 项目服务器端源码：https://github.com/gatersbolton/Server
- 项目Windows段源码：https://github.com/gatersbolton/CCZUhelper
