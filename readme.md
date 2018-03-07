
## 微信开发者第三方平台消息与事件监听服务器
### 结合图灵机器人api接口,实现微信公众号机器人自动聊天功能 （微信关注 郑跃的订阅号 可查看效果）
### 由微信官方提供的代码改动而来，实现快速开发

### 语言 python2.7
### web框架 web.py

### 部署
#### 1.安装依赖包  pip install -r requirements.txt
#### 2.进入目录wechat_listener/pycrypto-2.6.1 安装依赖  先执行 python setup.py build 再执行 python setup.py build
#### 3.修改config/config.json，配置mongodb，配置微信开放平台appId，token，encodingAESKey

### 第三方平台发布覆盖时 检测使用
#### 启动：python main_for_access.py 8081 dev


### 本地环境:
#### 启动: python main.py 8081 dev

### 微信开发者配置的消息接受地址

#### http://ccc.intbee.com/wechat/thirdpart/events/listen/(.*?)

### ngxin配置反向代理

location ^~ /wechat/thirdpart/events/listen/ {
    proxy_pass http://192.168.1.59:8081/wechat/thirdpart/events/listen/;
}


### 开发者平台消息与事件监听接口主文件 thirdPartHandle.py
