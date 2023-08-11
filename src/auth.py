import requests
import json

from .. import CFG_FILE as cfg


auth_url = f"/v1/authentication"

def get_env(env=None):

    # Get environment configuration
    env_msg = ""
    if env is None:
        env_id = str(cfg['AA']['default_cr'])
        env_msg = f"No env specified, using default"
    else:
        env_msg = f"Env specified, using"
        env_id = env
    
    for i in cfg['AA']['env_list']:
        if i['name'] == env_id:
            env_data = i
            print(f"{env_msg} environment: [bold]{env_data['name']}[/bold]", style="dark_goldenrod")

    # Get token for environment
    token = aa_token(env=env,env_data=env_data)    

    # Get headers for environment
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "X-Authorization": token
    }
    
    # Add headers and token to env_data
    env_data.update({
        "headers": headers,
        "token": token})

    return env_data

def aa_token(env,env_data=None):
    if env_data is None: env_data=get_env(env=env)
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = {
        "username": env_data['userid'],
        "apiKey": env_data['api_key']
    }
    response = requests.post(f"{env_data['endpoint']}{auth_url}", headers=headers, json=payload)
    resp_obj = response.json()
    return resp_obj['token']