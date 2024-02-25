from pytube import YouTube
import os
import sys
import eyed3
import re

def normalize_filename(name):
    # Replace non-alphanumeric characters with underscores
    return re.sub(r'[^a-zA-Z0-9]', '_', name)

#take youtube url as argument from command line and download the video

def ytgrab(url):
    yt = YouTube(url)
    yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()
    print(f'Downloaded {yt.title}')
    return yt.title

def ytgrabmp3(url):
    yt = YouTube(url)
    normalized_title = normalize_filename(yt.title)

    # Download the audio
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_stream.download(filename=f"{normalized_title}.mp4")
    print(f'Downloaded {yt.title}')

    # Convert to mp3
    print(f'Converting {yt.title} to mp3')
    os.system(f'ffmpeg -i "{normalized_title}.mp4" -vn -ar 44100 -ac 2 -ab 192k -f mp3 "{normalized_title}.mp3"')
    
    # Remove the original mp4 file
    os.remove(f'{normalized_title}.mp4')

    # Edit mp3 file metadata
    audiofile = eyed3.load(f'{normalized_title}.mp3')
    audiofile.tag.title = yt.title
    audiofile.tag.artist = yt.author
    audiofile.tag.save()

    return yt.title

if __name__ == '__main__':
    print(f'yo fire it up! dl: {sys.argv[1]}')
    #cli to grab as mp3
    if len(sys.argv) > 2 and sys.argv[2] == 'mp3':
        ytgrabmp3(sys.argv[1])
    else:
        ytgrab(sys.argv[1])