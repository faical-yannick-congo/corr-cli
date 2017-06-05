import httplib
import json
import traceback
import requests
import ssl as sslAgent
from io import BytesIO

def conn_generator(host_full, port):
    blocks = host_full.split("://")
    host = blocks[1]
    ssl = True if "https" == blocks[0] else False
    try:
        if ssl:
            conn = httplib.HTTPSConnection(host, int(port), context=sslAgent._create_unverified_context())
        else:
            conn = httplib.HTTPConnection(host, int(port))
        return conn
    except:
        traceback.print_exc()
        return None

def api_status(config=None, host=None, port=None):
    if host is None or port is None:
        conn = conn_generator(config['api']['host'], config['api']['port'])
        if conn is None:
            return False
    else:
        conn = conn_generator(host, port)
        if conn is None:
            return False

    conn.request("GET", "/corr/api/v0.1/public/api/status")
    response = conn.getresponse()
    data = response.read()
    conn.close()
    try:
        data_json = json.loads(data)
        if data_json['code'] == 200:
            return True
        else:
            return False
    except:
        traceback.print_exc()
        return False

def project_create(config=None, name=None, description='', goals='',
                   tags=[], access='private', group='computational'):
    if api_status(config=config):
        conn = conn_generator(config['api']['host'], config['api']['port'])
    else:
        return [False, 'No configured api.']

    headers = {"Accept": "application/json"}
    request = {}
    request['name'] = name
    request['description'] = description
    request['goals'] = goals
    request['tags'] = tags
    request['access'] = access
    request['group'] = group
    conn.request(
        "POST", 
           "/corr/api/v0.1/private/{0}/no-app/project/create".format(config['api']['key']), 
           json.dumps(request), headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    try:
        data_json = json.loads(data)
        # print data_json
        if data_json['code'] == 201:
            return [True, data_json['content']]
        elif data_json['code'] == 200:
            return [True, data_json['content']]
        else:
            return [False, data_json['content']]
    except:
        return [False, str(traceback.print_exc())]

def project_update(config=None, project=None, description=None, goals=None,
                   tags=None, access=None, group=None):
    if api_status(config=config):
        conn = conn_generator(config['api']['host'], config['api']['port'])
    else:
        return [False, 'No configured api.']
        
    headers = {"Accept": "application/json"}
    request = {}
    if description:
        request['description'] = description
    if goals:
        request['goals'] = goals
    if tags:
        request['tags'] = tags
    if access:
        request['access'] = access
    if group:
        request['group'] = group
    conn.request(
        "POST", 
           "/corr/api/v0.1/private/{0}/no-app/project/update/{1}".format(config['api']['key'], project), 
           json.dumps(request), headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    try:
        data_json = json.loads(data)
        # print data_json
        if data_json['code'] == 201:
            return [True, data_json['content']]
        else:
            return [False, data_json['content']]
    except:
        return [False, str(traceback.print_exc())]

def project_all(config=None):
    if api_status(config=config):
        conn = conn_generator(config['api']['host'], config['api']['port'])
    else:
        return [False, 'No configured api.']

    conn.request("GET", "/corr/api/v0.1/private/{0}/no-app/projects".format(config['api']['key']))
    response = conn.getresponse()
    data = response.read()
    conn.close()
    try:
        data_json = json.loads(data)
        # print data_json
        if data_json['code'] == 200:
            return [True, data_json['content']]
        else:
            return [False, data_json['content']]
    except:
        return [False, str(traceback.print_exc())]

def record_create(config=None, project=None, request={}):
    if api_status(config=config):
        conn = conn_generator(config['api']['host'], config['api']['port'])
    else:
        return [False, 'No configured api.']

    headers = {"Accept": "application/json"}
    conn.request(
        "POST",
        "/corr/api/v0.1/private/{0}/no-app/project/record/create/{1}".format(
            config['api']['key'], project), json.dumps(request), headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    try:
        data_json = json.loads(data)
        if data_json['code'] == 201:
            return [True, data_json['content']]
        else:
            return [False, data_json['content']]
    except:
        return [False, str(traceback.print_exc())]

def record_update(config=None, record=None, request={}):
    if api_status(config=config):
        conn = conn_generator(config['api']['host'], config['api']['port'])
    else:
        return [False, 'No configured api.']

    headers = {"Accept": "application/json"}
    conn.request(
        "POST",
        "/corr/api/v0.1/private/{0}/no-app/record/update/{1}".format(
            config['api']['key'], record), json.dumps(request), headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    try:
        data_json = json.loads(data)
        if data_json['code'] == 201:
            return [True, data_json['content']]
        else:
            return [False, data_json['content']]
    except:
        return [False, str(traceback.print_exc())]

def upload_file(config=None, path=None, obj=None, group=None):
    if api_status(config=config):
        if path and group and obj:
            url = "{0}:{1}/corr/api/v0.1/private/{2}/no-app/file/upload/{3}/{4}".format(
                config['api']['host'], int(config['api']['port']),
                config['api']['key'], group, obj)
        else:
            return [False, 'Required path, obj and group.']
    else:
        return [False, 'No configured api.']

    
    # print path
    files = {'file': open('{0}'.format(path))}
    response = requests.post(url, files=files, verify=False)
    data = response.content

    try:
        data_json = json.loads(data)
        if data_json['code'] == 201:
            return [True, data_json['content']]
        else:
            return [False, data_json['content']]
    except:
        return [False, str(traceback.print_exc())]


def project_env_next(config=None, project=None, path=None):
    if api_status(config=config):
        conn = conn_generator(config['api']['host'], config['api']['port'])
    else:
        return [False, 'No configured api.']

    headers = {"Accept": "application/json"}
    request = {
        "group":"computational",
        "system":"tool-based",
        "specifics":{'tool':'corr-cmd', 'version':'0.1'},
        "version":{},
        "bundle":{}
    }
    conn.request(
        "POST",
        "/corr/api/v0.1/private/{0}/no-app/project/env/next/{1}".format(
            config['api']['key'], project), json.dumps(request), headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    try:
        data_json = json.loads(data)
        if data_json['code'] == 201:
            upload_response = upload_file(
                config=config, path=path, 
                obj=data_json['content']['bundle'], group='bundle')
            if upload_response[0]:
                return [True, data_json['content']]
            else:
                return upload_response
        else:
            return [False, data_json['content']]
    except:
        return [False, str(traceback.print_exc())]

def project_records(config=None, project_id=None):
    if api_status(config=config):
        conn = conn_generator(config['api']['host'], config['api']['port'])
    else:
        return [False, 'No configured api.']

    conn.request("GET", "/corr/api/v0.1/private/{0}/no-app/project/records/{1}".format(config['api']['key'], project_id))
    response = conn.getresponse()
    data = response.read()
    conn.close()
    try:
        data_json = json.loads(data)
        # print data_json
        if data_json['code'] == 200:
            return [True, data_json['content']]
        else:
            return [False, data_json['content']]
    except:
        return [False, str(traceback.print_exc())]

def record_download(config=None, record_id=None):
    if api_status(config=config):
        if record_id:
            url = "{0}:{1}/corr/api/v0.1/private/{2}/no-app/record/download/{3}".format(
                config['api']['host'], int(config['api']['port']),
                config['api']['key'], record_id)
        else:
            return [False, 'Required record_id.']
    else:
        return [False, 'No configured api.']
    
    try:
        response = requests.get(url, verify=False)
        file_buffer = BytesIO(response.content)
        file_buffer.seek(0)
        return file_buffer
    except:
        print(traceback.print_exc())
        return None