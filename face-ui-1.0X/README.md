<p align="center">
    <img src="./logo.png" width="140" height="140" alt="easy-jenkins logo" title="Easy Jenkins - 一键部署工具" />
</p>
<h1 align="center">FACE-UI</h1>

<p align="center">
    <strong>基于前后端分离的Web端人脸登录解决方案</strong>
</p>

<p align="center">
  <a href="#"><img src="https://img.shields.io/badge/Spring%20Boot-2.6.0-brightgreen.svg" alt="Spring Boot 2.6.0"></a>
  <a href="#"><img src="https://img.shields.io/badge/MySQL-8.0.27-blue.svg" alt="MySQL 8.0.27"></a>
  <a href="#"><img src="https://img.shields.io/badge/Vue-2.6.14-brightgreen.svg" alt="Vue 2.6.14"></a>
  <a href="#"><img src="https://img.shields.io/badge/Node-16.18.0-green.svg" alt="Node 16.18.0"></a>
</p>


## 🌟 项目介绍

FACE-UI 是一个基于前后端分离架构的Web端项目，专注于提供网页版的人脸登录功能。通过调取前端摄像头拍照，并将照片传入后端进行与数据库中人脸库的相似度比对，我们能够实现安全快捷的身份验证。

## ✅ 增值版本

详细使用查看：[face-ui 增值版本](https://blog.csdn.net/Susan003/article/details/136912278)

### ✨ 主要功能

- **人脸列表CRUD**：管理和操作人脸数据。
- **日志列表CRUD**：记录和查询登录日志。
- **人脸库管理**：基于自建人脸库，通过base64编码方式存储人脸图片。
- **腾讯云人脸对比API**：通过调用腾讯云API实现高效的人脸对比功能。

## 🛠 工程介绍

### 1. face-easy (后端SpringBoot工程)

- **项目地址**：[susantyp/face-easy (gitee.com)](https://gitee.com/susantyp/face-easy)
- **主要步骤**：
  - 拉取相关代码
  - 在工程`sql`文件夹下有基于mysql的sql脚本
  - 在`application.yml`文件中配置腾讯云的`secretId`和`secretKey`
  - 选购并配置腾讯云人脸对比api

### 2. face-ui (前端Vue 2.x 工程)

- **项目地址**：[susantyp/face-ui (gitee.com)](https://gitee.com/susantyp/face-ui)
- **主要步骤**：
  - 拉取相关代码
  - `npm install` 安装相关依赖
  - `npm run serve` 运行服务
  - 浏览器初次访问时需授权摄像头权限

## 📘 演示讲解

详细使用教程请参见：[face-ui 详细使用教程](https://blog.csdn.net/Susan003/article/details/125920408)


## 📚 如何配置腾讯云？

为了使用腾讯云人脸对比API，您需要进行一些配置。详情请参考[官方文档](https://blog.csdn.net/Susan003/article/details/125914027?spm=1001.2014.3001.5502)。

## 🤝 贡献

欢迎通过 Pull Requests 或 Issues 参与贡献，让项目更加完美。

## 📄 许可证

本项目采用 Apache-2.0。

## 📬 联系方式

如有任何问题或建议，请通过 [Gitee Issues](https://gitee.com/susantyp/face-easy/issues) 联系我们。

---

感谢您对FACE-UI项目的关注，期待您的贡献和反馈！
