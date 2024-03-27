import os
import sys
import re
import pandas as pd
from pathlib import Path
import time

from googleapiclient.discovery import build
import pytube
from pytube import YouTube
from pytube.cli import on_progress

current_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
hidden_folder = os.path.join(current_dir, '.secret')
sys.path.insert(0, hidden_folder)
from api_keys import youtube_api

##### SECRET KEY #####
DEVELOPER_KEY = youtube_api
######################

API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

REGEX = r"[^A-Za-z0-9가-힣 \-\_\[\]]+"


def get_params(q, max_result, order, types):
    """
    search list params
    part: snippet - 기본
    q : 검색 명
    order:
        date - 최신 날짜 순
        rating - 높은 평가 순
        relevance - 관련성 (기본 값)
        title - 타이틀 알파벳 순
        videoCount - 채널 동영상 수 순
        viewCount - 조회수 높은 수, 실시간 방송 시 시청자 수 기준
    maxResults: 0 ~ 50 default 5
    type:
        channel - 채널
        playlist - 플레이 리스트
        video - 영상 만

    """

    params = {
        'q': q,
        'order': order,
        'part': 'snippet',
        'maxResults': max_result,
        "type": types
    }

    return params


def clean_result(search_result):
    youtube_info = {
        "channelName": list(),
        "videoTitle": list(),
        "videoDescription": list(),
        "videoPublishAt": list(),
        "videoId": list(),

    }

    youtube_url = "https://www.youtube.com/watch?v="

    for item in search_result:
        snipper = item['snippet']
        vid = item["id"]

        youtube_info["videoId"].append(f'{youtube_url}/{vid["videoId"]}')
        youtube_info["videoTitle"].append(snipper["title"])
        youtube_info["videoDescription"].append(snipper["description"])
        youtube_info["videoPublishAt"].append(snipper["publishedAt"])
        youtube_info["channelName"].append(snipper["channelTitle"])

    return youtube_info


def search_video_info(text, max_result, order, types, save_info=True):
    search_params = get_params(text, max_result, order, types)

    youtube = build(API_SERVICE_NAME, API_VERSION, developerKey=DEVELOPER_KEY)

    video_response = youtube.search().list(
        **search_params
    ).execute()

    result_items = video_response["items"]

    youtube_info = clean_result(result_items)

    if save_info:
        print("Saved search youtube info")
        if not Path('./csv').exists():
            Path('./csv').mkdir(parents=True)

        if Path("./csv/youtube_info.csv").exists():
            dataframe = pd.read_csv("./csv/youtube_info.csv")
            temp = pd.DataFrame(youtube_info)
            dataframe = pd.concat([dataframe, temp], axis=0)
            dataframe.drop_duplicates(subset="videoId", inplace=True)
        else:
            dataframe = pd.DataFrame(youtube_info)

        dataframe.to_csv("./csv/youtube_info.csv", index=False)

    return youtube_info


def download_video(youtube_info, output_dir, update_info=True, verbose=False):
    if not Path(output_dir).exists():
        Path(output_dir).mkdir(parents=True)

    if "age_restricted" not in youtube_info:
        youtube_info["age_restricted"] = []

    normal_rating = 0
    age_restricted = 0

    if update_info:
        if Path("./csv/youtube_info.csv").exists():
            dataframe = pd.read_csv("./csv/youtube_info.csv")
    else:
        print("File is not exists")

    for video_id in youtube_info["videoId"]:
        data = YouTube(video_id, on_progress_callback=on_progress)
        title = re.sub(REGEX, "", data.title).replace(" ", "_")
        title = title.replace("__", "_")
        publish_at = data.publish_date

        if verbose:
            print(f"Title: {title}, publish_at: {publish_at}")

        try:
            audio = data.streams.filter(mime_type="audio/mp4")
            youtube_info["age_restricted"].append(0)
            normal_rating += 1

        except pytube.exceptions.AgeRestrictedError:
            youtube_info["age_restricted"].append(1)
            age_restricted += 1

            if 'dataframe' in locals():
                dataframe = dataframe.drop(dataframe[dataframe["videoId"] == video_id].index)

            continue

        if Path(f"{output_dir}/{title}.mp4").exists():
            print(f"File is existing. Skipping download {title}")
            continue

        audio[-1].download(output_path=output_dir, filename=f"{title}.mp4")
        time.sleep(1)

    if verbose:
        print(f"Total videos: {len(youtube_info['videoId'])}")
        print(f"Successful download videos : {normal_rating}")
        print(f"Age restricted videos: {age_restricted}")


