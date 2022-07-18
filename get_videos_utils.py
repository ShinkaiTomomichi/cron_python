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


def save_videos(youtube, video_ids, channel_name, channel_id, output_dir_path, already_videos = None):
    # 動画のIDから詳細情報を取得する
    video_details = []
    for video_id in video_ids:
        try:
            video_detail = youtube.videos().list(
                part = 'snippet,statistics,contentDetails', 
                id = video_id, 
            ).execute()
        except HttpError as e:
            print('save_videosにてエラーが発生しました')
            print(video_id)
            print(e)
            print(e.response.status_code) 
            return
        
        # 公開されていない動画など、取得できない場合がある
        if len(video_detail['items']) == 0:
            return
        video_snippet = video_detail['items'][0]['snippet']
        video_statistics = video_detail['items'][0]['statistics']
        video_content_details = video_detail['items'][0]['contentDetails']
        # snippetから取得
        date = video_snippet['publishedAt']
        title = video_snippet['title']
        thumbnail = video_snippet['thumbnails']['high']['url']
        description = video_snippet['description']
        category_id = video_snippet['categoryId']
        # contentDetailsから取得        
        duration = pt2sec(video_content_details['duration'])
        duration_origin = video_content_details['duration']
        # statisticsから取得
        # 評価数、コメントが非公開の場合は0で埋める
        view_count = 0
        like_count = 0
        dislike_count = 0
        comment_count = 0
        if 'viewCount' in video_statistics.keys():
            view_count = video_statistics['viewCount']
        if 'likeCount' in video_statistics.keys():
            like_count = video_statistics['likeCount']
        if 'dislikeCount' in video_statistics.keys():
            dislike_count = video_statistics['dislikeCount']
        if 'commentCount' in video_statistics.keys():
            comment_count = video_statistics['commentCount']
                # リストのリストとして情報を格納する
        video_details.append([video_id, channel_name, channel_id, date, title, 
                              thumbnail, category_id, duration, duration_origin, description, 
                              view_count, like_count, dislike_count, comment_count])

    # 動画情報を書き込む
    # video_idが取得できていない場合スキップする
    if len(video_ids) != 0:
        video_details_numpy = np.array(video_details)
        video_details_pandas = pd.DataFrame(data=video_details_numpy, 
                                            columns=['Id', 'Name', 'ChannelId', 'Date', 'Title', 
                                                     'Thumbnail', 'CategoryId', 'Duration', 'DurationOriginal', 'Description', 
                                                     'ViewCount', 'LikeCount', 'DislikeCount', 'CommentCount'])
        # 差分を追加する場合
        if already_videos == None:
            videos = pd.concat([already_videos, video_details_pandas])
        else:
            videos = video_details_pandas
        videos.to_csv(os.path.join(output_dir_path, channel_name+'_videos.csv'))
    

def get_videos_diff(youtube, channel_path, input_dir_path, output_dir_path):
    channels = pd.read_csv(channel_path, header=0)
    channel_ids = np.array(channels['ChannelId'])
    channel_names = np.array(channels['Name'])

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
        except HttpError as e:
            print('get_videos_diffにてエラーが発生しました')
            print(e)
            return
        for new_video_item in new_videos['items']:
            new_video_ids.append(new_video_item['id']['videoId'])

        # 動画情報が0の場合はこの時点でスキップする
        if len(new_video_ids) == 0:
            print("データが存在しません")

        # 既に保存された動画のIDを取得する
        # ファイルが存在しない場合はスキップする
        if os.path.exists(os.path.join(input_dir_path, channel_name+'_videos.csv')):
            already_videos = pd.read_csv(os.path.join(input_dir_path, channel_name+'_videos.csv'))
            already_video_ids = np.array(already_videos['Id'])
        else:
            continue

        # まだ保存されていない差分を取り出す
        diff_video_ids = []
        for video_id in new_video_ids:
            if video_id not in already_video_ids:
                diff_video_ids.append(video_id)

        print(str(len(diff_video_ids))+'件の動画が追加されました')

        save_videos(youtube, diff_video_ids, channel_name, channel_id, output_dir_path, already_videos)
        
    print('差分の追加が完了しました')


def get_videos_new(youtube, channel_path, output_dir_path):
    channels = pd.read_csv(channel_path, header=0)
    channel_ids = np.array(channels['ChannelId'])
    channel_names = np.array(channels['Name'])

    # 動画情報を取得する
    for i, channel_id in enumerate(channel_ids):
        channel_name = channel_names[i]
        print(channel_name, ":", i+1, "/", channel_ids.size)
        
        # 既にファイルが存在する場合はskip
        if os.path.exists(os.path.join(output_dir_path, channel_name+'_videos.csv')):
            continue

        # 各チャンネルから全ての動画IDを取得する
        video_ids = []
        next_page_token = 'search_start'
        while True:
            if next_page_token == 'search_start':         
                try:
                    videos = youtube.search().list(
                        part = 'id', 
                        channelId = channel_id, 
                        order = 'viewCount',
                        type = "video",
                        maxResults = 50, 
                    ).execute()
                # HTTPエラー（主にQuota上限）だった場合
                except HttpError as e:
                    print('get_videos_newにてエラーが発生しました')
                    print(e)
                    return
            else:
                try:
                    videos = youtube.search().list(
                        part = 'id', 
                        channelId = channel_id, 
                        order = 'viewCount',
                        type = 'video',
                        pageToken = next_page_token,
                        maxResults = 50, 
                    ).execute()
                except HttpError as e:
                    print('get_videos_newにてエラーが発生しました')
                    print(e)
                    return
            
            # 動画のIDを取得する
            for video_item in videos['items']:
                video_ids.append(video_item['id']['videoId'])
            
            # 次のページが存在しない場合終了する
            if 'nextPageToken' in videos.keys():
                next_page_token = videos['nextPageToken']
            else:
                break
        
        if len(video_ids) != 0:
            save_videos(youtube, video_ids, channel_name, channel_id, output_dir_path)
    
    print("新規作成が完了しました")
