import subprocess
import sys
import shutil

# --- ANSI color codes ---
RED = "\033[91m"
RESET = "\033[0m"


def print_title():
    print(f"{RED}{'=' * 40}{RESET}")
    print("Dead Video Downloader")
    print(f"{RED}{'=' * 40}{RESET}")


# --- Check if 'yt-dlp' is installed, prompt to install if not ---
try:
    import yt_dlp
except ImportError:
    print("You need yt-dlp to download videos.")
    answer = input("Download and install it now? (y/n): ").strip().lower()
    if answer == 'y':
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
            import yt_dlp  # try importing again after install
            print("yt-dlp installed successfully.\n")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install yt-dlp: {e}")
            sys.exit(1)
    else:
        print("Cannot continue without yt-dlp. Exiting.")
        sys.exit(1)

from pathlib import Path


def check_ffmpeg():
    if shutil.which("ffmpeg") is None:
        print("\nWarning: ffmpeg is not installed.")
        print("Some videos (especially high-res YouTube videos) need ffmpeg to merge audio/video.")
        print("Downloads may fail or be lower quality without it.")
        answer = input("Continue anyway? (y/n): ").strip().lower()
        if answer != 'y':
            print("Exiting. Install ffmpeg and run this script again.")
            sys.exit(1)


def download_file():
    print_title()

    save_path = Path.home() / "Downloads"
    save_path.mkdir(parents=True, exist_ok=True)

    check_ffmpeg()

    while True:
        url = input(f"\n{RED}Enter video URL (or 'q' to quit): {RESET}").strip()

        if url.lower() == 'q':
            break

        if not url:
            print("error: empty URL")
            continue

        ydl_opts = {
            'outtmpl': str(save_path / '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            print(f"downloaded successfully to {save_path}")

        except yt_dlp.utils.DownloadError as e:
            print(f"error: yt-dlp could not download this video ({e})")
        except Exception as e:
            print(f"error: something went wrong ({e})")


if __name__ == "__main__":
    download_file()