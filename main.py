from yt_dlp import YoutubeDL

DOWNLOAD_STATES = {
    'video and audio': '1',
    'video only': '2',
    'audio only': '3'
}

def print_title_list(title_list):
    print()
    for i, title in enumerate(title_list):
        print(f'{i + 1}. {title}')
    print()

def get_playlist_slice(want_full_download, title_list):
    if want_full_download == 'N':
        print_title_list(title_list)
        start, end = float('inf'), float('inf')
        while not 0 <= start < end <= len(title_list):
            start, end = '', ''
            while not start.isdigit() or not end.isdigit():
                start = input('Enter the number of the entry you want to start the download with: ')
                end = input('Enter the number of the entry you want to end the download with(inclusive): ')
                if not start.isdigit() or not end.isdigit():
                    print('Enter valid numbers.')

            start, end = int(start) - 1, int(end)
            if not 0 <= start <= end <= len(title_list):
                print('Provided index\\es out of range.')

    else:
        start = 0
        end = len(title_list)
    return start, end

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

def download_playlist(save_file_path, download_state, urls):
    ydl_opts = {
        'paths': {
            'home': save_file_path,
        },
        'outtmpl': '%(title)s.%(ext)s', # Format for setting file name.

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
            'format': 'bestvideo[ext=mp4]/bestvideo', # Download highest quality mp4 video. If not available download best alternative.
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

    # Download using ydl_opts configuration.
    continue_downloading = 'Y'
    while continue_downloading == 'Y':
        with YoutubeDL(ydl_opts) as ydl:
            try:
                for i, url in enumerate(urls):
                    ydl.download(url)

                continue_downloading = 'N'
                break

            except Exception:
                if i == len(urls) - 1:
                    print('Last entry download error.')
                    continue_downloading = 'N'
                    break

                continue_downloading = None
                while continue_downloading not in ('Y', 'N'):
                    continue_downloading = input('\nDo you want to continue downloading the remaining entries? (Y\\N): ').upper()
                    if continue_downloading == 'Y':
                        urls = urls[i + 1:]

def main():
    playlist_url = input('Enter url to playlist for download: ')
    save_file_path = input('Enter file path to save in: ')

    download_state = None
    while download_state not in ('1', '2', '3'):
        download_state = input('Download video & audio(1), video only(2), audio only(3): ')

    print('Extracting playlist information.')
    playlist_info = get_playlist_info(playlist_url)
    if not playlist_info['entries']:
        print('Playlist has no videos or provided link isn\'t of playlist.')
        return

    # Get the slice indexes of the playlist that user wants to download.
    want_full_download = None
    while want_full_download not in ('Y', 'N'):
        want_full_download = input('Do you want to download the entire playlist? Yes(Y)/No(N): ').upper()

    title_list = [entry['title'] for entry in playlist_info['entries']]
    start, end = get_playlist_slice(want_full_download, title_list)

    # Downloading inside a folder named the title of the playlist.
    url_list = [entry['url'] for entry in playlist_info['entries']]
    save_file_path = save_file_path + '\\' + playlist_info['title']
    download_playlist(save_file_path, download_state, url_list[start:end])

if __name__ == '__main__':
    main()