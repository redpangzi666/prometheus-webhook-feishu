# feishu alert
Generating feishu notification from Prometheus AlertManager WebHooks.
This project rely on python3.

## First
You must be have a self-built. This bot should have callback API.Follow this  https://open.feishu.cn/document/uQjL04CN/ukzM04SOzQjL5MDN

## Config
You must set some envs.

-  CHAT_ID: The name of feishu channel name. you can follow this api https://open.feishu.cn/open-apis/chat/v4/list
- APP_ID: Bot APP_ID
- APP_SECRET: Bot App Secret
- ALERTMANAER_URL: This for slience alerts.

## Install
### Building from source
To build Prometheus from source code, first ensure that have a working Python environment with version 3.6.
```
export CHAT_ID=xxx
export APP_ID=xxx
export APP_SECRET=xxx
export ALERTMANAER_URL=xxx
python feishu-alert.py
```
### Docker
```
docker build -t feishu-alert:latest .
docker run --name feishu-alert -d  feishu-alert:latest -e CHAT_ID=xxx -e APP_ID=xxx -e APP_SECRET=xxx -e ALERTMANAER_URL=xxx
```
