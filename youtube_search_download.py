import argparse

from utils import search_video_info, download_video, convert_mp4_to_wav, convert_error_types
# Assert
from utils import assert_order, bool_string, max_result_value_check, assert_type

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Youtube audio downloader")
    parser.add_argument("-s", "--search_text", type=str, help="Search text")
    parser.add_argument("-m", "--max_results", type=max_result_value_check, default=5,
                        help="Max results 5 ~ 50 Default: 5")
    parser.add_argument("-o", "--order", type=assert_order, default="relevance",
                        help="Order support: date/rating/relevance/title/vidoeCount/viewCount"
                             "Default: relevance")
    parser.add_argument("-t", "--type", type=assert_type, default="video",
                        help="type support: channel/playlist/video\n"
                             "Default: video")
    parser.add_argument("-v", "--verbose", type=bool_string, default=True, help="Verbose & saved csv files")

    parser.add_argument("-d", "--download", type=bool_string, default=True, help="Download audio files")
    parser.add_argument("-c", "--convert", type=bool_string, default=True, help="Convert Download mp4 to wav")

    INPUT_DIR = "./raw_audio"
    OUTPUT_DIR = "./wav_audio"

    args = parser.parse_args()

    if args.download:
        items = search_video_info(args.search_text, args.max_results, args.order, args.type, args.verbose)
        download_video(items, INPUT_DIR, args.verbose, args.verbose)

    if args.convert:
        convert_error_types(INPUT_DIR)
        convert_mp4_to_wav(INPUT_DIR, OUTPUT_DIR)
