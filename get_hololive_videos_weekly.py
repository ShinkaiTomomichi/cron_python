# Pythonの基本ライブラリ
import numpy as np
import pandas as pd

# YoutubeAPIの利用
from apiclient.discovery import build

# 別ファイルに切り出したメソッド
import get_hololive_videos_utils

# 利用するディレクトリやファイルの絶対パス
APIKEY_PATH = ''
CHANNEL_PATH = ''
INPUT_DIR_PATH = ''
OUTPUT_DIR_PATH = ''

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
    # Youtubeに接続するためのクラスを生成
    youtube = build_youtube()

    # 更新差分を取得して保存
    get_hololive_videos_utils.get_hololive_videos_diff(youtube, CHANNEL_PATH, INPUT_DIR_PATH, OUTPUT_DIR_PATH)