<p align="center">
	<img alt="logo" src="https://oscimg.oschina.net/oscnet/up-d3d0a9303e11d522a06cd263f3079027715.png">
</p>
<h1 align="center" style="margin: 30px 0 30px; font-weight: bold;">Dash-FastAPI v1.0.0</h1>
<h4 align="center">基于Dash+FastAPI前后端分离的纯Python快速开发框架</h4>
<p align="center">
	<a href="https://gitee.com/y_project/RuoYi-Vue/stargazers"><img src="https://gitee.com/insistence2022/dash-fastapi/badge/star.svg?theme=dark"></a>
	<a href="https://gitee.com/insistence2022/dash-fastapi"><img src="https://img.shields.io/badge/DashFastAPI-v1.0.0-brightgreen.svg"></a>
	<a href="https://gitee.com/insistence2022/dash-fastapi/blob/master/LICENSE"><img src="https://img.shields.io/github/license/mashape/apistatus.svg"></a>
</p>

## 平台简介

Dash-FastAPI是一套全部开源的快速开发平台，毫无保留给个人及企业免费使用。

* 前端采用Dash、feffery-antd-components、feffery-utils-components。
* 后端采用FastAPI、sqlalchemy、Redis & Jwt。
* 权限认证使用Jwt，支持多终端认证系统。
* 支持加载动态权限菜单，多方式轻松权限控制。
* 特别鸣谢：<u>[RuoYi](https://gitee.com/y_project/RuoYi-Vue)</u> ，[feffery-antd-components](https://github.com/CNFeffery/feffery-antd-components)，[feffery-utils-components](https://github.com/CNFeffery/feffery-utils-components)。

## 内置功能

1.  用户管理：用户是系统操作者，该功能主要完成系统用户配置。
2.  部门管理：配置系统组织机构（公司、部门、小组）。
3.  岗位管理：配置系统用户所属担任职务。
4.  菜单管理：配置系统菜单，操作权限，按钮权限标识等。
5.  角色管理：角色菜单权限分配。
6.  字典管理：对系统中经常使用的一些较为固定的数据进行维护。
7.  参数管理：对系统动态配置常用参数。
8.  通知公告：系统通知公告信息发布维护。
9.  操作日志：系统正常操作日志记录和查询；系统异常信息日志记录和查询。
10. 登录日志：系统登录日志记录查询包含登录异常。
11. 在线用户：当前系统中活跃用户状态监控。
12. 定时任务：在线（添加、修改、删除)任务调度包含执行结果日志。
13. 系统接口：根据业务代码自动生成相关的api接口文档。
14. 服务监控：监视当前系统CPU、内存、磁盘、堆栈等相关信息。
15. 缓存监控：对系统的缓存信息查询，命令统计等。

## 演示图

<table>
    <tr>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi/blob/develop/demo-pictures/%E7%99%BB%E5%BD%95.png"/></td>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi/blob/develop/demo-pictures/%E5%BF%98%E8%AE%B0%E5%AF%86%E7%A0%81.png"/></td>
    </tr>
    <tr>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi/blob/develop/demo-pictures/%E7%94%A8%E6%88%B7%E7%AE%A1%E7%90%86.png"/></td>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi/blob/develop/demo-pictures/%E8%A7%92%E8%89%B2%E7%AE%A1%E7%90%86.png"/></td>
    </tr>
    <tr>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi/blob/develop/demo-pictures/%E8%8F%9C%E5%8D%95%E7%AE%A1%E7%90%86.png"/></td>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi/blob/develop/demo-pictures/%E9%83%A8%E9%97%A8%E7%AE%A1%E7%90%86.png"/></td>
    </tr>
    <tr>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi/blob/develop/demo-pictures/%E5%B2%97%E4%BD%8D%E7%AE%A1%E7%90%86.png"/></td>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi/blob/develop/demo-pictures/%E5%AD%97%E5%85%B8%E7%AE%A1%E7%90%86.png"/></td>
    </tr>	 
    <tr>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi/blob/develop/demo-pictures/%E5%8F%82%E6%95%B0%E8%AE%BE%E7%BD%AE.png"/></td>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi/blob/develop/demo-pictures/%E9%80%9A%E7%9F%A5%E5%85%AC%E5%91%8A.png"/></td>
    </tr>
    <tr>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi/blob/develop/demo-pictures/%E6%93%8D%E4%BD%9C%E6%97%A5%E5%BF%97.png"/></td>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi/blob/develop/demo-pictures/%E7%99%BB%E5%BD%95%E6%97%A5%E5%BF%97.png"/></td>
    </tr>
    <tr>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi/blob/develop/demo-pictures/%E5%9C%A8%E7%BA%BF%E7%94%A8%E6%88%B7.png"/></td>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi/blob/develop/demo-pictures/%E5%AE%9A%E6%97%B6%E4%BB%BB%E5%8A%A1.png"/></td>
    </tr>
    <tr>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi/blob/develop/demo-pictures/%E6%9C%8D%E5%8A%A1%E7%9B%91%E6%8E%A7.png"/></td>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi/blob/develop/demo-pictures/%E7%BC%93%E5%AD%98%E7%9B%91%E6%8E%A7.png"/></td>
    </tr>
    <tr>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi/blob/develop/demo-pictures/%E7%B3%BB%E7%BB%9F%E6%8E%A5%E5%8F%A3.png"/></td>
    </tr>
</table>