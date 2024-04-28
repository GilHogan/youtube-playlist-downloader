#!python3
# Usage -
# 1. open cmd
# 2. cd to the folder where these files are present
# 3. type - python ytdown.py
# the script will start working


import os
import re
import subprocess
import time

import requests
from pytube import Playlist, YouTube


# imp functions


def foldertitle(url):
    try:
        res = requests.get(url)
    except:
        print('no internet')
        return False

    plain_text = res.text

    if 'list=' in url:
        eq = url.rfind('=') + 1
        cPL = url[eq:]

    else:
        print('Incorrect attempt.')
        return False

    return cPL


def link_snatcher(url):
    our_links = []
    try:
        res = requests.get(url)
    except:
        print('no internet')
        return False

    plain_text = res.text

    if 'list=' in url:
        eq = url.rfind('=') + 1
        cPL = url[eq:]
    else:
        print('Incorrect Playlist.')
        return False

    tmp_mat = re.compile(r'watch\?v=\S+?list=' + cPL)
    mat = re.findall(tmp_mat, plain_text)

    for m in mat:
        new_m = m.replace('&amp;', '&')
        work_m = 'https://youtube.com/' + new_m
        # print(work_m)
        if work_m not in our_links:
            our_links.append(work_m)

    return our_links


BASE_DIR = os.getcwd()

print('WELCOME TO PLAYLIST DOWNLOADER DEVELOPED BY - www.github.com/mohit0101')

url = str(input("\nspecify you playlist url\n"))

print('\nCHOOSE ANY ONE - TYPE 360P OR 720P OR 1080P\n')
user_res = str(input()).lower()
if len(user_res) == 0:
    user_res = '1080p'
else:
    user_res = user_res.lower()
print('...You choosed ' + user_res + ' resolution\n.')

# our_links = link_snatcher(url)

os.chdir(BASE_DIR)

new_folder_name = foldertitle(url)
print(new_folder_name[:7])

try:
    os.mkdir(new_folder_name[:7])
except:
    print('folder already exists')

os.chdir(new_folder_name[:7])
SAVEPATH = os.getcwd()
print(f'\n files will be saved to {SAVEPATH}')

x = []
for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        pathh = os.path.join(root, name)

        if os.path.getsize(pathh) < 1:
            os.remove(pathh)
        else:
            x.append(str(name))

print('\nconnecting . . .\n')

print()


def transform_episode_title(input_title):
    """
    标题转换
    """
    ep_index = input_title.rfind("| EP")
    first_str = input_title
    second_str = ''
    if ep_index != -1:
        first_str = input_title[0:ep_index].strip()
        second_str = input_title[ep_index:].split("|", 1)[1].strip()

    match = re.search(r"(EP\s*\d+)", second_str)
    ep_str = ''
    third_str = ''
    if match:
        ep_str = match.group(1)
        third_str = second_str.split(ep_str)[1]
    ep_str = ep_str.replace(' ', '')
    if ep_str:
        ep_str += ' '
    return {"title": ep_str + first_str + third_str, "ep": ep_str}


def get_title_and_video(_video_url):
    """
    获取标题和youtube对象的列表
    """
    print('start get_title_and_video')
    _result = {}
    retry_times = 50
    for i in range(retry_times):
        try:
            _yt = YouTube(_video_url)
            _main_title = _yt.title
            # 修改标题前缀
            ep_title_dict = transform_episode_title(_main_title)
            _main_title = ep_title_dict.get("title")
            ep = ep_title_dict.get("ep")
            _main_title = _main_title + '.mp4'
            # 去掉windows非法字符
            _main_title = re.sub('[\/:*?"<>|]', '', _main_title)
            _result = {"title": _main_title, "video": _yt, "ep": ep}
            break
        except Exception as e:
            print("warning: connection problem..unable to fetch video info.")
            time.sleep(5)
            if i == retry_times - 1:
                print("error: cannot connected to video = ", _video_url)
    print('end get_title_and_video')
    return _result


# 获取标题和youtube对象的列表
for _video in Playlist(url):

    title_and_video = get_title_and_video(_video)
    video = title_and_video.get("video")
    main_title = title_and_video.get("title")
    retry_times = 20
    if main_title and main_title not in x:
        for i in range(retry_times):
            try:
                if user_res == '360p' or user_res == '720p' or user_res == '1080p':
                    if user_res == '360p' or user_res == '720p':
                        vid = video.streams.filter(progressive=True, file_extension='mp4', res=user_res).first()
                        print('Downloading. . . ' + vid.default_filename + ' and its file size -> ' + str(
                            round(vid.filesize / (1024 * 1024), 2)) + ' MB.')
                        vid.download(SAVEPATH)
                    else:
                        yt_streams = video.streams
                        vid = yt_streams.filter(adaptive=True, file_extension='mp4', res=user_res).first()
                        if vid.audio_codec is None:
                            audio = yt_streams.filter(only_audio=True, file_extension='mp4').last()
                            audio_file_name = main_title + "_audio"
                            print('Downloading audio. . . ' + audio_file_name + ' and its file size -> ' + str(
                                round(audio.filesize / (1024 * 1024), 2)) + ' MB.')
                            audio.download(output_path=SAVEPATH, filename=audio_file_name, max_retries=5)

                            video_file_name = main_title + "_video"
                            print('Downloading video. . . ' + video_file_name + ' and its file size -> ' + str(
                                round(vid.filesize / (1024 * 1024), 2)) + ' MB.')
                            vid.download(output_path=SAVEPATH, filename=video_file_name, max_retries=5)

                            # 加载视频和音频文件
                            video_path = os.path.join(SAVEPATH, video_file_name)
                            audio_path = os.path.join(SAVEPATH, audio_file_name)
                            out_file_path = os.path.join(SAVEPATH, main_title)

                            command = 'D:/soft/ffmpeg-full_build/bin/ffmpeg.exe -i "' + video_path + '" -i "' \
                                      + audio_path + '" -f mp4 "' + out_file_path + '"'
                            subprocess.call(command, shell=True)

                            # 删除多余的文件
                            os.remove(video_path)
                            os.remove(audio_path)
                        else:
                            print('Downloading. . . ' + vid.default_filename + ' and its file size -> ' + str(
                                round(vid.filesize / (1024 * 1024), 2)) + ' MB.')
                            vid.download(SAVEPATH)

                    print('Video Downloaded')
                else:
                    print('something is wrong.. please rerun the script')
                break
            except Exception as e:
                print("warning download error retry", e)
                time.sleep(5)
                if i == retry_times - 1:
                    print("error: download failed main_title = ", main_title)
    else:
        print(f'\n skipping "{main_title}" video \n')

print('downloading finished')
print(f'\n all your videos are saved at --> {SAVEPATH}')
