# 项目简介
**第九届中国软件杯大学生软件设计大赛决赛作品**

本项目是一个基于机器学习（图像识别）技术的企业实体识别软件系统

实现对店铺门面招牌照片上的企业实体名称探测、文字识别和简单查证功能

# 项目组成
srvbase_qcc：企航企业实体名称识别服务端

client_qcc：企航Web应用

client_qcc_app：企航移动端App（实现随手拍照识别）

# 运行环境
> python>=3.7<br>
tensorflow==1.14.0<br>
tensorflow-gpu==1.14.0<br>
tensorpack==0.9.8<br>
keras==2.1.4<br>
pycocotools<br>
**gast==0.2.2**<br>

# 效果展示
## uni-app端拍照查证
![手机端](https://github.com/xiaobao520123/EnterpriseNavigator/blob/main/APP%E9%9A%8F%E6%89%8B%E6%8B%8D%E7%85%A7%E6%9F%A5%E8%AF%81.gif)

## Web端批量识别
![Web端](https://github.com/xiaobao520123/EnterpriseNavigator/blob/main/Web%E7%AB%AF%E6%89%B9%E9%87%8F%E8%AF%86%E5%88%AB.gif)

# 参考
[AdvancedEAST](https://github.com/huoyijie/AdvancedEAST)

[AttentionOCR](https://github.com/zhang0jhon/AttentionOCR)

[Materialize](https://github.com/Dogfalo/materialize)
