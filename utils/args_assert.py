import argparse


def max_result_value_check(x):
    x = int(x)

    if x > 50:
        raise argparse.ArgumentTypeError('Maximum result value must be less than 50')
    if x < 5:
        raise argparse.ArgumentTypeError('Minimum result value must be greater than 5')

    return x


def bool_string(x):
    if x not in {'False', 'True'}:
        raise argparse.ArgumentError('Not a valid boolean string')
    return x == 'True'


def assert_order(x):
    if x not in ["date", "rating", "relevance", "title", "videoCount", "viewCount"]:
        raise argparse.ArgumentError("Order settings are not correct.\n"
                                     "Support: date/rating/relevance/title/vidoeCount/viewCount")

    return x


def assert_type(x):
    if x not in ["channel", "playlist", "video"]:
        raise argparse.ArgumentParser("Type setting just support channel/playlist/video")

    return x
