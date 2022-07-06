# Pythonの基本ライブラリ
from ast import Return
import numpy as np
import pandas as pd

# YoutubeAPIの利用
from apiclient.discovery import build

# 引数を取得
import sys

# 別ファイルに切り出したメソッド
import get_hololive_videos_utils

# 利用するディレクトリやファイルの絶対パス
APIKEY_PATH = ''

# これとは別に自動取得プログラムも自動化しておきたい
def build_youtube():
    # APIキーをファイルから取得
    f = open(APIKEY_PATH, 'r')
    api_key = f.read()
    f.close()

    # APIキーを用いてリクエスト用のクラスを作成
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=api_key)
    return youtube

if __name__ == "__main__":
    args = sys.argv
    if len(args) < 3:
        print("引数を2つ以上指定してください")
        exit()

    file_type = args[1]
    update_type = args[2]

    # Youtubeに接続するためのクラスを生成
    youtube = build_youtube()

    channel_path = ''
    input_dir_path = ''
    output_dir_path = ''

    if update_type == 'd':
        # 更新差分を取得して保存
        get_hololive_videos_utils.get_videos_diff(youtube, channel_path, input_dir_path, output_dir_path)
    elif update_type == 'n':
        # 新規作成
        get_hololive_videos_utils.get_videos_new(youtube, channel_path, output_dir_path)