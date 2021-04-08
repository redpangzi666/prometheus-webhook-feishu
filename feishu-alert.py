from flask import Flask, request
import json
import requests
import os
from silence import callback_body
from common import generate_iris_post,generate_alertmanager_post,generate_label,generate_desc,generate_feishu_post,get_token,extra,labels_fields

app = Flask(__name__)

env_dist = os.environ
chat_id = env_dist.get("CHAT_ID")

@app.route('/',methods=['POST'])
def feishu_post():
    body = request.get_data()
    body = json.loads(body)
    print(body)
    status = body["status"]
    alertname =  body["alerts"][0]["labels"]["alertname"]
    cluster = body["alerts"][0]["labels"]["cluster"]
    alertname = status.capitalize()+": " + alertname
    labels = body["alerts"][0]["labels"]
    instance = labels.get("instance")
    description = body["alerts"][0]["annotations"].get("description")
    message = body["alerts"][0]["annotations"].get("message")
    prometheus_link = body["alerts"][0]["generatorURL"]
    prometheus = extra("Open Prometheus", "prometheus",prometheus_link)
    startsAt = body["alerts"][0]["startsAt"]
    content = []
    resolved_content = []
    actions = []
    fields = []
    overflow_options=[]
    delete_labels = {'job','team','alertname','owner','alert_channel','kubernetes_namespace','kubernetes_pod_name','pod_template_hash','severity','beta_kubernetes_io_os','failure_domain_beta_kubernetes_io_region','failure_domain_beta_kubernetes_io_zone','kubernetes_io_hostname','beta_kubernetes_io_instance_type','kops_k8s_io_instancegroup','beta_kubernetes_io_arch'}
    new_labels = {key:labels[key] for key in labels.keys()- delete_labels}
    for key,val in new_labels.items():
        info = generate_label(key.capitalize(),val)
        fields.append(info)


    label_div = labels_fields(fields)
    overflow_options.append(prometheus)

    resolved_content.append(label_div)
    if description:
        description = generate_desc("Description","**\n    "+description+"**",overflow_options)
        resolved_content.append(description)
    if message:
        message = generate_label("Description",message)
        resolved_content.append(message)

    silence_body = callback_body(labels, startsAt, cluster)
    alertmanager_body = generate_alertmanager_post(silence_body,chat_id)
    actions.append(alertmanager_body)
    actions_info = {"actions": actions, "tag": "action"}
    content.extend(resolved_content)
    if status == "firing":
        content.append(actions_info)
    data = generate_feishu_post(alertname,status,content)
    post_feishu(data)

    return data



def post_feishu(data):
    env_dist = os.environ
    url = "https://open.feishu.cn/open-apis/message/v4/send/"
    data["chat_id"] = chat_id
    token = get_token()
    header = {"Authorization":token,"Content-Type":"application/json"}
    data = json.dumps(data)
    rep = requests.post(url,data=data,headers=header)
    print(rep.text)



if __name__ == '__main__':
    app.run(
      host='0.0.0.0',
      port= 5000,
      debug=True
    )