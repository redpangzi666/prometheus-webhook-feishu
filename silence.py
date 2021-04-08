import datetime
import time
import json
import requests
from common import generate_reply
import os

def silence_body(name,value):
    match = {
        "name": name,
        "value": value,
        "isRegex": False
    }
    return match

def callback_body(labels,starts,cluster):
    silence_body = make_silence_body(labels,starts,cluster)

    return silence_body

def make_silence_body(labels,starts,cluster):
    matchers = []
    for key,val in labels.items():
        matchs = silence_body(key,val)
        matchers.append(matchs)
    startsAt = starts
    comment = "Slience 4h"
    createdBy = "Rule Owner"
    alerts={
            "matchers": matchers,
            "startsAt": startsAt,
            "comment": comment,
            "createdBy": createdBy,
            "cluster": cluster
        }
    return alerts


def silence(silence_body,root_id,chat_id,token,option):
    cluster = silence_body["cluster"]
    time1 = option.split(' ')
    time1.pop()
    end_At = ' '.join(time1)
    timeArray = time.strptime(end_At, "%Y-%m-%d %H:%M")
    timeStamp = int(time.mktime(timeArray))

    endsAt = datetime.datetime.utcfromtimestamp(timeStamp-8*3600).isoformat()
    print(time1,end_At,endsAt)
    json = {
        "matchers": silence_body["matchers"],
        "startsAt": silence_body["startsAt"],
        "endsAt": endsAt,
        "comment": silence_body["comment"],
        "createdBy": silence_body["createdBy"],
        }

    env_dist = os.environ
    url = env_dist.get("ALERTMANAER_URL")


    rep = requests.post(url, json=json)
    text = "已经静默到 "+ end_At
    reply_body = generate_reply(root_id, chat_id, text)
    print(reply_body)
    reply_alert(reply_body, token)
    return (rep.text)


def reply_alert(reply_body, token):
    url = "https://open.feishu.cn/open-apis/message/v4/send/"
    header = {"Authorization": token, "Content-Type": "application/json"}
    rep = requests.post(url,data=json.dumps(reply_body), headers=header)
    print(rep.text)