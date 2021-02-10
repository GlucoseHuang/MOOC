# MOOC

为广大学习通学子提供的刷毛概MOOC项目

### 项目结构

- back文件夹为MOOC.py代码备份

- getAnswer文件夹用于从已做完题的页面中批量读取答案

- screen文件夹为运行时的屏幕截图，用于找点

- source文件夹为题号1~20以及ABCDE截图

- answer.txt为毛概慕课答案

- html.txt为课程主页面地址（不同账号不一样）

- FindPic.py为找图模块，返回屏幕坐标

- MOOC.py为主程序

### 运行方式

- 运行前需要先将main中的html.txt内容替换为自己的课程页面

URL格式: http://mooc1.mooc.whu.edu.cn/mycourse/studentcourse?courseId=123456&clazzid=123456&enc=xxx&cpi=xxxx&vc=1

- run.bat为单次运行

- run2.bat为循环运行，用于刷学习次数