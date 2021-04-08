import json
import requests

def generate_feishu_post(alertname,status,elements):
    if status == "firing":
        template = "red"
    else:
        template = "green"
    data ={
        "msg_type": "interactive",
        "card": {
            "config": {
                "wide_screen_mode": True,
                "enable_forward": True
            },
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": alertname
                },
                "template": template
            },
            "elements": elements
        }
    }
    return data

# div
def labels_fields(fields):
    label_div = {
                "tag": "div",
                "text": {
                    "tag": "plain_text",
                    "content": ""
                },
                "fields": fields
    }
    return label_div

def generate_label(key, val):
    label = {
        "is_short": False,
        "text": {
            "tag": "lark_md",
            "content": "**" + key + ": **" + val
        }
    }
    return label

# describe
def generate_desc(key, val,options):
    label = {
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": "**" + key + ": **" + val
        },
        "extra": {
            "tag": "overflow",
            "options": options
        }
    }
    return label

#alert post  button
def generate_alertmanager_post(silence_body,chat_id):
    alert_body = {
            # "tag": "button",
            # "text":{
            #                 "tag":"lark_md",
            #                 "content": "静默 4h"
            #             },
            # "type": "primary",
        "tag": "picker_datetime",
        "placeholder": {
            "tag": "plain_text",
            "content": "选择静默时间"
        },
        "confirm": {
            "title": {
                "tag": "plain_text",
                "content": "静默"
            },
            "text": {
                "tag": "plain_text",
                "content": "确认静默该告警?"
            }
        },
        "value": {
            "silence_body": silence_body,
            "chat_id": chat_id
            }
        }

    return alert_body

# iris button
def generate_iris_post(iris_plan,cliam_body,chat_id):
    iris_body = {
            "tag": "button",
            "text":{
                            "tag":"lark_md",
                            "content": "Iris Cliam"
                        },
            "type": "primary",
            "value": {
                "claim_body": cliam_body,
                "iris_plan": iris_plan,
                "chat_id": chat_id
            }
        }
    return iris_body

#overflow
def extra(text,anno,link):
    overflow = {
        "text": {
            "tag": "plain_text",
            "content": text
        },
        "value": anno,
        "url": link
    }
    return overflow


#reply body
def generate_reply(root_id,chat_id,text):
    reply = {
        "chat_id": chat_id,
        "root_id": root_id,
        "msg_type":"text",
        "content":{
            "text": text
        }
    }
    return reply

#get t token
def get_token():
    url  = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
    env_dist = os.environ
    app_id = env_dist.get("APP_ID")
    app_secret = env_dist.get("APP_SECRET")
    body = {
        "app_id": app_id,
        "app_secret": app_secret
    }
    rep = requests.post(url,data=json.dumps(body))
    data = json.loads(rep.text)
    token = "Bearer "+ data.get("tenant_access_token")
    return token