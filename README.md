<p align="center">
	<img alt="logo" src="https://oscimg.oschina.net/oscnet/up-d3d0a9303e11d522a06cd263f3079027715.png">
</p>
<h1 align="center" style="margin: 30px 0 30px; font-weight: bold;">Dash-FastAPI-Admin v1.0.2</h1>
<h4 align="center">基于Dash+FastAPI前后端分离的纯Python快速开发框架</h4>
<p align="center">
	<a href="https://gitee.com/insistence2022/dash-fastapi-admin/stargazers"><img src="https://gitee.com/insistence2022/dash-fastapi-admin/badge/star.svg?theme=dark"></a>
	<a href="https://gitee.com/insistence2022/dash-fastapi-admin"><img src="https://img.shields.io/badge/DashFastAPIAdmin-v1.0.2-brightgreen.svg"></a>
	<a href="https://gitee.com/insistence2022/dash-fastapi-admin/blob/master/LICENSE"><img src="https://img.shields.io/github/license/mashape/apistatus.svg"></a>
</p>

## 平台简介

Dash-FastAPI-Admin是一套全部开源的快速开发平台，毫无保留给个人及企业免费使用。

* 前端采用Dash、feffery-antd-components、feffery-utils-components。
* 后端采用FastAPI、sqlalchemy、MySQL、Redis、OAuth2 & Jwt。
* 权限认证使用OAuth2 & Jwt，支持多终端认证系统。
* 支持加载动态权限菜单，多方式轻松权限控制。
* 特别鸣谢：<u>[RuoYi-Vue](https://gitee.com/y_project/RuoYi-Vue)</u> ，<u>[feffery-antd-components](https://github.com/CNFeffery/feffery-antd-components)</u>，<u>[feffery-utils-components](https://github.com/CNFeffery/feffery-utils-components)</u>。

## 内置功能

1.  用户管理：用户是系统操作者，该功能主要完成系统用户配置。
2.  角色管理：角色菜单权限分配。
3.  菜单管理：配置系统菜单，操作权限，按钮权限标识等。
4.  部门管理：配置系统组织机构（公司、部门、小组）。
5.  岗位管理：配置系统用户所属担任职务。
6.  字典管理：对系统中经常使用的一些较为固定的数据进行维护。
7.  参数管理：对系统动态配置常用参数。
8.  通知公告：系统通知公告信息发布维护。
9.  操作日志：系统正常操作日志记录和查询；系统异常信息日志记录和查询。
10. 登录日志：系统登录日志记录查询包含登录异常。
11. 在线用户：当前系统中活跃用户状态监控。
12. 定时任务：在线（添加、修改、删除）任务调度包含执行结果日志。
13. 服务监控：监视当前系统CPU、内存、磁盘、堆栈等相关信息。
14. 缓存监控：对系统的缓存信息查询，命令统计等。
15. 系统接口：根据业务代码自动生成相关的api接口文档。

## 演示图

<table>
    <tr>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/%E7%99%BB%E5%BD%95.png"/></td>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/%E5%BF%98%E8%AE%B0%E5%AF%86%E7%A0%81.png"/></td>
    </tr>
    <tr>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/%E7%94%A8%E6%88%B7%E7%AE%A1%E7%90%86.png"/></td>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/%E8%A7%92%E8%89%B2%E7%AE%A1%E7%90%86.png"/></td>
    </tr>
    <tr>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/%E8%8F%9C%E5%8D%95%E7%AE%A1%E7%90%86.png"/></td>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/%E9%83%A8%E9%97%A8%E7%AE%A1%E7%90%86.png"/></td>
    </tr>
    <tr>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/%E5%B2%97%E4%BD%8D%E7%AE%A1%E7%90%86.png"/></td>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/%E5%AD%97%E5%85%B8%E7%AE%A1%E7%90%86.png"/></td>
    </tr>	 
    <tr>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/%E5%8F%82%E6%95%B0%E8%AE%BE%E7%BD%AE.png"/></td>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/%E9%80%9A%E7%9F%A5%E5%85%AC%E5%91%8A.png"/></td>
    </tr>
    <tr>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/%E6%93%8D%E4%BD%9C%E6%97%A5%E5%BF%97.png"/></td>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/%E7%99%BB%E5%BD%95%E6%97%A5%E5%BF%97.png"/></td>
    </tr>
    <tr>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/%E5%9C%A8%E7%BA%BF%E7%94%A8%E6%88%B7.png"/></td>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/%E5%AE%9A%E6%97%B6%E4%BB%BB%E5%8A%A1.png"/></td>
    </tr>
    <tr>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/%E6%9C%8D%E5%8A%A1%E7%9B%91%E6%8E%A7.png"/></td>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/%E7%BC%93%E5%AD%98%E7%9B%91%E6%8E%A7.png"/></td>
    </tr>
    <tr>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/%E7%B3%BB%E7%BB%9F%E6%8E%A5%E5%8F%A3.png"></td>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/%E4%B8%AA%E4%BA%BA%E8%B5%84%E6%96%99.png"/></td>
    </tr>
</table>

## 项目运行相关

```bash
# 克隆项目
git clone https://gitee.com/insistence2022/dash-fastapi-admin.git

# 进入项目根目录
cd Dash-FastAPI-Admin

# 安装项目依赖环境
pip3 install -r requirements.txt
```

### 前端
```bash
# 进入前端目录
cd dash-fastapi-frontend

# 运行前端
python3 wsgi.py
```

### 后端
```bash
# 进入后端目录
cd dash-fastapi-backend

# 配置环境
1.在config/env.py的DataBaseConfig类中配置数据库环境
2.在config/env.py的RedisConfig类中配置redis环境

# 运行sql文件
1.新建数据库dash-fastapi(默认，可修改)
2.使用命令或数据库连接工具运行sql文件夹下的dash-fastapi.sql

# 运行后端
python3 app.py
```

### 访问
```bash
# 默认账号密码
账号：admin
密码：admin123

# 浏览器访问
地址：http://127.0.0.1:8088
```

## 交流与赞助
如果有对本项目及FastAPI感兴趣的朋友，欢迎加入知识星球一起交流学习，让我们一起变得更强。如果你觉得这个项目帮助到了你，你可以请作者喝杯咖啡表示鼓励☕。
<table>
    <tr>
        <td><img alt="zsxq" src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/zsxq.jpg"></td>
        <td><img alt="zanzhu" src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/zanzhu.jpg"></td>
    </tr>
</table>