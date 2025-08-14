import requests
import fake_useragent
import json
import re

dic_values = {}    # 全局变量用于保存音乐数据字典
value_src = ''     # 全局变量用于接收用户输入信息
get_cookie = ''

def get_cookie_url(get_cookie):
    """提取token值"""
    cookie_url = re.findall(r'_csrf=(.*);', get_cookie)[0].split(";")[0]
    return cookie_url

def json_format(json_str: str) -> dict:
    """格式化JSON字符串"""
    json_str = json_str.replace("false",'0')
    json_str = json_str.replace("null",'0')
    json_str = json_str.replace("true",'1')
    json_dic = json.loads(json_str)
    return json_dic

def request(params, enSecKey) -> str:
    """发送请求获取音乐元数据"""
    User_Agent_Obj = fake_useragent.UserAgent()
    user_agent = User_Agent_Obj.random

    headers = {
        'User-Agent': user_agent,
        'cookie': get_cookie
    }

    data = {
        "params": params,
        "encSecKey": enSecKey
    }

    url = "https://music.163.com/weapi/cloudsearch/get/web?csrf_token={}".format(get_cookie_url(get_cookie))
    response = requests.post(url, headers=headers, data=data)
    return response.text

def get_music_metadata(dic_value: dict) -> list:
    """提取音乐元数据"""
    results = []
    for song in dic_value['result']['songs']:
        song_data = {
            'id': song['id'],
            'title': song['name'],
            'artist': song['ar'][0]['name'] if song['ar'] else '未知',
            'album': song['al']['name'] if song['al'] else '未知',
            'duration': song['dt'],
            'official_url': f"https://music.163.com/#/song?id={song['id']}"
        }
        results.append(song_data)
    return results

def fetch_music_data(params, enSecKey):
    """获取并处理音乐数据"""
    try:
        result = request(params, enSecKey)
        json_dic = json_format(result)
        return get_music_metadata(json_dic)
    except Exception as e:
        print(f"\033[1;31m ☹️ Error: {str(e)}\033[0m")
        return None