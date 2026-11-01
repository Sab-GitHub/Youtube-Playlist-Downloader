from yt_dlp import YoutubeDL

DOWNLOAD_STATES = {
    'video and audio': '1',
    'video only': '2',
    'audio only': '3'
}

def slice_playlist():
    print('\nEnter older entry as start and newer entry as end.')
    print('Entries are new or old based on when you added them to the playlist.\n')
    start = input('Enter the url of the entry you want to start the download with: ')
    end = input('Enter the url of the entry you want to end the download with: ')
    return (start, end)

def get_slice_url_list(playlist_slice, urls):
    start_i, end_i = None, None
    for i, url in enumerate(urls):
        if url == playlist_slice[0]:
            start_i = i

        elif url == playlist_slice[1]:
            end_i = i

    if start_i == None:
        print('Couldn\'t find slice start entry url.')
        return None
    
    elif end_i == None:
        print('Couldn\'t find slice end entry url.')
        return None

    elif start_i > end_i:
        print('Your entered start entry come after end entry.')
        return None

    return urls[start_i : end_i + 1]

def get_playlist_info(url):
    ydl_opts = {
    'extract_flat': True, # Extracts superficial metadata.
    'skip_download': True,
    'noplaylist': False,

    # Lowering console prints.
    'quiet': True,
    'no_warnings': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, False)

    return info

def download_playlist(info, save_file_path, download_state, playlist_slice):
    ydl_opts = {
        'outtmpl': None, # Directory\Name set dynamically before downloading.

        # Sleep options to prevent rate-limit soft ban.
        'sleep_interval': 3,
        'max_sleep_interval': 7,

        # Lowering console prints.
        'no_warnings': True,
    }

    if download_state == DOWNLOAD_STATES['video and audio']:
        ydl_opts.update({
            'format': 'bestvideo+bestaudio/best', # Download highest quality video and audio separately. If not possible download best alternative.
            'merge_output_format': 'mp4',
        })

    elif download_state == DOWNLOAD_STATES['video only']:
        ydl_opts.update({
            'format': 'bestvideo[ext=mp4]/best', # Download highest quality mp4 video. If not available download best alternative.
            'merge_output_format': 'mp4',
        })

    elif download_state == DOWNLOAD_STATES['audio only']:
        ydl_opts.update({
            'format': 'm4a/bestaudio/best', # Select most suitable format in order: m4a, separate audio, video file.
            'postprocessors': [{
                'key': 'FFmpegExtractAudio', # If video file format, extract audio.
                'preferredcodec': 'm4a' # If not m4a already, convert to m4a.
            }],
        })

    # Downloading entries inside of playlist.
    urls = [entry_info['url'] for entry_info in info['entries']]
    slice_urls = get_slice_url_list(playlist_slice, urls)
    if not slice_urls: return

    with YoutubeDL(ydl_opts) as ydl:
        ydl_opts['outtmpl'] = save_file_path + '/' + '%(title)s.%(ext)s'
        ydl.download(slice_urls)

def main():
    url = input('Enter url to playlist for download: ')
    save_file_path = input('Enter file path to save in: ')

    download_state = None
    while download_state not in ('1', '2', '3'):
        download_state = input('Download video & audio(1), video only(2), audio only(3): ')

    # Get the url of start and end entries if user wants to download a slice of the playlist.
    playlist_slicing = None
    while playlist_slicing not in ('Y', 'N'):
        playlist_slicing = input('Do you want to download the entire playlist? Yes(Y)/No(N): ').upper()

    if playlist_slicing == 'N':
        playlist_slice = slice_playlist()
    else:
        playlist_slice = None

    print('Extracting playlist information.')
    playlist_info = get_playlist_info(url)
    if not playlist_info['entries']:
        print('Playlist has no videos or provided link isn\'t of playlist.')
        return

    save_file_path = save_file_path + '/' + playlist_info['title'] # Downloading inside a folder named the title of the playlist.
    download_playlist(playlist_info, save_file_path, download_state, playlist_slice)

if __name__ == '__main__':
    main()