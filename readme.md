# README

## 杭电校园网自动认证

自用脚本，部署在Windows服务器能持续监测网络并自动登录。

这是方便实验室联网写的脚本，由于之前网上找的项目在我实验室没法登录，就用最傻瓜的方式爬虫实现了自动化认证程序。

缺点很多，体积大，占资源。但我反正是放win服务器上，就无所谓了。

## 使用

下载chrome驱动程序：https://developer.chrome.com/docs/chromedriver/downloads?hl=zh-cn
同级目录下创建 config.json ，见下面模板
双击直接运行，或将exe使用 nssm 注册为windows服务以便后台运行（推荐）
nssm下载地址：https://nssm.cc/download

```json
{
  "web_login_url": "",
  "chrome_drive_path": "chrome驱动程序路径",
  "chrome_exe_path": "chrome安装路径",
  "head_less": true,
  "ignore_ssl": true,
  "check_interval": 60,
  "username": "学号",
  "password": "密码"
}
```

## 打包

```bash
pip install -r requirements.txt
Pyinstaller HduWebHelper.py -F
```
