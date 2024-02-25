from pytube import YouTube
import os
import sys

#take youtube url as argument from command line and download the video

def ytgrab(url):
    yt = YouTube(url)
    yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()
    print(f'Downloaded {yt.title}')
    return yt.title

if __name__ == '__main__':
    ytgrab(sys.argv[1])