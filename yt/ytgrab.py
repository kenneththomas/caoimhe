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
    #avoid age restriction
    yt = YouTube(url, use_oauth=False, allow_oauth_cache=False)
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

#function to convert all mov files in a directory to mp3
def movtomp3():
    for file in os.listdir('.'):
        if file.endswith('.mov'):
            print(f'Converting {file} to mp3')
            os.system(f'ffmpeg -i "{file}" -vn -ar 44100 -ac 2 -ab 192k -f mp3 "{file[:-4]}.mp3')
            os.remove(file)

# new function to convert existing mp4 to mp3
def mp4tomp3(mp4file):
    # Convert to mp3
    print(f'Converting {mp4file} to mp3')
    os.system(f'ffmpeg -i "{mp4file}" -vn -ar 44100 -ac 2 -ab 192k -f mp3 "{mp4file[:-4]}.mp3')
    
    # Remove the original mp4 file
    print('not removing mp4')
    #os.remove(mp4file)

    # Edit mp3 file metadata
    audiofile = eyed3.load(f'{mp4file[:-4]}.mp3')
    audiofile.tag.title = mp4file[:-4]
    # set artist to caoimhe
    audiofile.tag.artist = 'caoimhe'
    audiofile.tag.save()

    return mp4file[:-4]

#rename artist on all mp3 files in a directory to caoimhe
def renameartist():
    for file in os.listdir('.'):
        if file.endswith('.mp3'):
            audiofile = eyed3.load(file)
            audiofile.tag.artist = 'caoimhe'
            audiofile.tag.save()

if __name__ == '__main__':
    print(f'yo fire it up! dl: {sys.argv[1]}')
    #cli to grab as mp3
    if len(sys.argv) > 2 and sys.argv[2] == 'mp3':
        ytgrabmp3(sys.argv[1])
    #cli to convert existing mp4 to mp3
    elif len(sys.argv) > 2 and sys.argv[2] == 'convert':
        mp4tomp3(sys.argv[1])
    #use movtomp3 to convert all mov files in a directory to mp3
    elif len(sys.argv) > 2 and sys.argv[2] == 'mov':
        movtomp3()
    #rename artist on all mp3 files in a directory to caoimhe
    elif len(sys.argv) > 2 and sys.argv[2] == 'rename':
        renameartist()
    else:
        ytgrab(sys.argv[1])