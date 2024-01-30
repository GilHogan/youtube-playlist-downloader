#!python3
# Usage -
# 1. open cmd
# 2. cd to the folder where these files are present
# 3. type - python ytdown.py
# the script will start working


import os
import subprocess
from pytube import YouTube
import random
import requests
import re
import string


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

print('...You choosed ' + user_res + ' resolution\n.')

our_links = link_snatcher(url)

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

for link in our_links:
    try:
        yt = YouTube(link)
        main_title = yt.title
        main_title = main_title + '.mp4'
        main_title = main_title.replace('|', '')

    except:
        print('connection problem..unable to fetch video info')
        break

    if main_title not in x:

        if user_res == '360p' or user_res == '720p' or user_res == '1080p':
            if user_res == '360p' or user_res == '720p':
                vid = yt.streams.filter(progressive=True, file_extension='mp4', res=user_res).first()
                print('Downloading. . . ' + vid.default_filename + ' and its file size -> ' + str(
                    round(vid.filesize / (1024 * 1024), 2)) + ' MB.')
                vid.download(SAVEPATH)
            else:
                yt_streams = yt.streams
                vid = yt_streams.filter(adaptive=True, file_extension='mp4', res=user_res).first()
                if vid.audio_codec is None:
                    audio = yt_streams.filter(only_audio=True, file_extension='mp4').last()
                    audio_file_name = main_title + "_audio"
                    print('Downloading audio. . . ' + audio_file_name + ' and its file size -> ' + str(
                        round(audio.filesize / (1024 * 1024), 2)) + ' MB.')
                    audio.download(output_path=SAVEPATH, filename=audio_file_name)

                    video_file_name = main_title + "_video"
                    print('Downloading video. . . ' + video_file_name + ' and its file size -> ' + str(
                        round(vid.filesize / (1024 * 1024), 2)) + ' MB.')
                    vid.download(output_path=SAVEPATH, filename=video_file_name)

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

    else:
        print(f'\n skipping "{main_title}" video \n')

print(' downloading finished')
print(f'\n all your videos are saved at --> {SAVEPATH}')
