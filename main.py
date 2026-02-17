import threading, tkinter as tk
from tkinter import messagebox
import yt_dlp

def download(url, mode):
    opts = {
        "mp3": {
            "format": "bestaudio/best",
            "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "0"}],
            "outtmpl": "%(title)s.%(ext)s",
        },
        "mp4": {
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "outtmpl": "%(title)s.%(ext)s",
            "merge_output_format": "mp4",
        },
    }
    with yt_dlp.YoutubeDL(opts[mode]) as ydl:
        ydl.download([url])

def start_download(entry, status_label, mode):
    url = entry.get().strip()
    if not url:
        messagebox.showwarning("No URL", "Paste a YouTube URL first.")
        return
    status_label.config(text="Downloading...")
    def run():
        try:
            download(url, mode)
            status_label.config(text="Done!")
        except Exception as e:
            status_label.config(text="Error")
            messagebox.showerror("Error", str(e))
    threading.Thread(target=run, daemon=True).start()

def main():
    root = tk.Tk()
    root.title("yt4me")
    root.resizable(False, False)

    tk.Label(root, text="YouTube URL:").pack(padx=20, pady=(20, 4))
    entry = tk.Entry(root, width=50)
    entry.pack(padx=20)

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=12)
    status = tk.Label(root, text="Ready", fg="gray")
    status.pack(pady=(0, 16))

    tk.Button(btn_frame, text="Download MP3", width=14,
              command=lambda: start_download(entry, status, "mp3")).pack(side="left", padx=6)
    tk.Button(btn_frame, text="Download MP4", width=14,
              command=lambda: start_download(entry, status, "mp4")).pack(side="left", padx=6)

    root.mainloop()

if __name__ == "__main__":
    main()
