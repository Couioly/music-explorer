import requests
import fake_useragent
import execjs
import os
import sys
import Crawl_Music_Info

def get_resource_path(relative_path):
    """获取资源的绝对路径"""
    if getattr(sys, 'frozen', False):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def generate_official_link(song_id):
    """生成官方播放链接"""
    return f"https://music.163.com/#/song?id={song_id}"

def format_duration(milliseconds):
    """格式化时长"""
    seconds = milliseconds // 1000
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes}:{seconds:02d}"

def display_song_info(song):
    """显示歌曲信息"""
    print(f"\033[1;36m 🎵 标题: {song['title']}")
    print(f" 👤 歌手: {song['artist']}")
    print(f" 💿 专辑: {song['album']}")
    print(f" ⏱️ 时长: {format_duration(song['duration'])}")
    print(f" 🔗 官方链接: {song['official_url']}")
    print("\033[1;32m" + "-"*50 + "\033[0m")