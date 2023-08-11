import requests
import json

from auth import *


def startBot(bot_id: int,run_as: int,env=None,pool_ids=None,input_name=None,auto_name=None,input=None):
    ### Get Environment Data ###
    cr=get_env(env=env)
    if auto_name is None:
        auto_name = f"YDA API - {cfg['env_name']} - startBot"
    req_body = {"fileId": bot_id, 
                "automationName": auto_name, 
                "runAsUserIds": run_as,
                "numOfRunAsUsersToUse": 1,
                }
    if pool_ids is not None:
        req_body.update({
                "poolIds": pool_ids,
                "overrideDefaultDevice": True})
    if isinstance(input,dict): 
        req_body['automationName'] = f"YDA API - {cfg['env_name']} - {input_name}"
        req_body['botInput'] = input
    if isinstance(input,list):
        req_body.update['automationName'] = f"YDA API - {cfg['env_name']} - 'list: {input_name}'"
        list_input = { f"{input_name}": {
                      "type": "string", 
                      "string": input.join(",")}}
        req_body['botInput'] = list_input
    if isinstance(input,str):
        req_body['automationName'] = f"YDA API - {cfg['env_name']} - {input}"
        req_body['botInput'] = { "type": "string",
                                 "string": input}
        
    req_data = json.dumps(req_body)
        
    response = requests.post(f"{cr['endpoint']}/v3/automations/deploy", headers=cr['headers'], data=req_data)
    resp_obj = response.json()
    resp_obj.update({"status_code": response.status_code})
    print(f"### BOT {bot_id} DEPLOY REQUEST ###")
    print(json.dumps(req_body, indent=2))
    print(f"### BOT {bot_id} DEPLOY RESPONSE ###")
    if response.status_code == 200:
        print(f"Bot {bot_id} launched successfully")
    else:
        print(f"Failed to launch bot {bot_id}")
    print(json.dumps(resp_obj, indent=2))
    print(f"### END BOT {bot_id} DEPLOY REQUEST ###")
    return resp_obj

def getBotStatus(deploymentId: str,env=None):
    cr=get_env(env=env)
    url = f"{env['endpoint']}/v3/activity/execution/{deploymentId}"
    print(f"### BOT {deploymentId} STATUS REQUEST ###")
    print(f"GET {url}")
    response = requests.get(url, headers=cr['headers'])
    print(response)
    print(f"### BOT {deploymentId} STATUS RESPONSE ###")
    if response.status_code == 200:
        print(f"Bot {deploymentId} status request successful")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Failed to get status for bot {deploymentId}")
    print(f"### END BOT {deploymentId} STATUS REQUEST ###")
    return response