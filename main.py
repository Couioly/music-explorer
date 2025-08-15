import os
import sys
import pyfiglet
from urllib.parse import quote
import Crawl_Tools
import Crawl_Music_Info
from colorama import Fore, init, Style
import webbrowser
import time
import pyautogui as pag


def startup():
    """启动界面"""
    status = os.system('cls || clear')  # 开启前进行清屏操作
    if status == 0:
        weight = 75
        figlet = pyfiglet.figlet_format('MusicExplorer', font='slant', justify='center')
        # logo 设计
        print("\033[1;32m +{}+\033[0m".format("-" * (weight - 2)))
        init()  # 初始化colorama
        print(Style.BRIGHT + Fore.GREEN + figlet)
        print("\033[1;32m {}@作者:Couioly/姜玖儿\033[0m".format(" " * (weight - 25)))
        print("\033[1;32m {}@微信公众号：Q哩编程\033[0m".format(" " * (weight - 25)))
        print("\033[1;32m {}@Github: https://www.github.com/Couioly/\033[0m".format(" " * (weight - 45)))
        print("\033[1;32m +{}+\033[0m".format("-" * (weight - 2)))
        # 免责声明部分
        print("\033[1;33m 🪶 免责声明：\033[0m")
        print("\033[1;35m \t1.仅供个人使用禁止商业用途。\033[0m")
        print("\033[1;35m \t2.避免一切形式的盈利活动。\033[0m")
        print("\033[1;35m \t3.本脚本仅供个人学习使用。\033[0m")
        print("\033[1;35m \t4.MusicExplorer 的发布遵循MIT协议且存在附加说明，请务必遵守。\033[0m")
        print("\033[1;35m \t5.遵守网易云音乐平台用户协议及法律，禁止侵犯他人知识产权。\033[0m")
        print("\033[1;35m \t6.因违规使用本工具导致的任何法律责任，由使用者自行承担。\033[0m")
        print("\033[1;32m +{}+\033[0m".format("-" * (weight - 2)))
        # 更新使用说明
        print("\033[1;33m 😉 使用说明：\033[0m")
        print("\033[1;36m \t1.本工具仅用于学习网络爬虫技术")
        print("\033[1;36m \t2.不提供音乐下载功能，仅展示官方链接")
        print("\033[1;36m \t3.请支持正版音乐平台")
        print("\033[1;36m \t3.现在让我们开启享受音乐时光吧！ 💕\033[0m")
        print()
        print(format("\033[1;32m 音乐空间开启\033[0m", '^90'))
        print("\033[1;32m {}\033[0m".format("*" * weight))
        return True
    else:
        # 清屏失败 退出程序
        print("\033[1;31m ☹️ 开启失败，请重新尝试！\033[0m")
        return False


def pyauto():
    """辅助打开开发者工具"""
    print("\033[1;33m 😳 注意：接下来将自动打开网页...")
    time.sleep(1)
    webbrowser.open(f'https://music.163.com/#/search/m/?s={quote(Crawl_Music_Info.value_src)}&type=1')
    time.sleep(5)
    pag.hotkey('F12')
    time.sleep(1)
    modifier = 'command' if sys.platform.startswith('darwin') else 'Ctrl'
    pag.hotkey(modifier, 'r')


def crawl():
    """爬取音乐元数据"""
    Crawl_Music_Info.value_src = input("\033[1;32m 🪶 请输入音乐关键字[歌手/歌名]: \033[0m")
    while not Crawl_Music_Info.value_src:
        print("\033[1;31m 😨 输入内容为空，请重新输入！\033[0m")
        Crawl_Music_Info.value_src = input("\033[1;32m 请输入音乐关键字[歌手/歌名]: \033[0m")

    print("\033[1;33m 🪜 请打开网易云音乐官网搜索页面...")
    boo = input("\033[1;32m 🪶 是否需要辅助打开开发者工具? [y/n]: \033[0m").lower()
    if boo == 'y':
        pyauto()

    print("\033[1;32m 🧐 请在开发者工具中查找以下内容:")
    print("\t 1. 在Network标签页筛选 'web?csrf_token='")
    print("\t 2. 复制Payload中的params和encSecKey")

    params = input("\033[1;32m 🪶 params: \033[0m")
    encseckey = input("\033[1;32m 🪶 encSecKey: \033[0m")
    Crawl_Music_Info.get_cookie = input("\033[1;32m 🪶 Cookie: \033[0m")

    print("\033[1;33m 🥴 正在获取音乐信息...\033[0m")
    return Crawl_Music_Info.fetch_music_data(params, encseckey)


def display_results(songs):
    """显示搜索结果"""
    if not songs:
        print("\033[1;31m ☹️ 未找到相关歌曲信息\033[0m")
        return

    print(f"\033[1;32m 🔍 找到 {len(songs)} 首相关歌曲:\033[0m")
    for i, song in enumerate(songs, 1):
        print(f"\033[1;35m {i}. {song['title']} - {song['artist']}\033[0m")

    choice = input("\033[1;32m 🪶 输入序号查看详情(0查看全部，q退出): \033[0m")
    if choice == 'q':
        return

    if choice == '0':
        for song in songs:
            Crawl_Tools.display_song_info(song)
    elif choice.isdigit() and 1 <= int(choice) <= len(songs):
        Crawl_Tools.display_song_info(songs[int(choice) - 1])


def main():
    if startup():
        while True:
            songs = crawl()
            if songs:
                display_results(songs)

            cont = input("\033[1;32m 🪶 继续搜索? [y/n]: \033[0m").lower()
            if cont != 'y':
                break

        print("\033[1;35m \n感谢使用，请支持正版音乐！ 😊\033[0m")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\033[1;35m \n感谢使用，请支持正版音乐！ 😊\033[0m")
        exit(0)