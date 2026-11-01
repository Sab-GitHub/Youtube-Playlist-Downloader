from yt_dlp import YoutubeDL
import json

def get_req_info(info, isPlaylist=False):
    req_info = {
        'id': info.get('id'),
        'title': info.get('title'),
        'url': info.get('url') or info.get('webpage_url')
    }

    if isPlaylist:
        req_info['entries'] = info.get('entries')

    return req_info

def get_playlist_info(url):
    ydl_opts = {
    'extract_flat': True,
    'skip_download': True,
    'noplaylist': False
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, False)

    # Might delete keep only section later.-----------------------------------------------------------------------

    # Keep only required info of playlist.
    req_info = get_req_info(info, True)

    # Keep only required info of entries of playlist.
    for i, entry in enumerate(req_info['entries']):
        req_info['entries'][i] = get_req_info(entry)

    return req_info

def download_playlist_audio(req_info, save_file_path):
    ydl_opts = {
        'format': 'm4a/bestaudio/best', # Select most suitable format in order: m4a, separate audio, video file.
        'postprocessors': [{
            'key': 'FFmpegExtractAudio', # If video file format, extract audio.
            'preferredcodec': 'm4a' # If not m4a already, convert to m4a.
        }],
        'outtmpl': None,

        # Preventing rate-limit soft ban.
        'sleep_interval': 5,
        'max_sleep_interval': 15
    }

    for entry_info in req_info['entries']:
        ydl_opts['outtmpl'] = save_file_path + '/%(title)s.%(ext)s'
        with YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download(entry_info['url'])

URL = 'https://www.youtube.com/playlist?list=PLcahqx3SI_Qw'

req_info = get_playlist_info(URL)
save_file_path = f'audio/{req_info['title']}'
download_playlist_audio(req_info, save_file_path)

#req_info = json.dumps(ydl.sanitize_info(req_info), indent=4)
# with open('info1.json', 'w') as f:
#     f.write(req_info_json)

