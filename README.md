<p align="center">
	<img alt="logo" src="https://oscimg.oschina.net/oscnet/up-d3d0a9303e11d522a06cd263f3079027715.png">
</p>
<h1 align="center" style="margin: 30px 0 30px; font-weight: bold;">Dash-FastAPI-Admin v1.4.0</h1>
<h4 align="center">基于Dash+FastAPI前后端分离的纯Python快速开发框架</h4>
<p align="center">
	<a href="https://gitee.com/insistence2022/dash-fastapi-admin/stargazers"><img src="https://gitee.com/insistence2022/dash-fastapi-admin/badge/star.svg?theme=dark"></a>
    <a href="https://github.com/insistence/Dash-FastAPI-Admin"><img src="https://img.shields.io/github/stars/insistence/Dash-FastAPI-Admin?style=social"></a>
	<a href="https://gitee.com/insistence2022/dash-fastapi-admin"><img src="https://img.shields.io/badge/DashFastAPIAdmin-v1.4.0-brightgreen.svg"></a>
	<a href="https://gitee.com/insistence2022/dash-fastapi-admin/blob/master/LICENSE"><img src="https://img.shields.io/github/license/mashape/apistatus.svg"></a>
    <img src="https://img.shields.io/badge/python-3.8 | 3.9-blue">
    <img src="https://img.shields.io/badge/MySQL-≥5.7-blue">
</p>






## 平台简介

Dash-FastAPI-Admin是一套全部开源的快速开发平台，毫无保留给个人及企业免费使用。

* 前端采用Dash、feffery-antd-components、feffery-utils-components。
* 后端采用FastAPI、sqlalchemy、MySQL、Redis、OAuth2 & Jwt。
* 权限认证使用OAuth2 & Jwt，支持多终端认证系统。
* 支持加载动态权限菜单，多方式轻松权限控制。
* Vue2版本：
  - Gitte仓库地址：https://gitee.com/insistence2022/RuoYi-Vue-FastAPI
  - GitHub仓库地址：https://github.com/insistence/RuoYi-Vue-FastAPI
* Vue3版本：
  - Gitte仓库地址：https://gitee.com/insistence2022/RuoYi-Vue3-FastAPI
  - GitHub仓库地址：https://github.com/insistence/RuoYi-Vue3-FastAPI
* 特别鸣谢：<u>[RuoYi-Vue](https://gitee.com/y_project/RuoYi-Vue)</u> ，<u>[feffery-antd-components](https://github.com/CNFeffery/feffery-antd-components)</u>，<u>[feffery-utils-components](https://github.com/CNFeffery/feffery-utils-components)</u>。

## 内置功能

1.  用户管理：用户是系统操作者，该功能主要完成系统用户配置。
2.  角色管理：角色菜单权限分配、设置角色按机构进行数据范围权限划分。
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
        <td><img src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/%E7%BC%93%E5%AD%98%E5%88%97%E8%A1%A8.png"></td>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/%E7%B3%BB%E7%BB%9F%E6%8E%A5%E5%8F%A3.png"></td>
    </tr>
    <tr>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/%E9%A6%96%E9%A1%B5.png"></td>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/%E4%B8%AA%E4%BA%BA%E8%B5%84%E6%96%99.png"/></td>
    </tr>
</table>

## 在线体验
- *账号：admin*
- *密码：admin123*
- 演示地址：<a href="https://dfadmin.insistence.tech">dfadmin管理系统<a>

## 项目开发及发布

```bash
# 克隆项目
git clone https://gitee.com/insistence2022/dash-fastapi-admin.git

# 进入项目根目录
cd dash-fastapi-admin

# 安装项目依赖环境
pip3 install -r requirements.txt
```

### 开发

#### 前端
```bash
# 进入前端目录
cd dash-fastapi-frontend

# 配置应用信息
在.env.dev文件中配置应用开发模式的相关信息

# 运行前端
python3 app.py --env=dev
```

#### 后端
```bash
# 进入后端目录
cd dash-fastapi-backend

# 配置环境
1.在.env.dev文件中配置开发模式的数据库环境
2.在.env.dev文件中配置开发模式的redis环境

# 运行sql文件
1.新建数据库dash-fastapi(默认，可修改)
2.使用命令或数据库连接工具运行sql文件夹下的dash-fastapi.sql

# 运行后端
python3 app.py --env=dev
```

### 发布

本应用发布建议使用nginx部署，nginx代理配置参考如下：

```bash
server {
    location / {
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header REMOTE-HOST $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_pass http://127.0.0.1:8088/;
    }

    location /prod-api {
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header REMOTE-HOST $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_pass http://127.0.0.1:9099/;
        rewrite ^/prod-api/(.*)$ /$1 break;
    }

    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   html;
    }
}
```

#### 前端
```bash
# 进入前端目录
cd dash-fastapi-frontend

# 配置应用信息
在.env.prod文件中配置应用发布的相关信息，注意：APP_BASE_URL需要配置为nginx代理的地址，例如上面的nginx代理监听的是8000端口，则APP_BASE_URL需要配置为http://127.0.0.1:8000

# 运行前端
python3 wsgi.py --env=prod
```

#### 后端
```bash
# 进入后端目录
cd dash-fastapi-backend

# 配置环境
1.在.env.prod文件中配置生产模式的数据库环境
2.在.env.prod文件中配置生产模式的redis环境

# 运行sql文件
1.新建数据库dash-fastapi(默认，可修改)
2.使用命令或数据库连接工具运行sql文件夹下的dash-fastapi.sql

# 运行后端
python3 app.py --env=prod
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
如果有对本项目及FastAPI感兴趣的朋友，欢迎加入知识星球一起交流学习，让我们一起变得更强。如果你觉得这个项目帮助到了你，你可以请作者喝杯咖啡表示鼓励☕。扫描下面微信二维码添加微信备注DF-Admin即可进群，也欢迎大家加入dash大神费弗里的知识星球学习更多dash开发知识。
<table>
    <tr>
        <td><img alt="zsxq" src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/zsxq.jpg"></td>
        <td><img alt="zanzhu" src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/zanzhu.jpg"></td>
    </tr>
    <tr>
        <td><img alt="wxcode" src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/wxcode.jpg"></td>
        <td><img alt="dashzsxq" src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/dashzsxq.jpg"></td>
    </tr>
</table>