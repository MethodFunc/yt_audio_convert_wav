# Youtube API 발급방법
1. 구글 로그인
2. https://console.cloud.google.com/apis/dashboard 접속
3. 왼쪽 목록에서 라이브러리 클릭
4. Youtube 검색
5. YouTube Data API v3 클릭
6. 사용 클릭 후 뒤로가기
7. 사용 설정된 API 및 서비스에서 YouTube Data API v3 확인
8. 왼쪽 목록에서 사용자 인증 정보 클릭
9. 상단에 사용자 인증 정보 만들기 -> API 키 클릭
10. 생성 후 API키 복사
11. .secret 폴더 안에 api_keys.py를 생성 후
12. youtube_api변수에 집어넣기

# Youtube search download 사용 방법
## 필수 설치 라이브러리 및 프로그램
### 프로그램
~~~
ffmpeg
~~~
### 라이브러리
~~~ plain
ffmpeg-python  << conda -c conda-forge 추천
pytube - 유튜브 다운로드 관련 라이브러리
google-api-python-client
pandas
~~~

~~~ bash
pip install pytube google-api-python-client pandas
conda install -c conda-forge ffmpeg-python
~~~

## 사용방법
~~~
# 도움말
python youtube_search_download.py -h

options:
  -h, --help            show this help message and exit
  -s SEARCH_TEXT, --search_text SEARCH_TEXT
                        Search text
  -m MAX_RESULTS, --max_results MAX_RESULTS
                        Max results 5 ~ 50 Default: 5
  -v VERBOSE, --verbose VERBOSE
                        Verbose & saved csv files
  -d DOWNLOAD, --download DOWNLOAD
                        Download audio files
  -c CONVERT, --convert CONVERT
                        Convert Download mp4 to wav


# 기초 사용법 (결과물 50개 추출)
python youtube_search_download.py -s "하노이 기념품" -m 50 -v True

~~~

## 출력 파일
1. youtube_info.csv - 다운로드 할 유튜브 영상의 기본 정보
2. raw_audio - 원본 음성 파일이 다운로드 되는 폴더 (mp4)
3. wav_audio - 클로바 노트를 사용하기 위해 wav로 변환된 음성 폴더
