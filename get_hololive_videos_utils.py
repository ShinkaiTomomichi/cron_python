# Pythonの基本ライブラリ
import numpy as np
import pandas as pd

# YoutubeAPIの利用
from apiclient.errors import HttpError

# ファイル操作
import os

# ISO表記の動画時間を秒に変換
def pt2sec(pt_time):
    s_list, m_list, h_list = [], [], []
    conc_s, conc_m, conc_h = '', '', ''
    flag = ''
    
    for i in reversed(pt_time):
        if i == 'S':
            flag = 'S'
        elif i == 'M':
            flag = 'M'
        elif i == 'H':
            flag = 'H'
        elif i == 'T':
            break
        else:
            if flag == 'S':
                s_list.append(i)
            elif flag == 'M':
                m_list.append(i)
            elif flag == 'H':
                h_list.append(i)
    
    for s in reversed(s_list):
        conc_s += s
    for m in reversed(m_list):
        conc_m += m
    for h in reversed(h_list):
        conc_h += h
    conc_s = 0 if conc_s == '' else int(conc_s)
    conc_m = 0 if conc_m == '' else int(conc_m)
    conc_h = 0 if conc_h == '' else int(conc_h)

    times = conc_h*3600 + conc_m*60 + conc_s
    return times

def get_hololive_videos_diff(youtube, channel_path, input_dir_path, output_dir_path):
    channels = pd.read_csv(channel_path, header=0)
    channel_ids = np.array(channels['id'])
    channel_names = np.array(channels['チャンネル'])

    # 動画情報を取得する
    for i, channel_id in enumerate(channel_ids):
        channel_name = channel_names[i]
        print(channel_name, ":", i+1, "/", channel_ids.size)
        
        # 各チャンネルから最新の50件の動画のIDを取得する
        new_video_ids = []
        try:
            new_videos = youtube.search().list(
                part = 'id', 
                channelId = channel_id, 
                order = 'date',
                type = "video",
                maxResults = 50, 
            ).execute()
        # HTTPエラー（主にQuota上限）だった場合
        except HttpError:
            print('データ取得中にエラーが発生しました')
            break
        for new_video_item in new_videos['items']:
            new_video_ids.append(new_video_item['id']['videoId'])

        # 既に保存された動画のIDを取得する
        already_videos = pd.read_csv(os.path.join(input_dir_path, channel_name+'_videos.csv'))
        already_video_ids = np.array(already_videos['Id'])

        # まだ保存されていない差分を取り出す
        diff_video_ids = []
        for video_id in new_video_ids:
            if video_id not in already_video_ids:
                diff_video_ids.append(video_id)

        print(str(len(diff_video_ids))+'件の動画が追加されました')

        # 動画のIDから詳細情報を取得する
        for video_id in diff_video_ids:
            try:
                video_detail = youtube.videos().list(
                    part = 'snippet,statistics,contentDetails', 
                    id = video_id, 
                ).execute()
            except HttpError:
                print('データ参照中にエラーが発生しました')
                break
                
            video_snippet = video_detail['items'][0]['snippet']
            video_statistics = video_detail['items'][0]['statistics']
            video_contentDetails = video_detail['items'][0]['contentDetails']
            # snippetから取得
            date = video_snippet['publishedAt']
            title = video_snippet['title']
            thumbnail = video_snippet['thumbnails']['high']['url']
            description = video_snippet['description']
            category_id = video_snippet['categoryId']
            # contentDetailsから取得        
            duration = pt2sec(video_contentDetails['duration'])
            duration_origin = video_contentDetails['duration']
            # statisticsから取得
            views = video_statistics['viewCount']
            # 評価数、コメントが非公開の場合は0で埋める
            like = 0
            dislike = 0
            comments = 0
            if 'likeCount' in video_statistics.keys():
                like = video_statistics['likeCount']
            if 'dislikeCount' in video_statistics.keys():
                dislike = video_statistics['dislikeCount']
            if 'commentCount' in video_statistics.keys():
                comments = video_statistics['commentCount']
            
            # 既存のファイルに差分を追加して保存する
            video_details_numpy = np.array([[video_id, channel_name, date, title, thumbnail, category_id, duration, duration_origin, description, views, like, dislike, comments]])            
            video_details_pandas = pd.DataFrame(data=video_details_numpy, 
                                                columns=['Id', 'Channel', 'Date', 'Title', 'Thumbnail', 'CategoryId', 'Duration', 'DurationOriginal', 'Description', 'Viewcount', 'LikeCount', 'DislikeCount', 'CommentCount'])
            already_videos = pd.concat([already_videos, video_details_pandas])
    
        already_videos.to_csv(os.path.join(output_dir_path, channel_name+'_videos.csv'))
        
    print('差分の取得が完了しました')