import threading
import tkinter as tk
from tkinter import ttk, messagebox
import yt_dlp


def make_progress_hook(bar, status, root):
    def hook(d):
        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate", 0)
            downloaded = d.get("downloaded_bytes", 0)
            if total > 0:
                pct = downloaded / total * 100
                root.after(0, lambda p=pct: bar.configure(value=p))
                root.after(0, lambda p=pct: status.configure(text=f"Downloading... {p:.1f}%"))
        elif d["status"] == "finished":
            root.after(0, lambda: status.configure(text="Processing..."))
    return hook


def download(url, mode, bar, status, root):
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
    opts[mode]["progress_hooks"] = [make_progress_hook(bar, status, root)]
    with yt_dlp.YoutubeDL(opts[mode]) as ydl:
        ydl.download([url])


def start_download(entry, bar, status, root, mode):
    url = entry.get().strip()
    if not url:
        messagebox.showwarning("No URL", "Paste a YouTube URL first.")
        return
    bar["value"] = 0
    status.configure(text="Starting...")

    def run():
        try:
            download(url, mode, bar, status, root)
            root.after(0, lambda: bar.configure(value=100))
            root.after(0, lambda: status.configure(text="Done!"))
        except Exception as e:
            root.after(0, lambda: status.configure(text="Error"))
            root.after(0, lambda: messagebox.showerror("Error", str(e)))

    threading.Thread(target=run, daemon=True).start()


def main():
    BG       = "#1e1e2e"
    SURFACE  = "#313244"
    TEXT     = "#cdd6f4"
    SUBTEXT  = "#a6adc8"
    MUTED    = "#6c7086"
    BLUE     = "#89b4fa"
    GREEN    = "#a6e3a1"

    root = tk.Tk()
    root.title("yt4me")
    root.resizable(False, False)
    root.configure(bg=BG)

    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("TProgressbar",
                    troughcolor=SURFACE,
                    background=BLUE,
                    borderwidth=0,
                    thickness=8)

    # Title
    tk.Label(root, text="yt4me", font=("Segoe UI", 22, "bold"),
             bg=BG, fg=TEXT).pack(pady=(28, 0))
    tk.Label(root, text="YouTube Downloader", font=("Segoe UI", 10),
             bg=BG, fg=MUTED).pack(pady=(2, 22))

    # URL field
    tk.Label(root, text="YouTube URL", font=("Segoe UI", 9),
             bg=BG, fg=SUBTEXT).pack(anchor="w", padx=28)
    entry = tk.Entry(root, width=48, font=("Segoe UI", 10),
                     bg=SURFACE, fg=TEXT, insertbackground=TEXT,
                     relief="flat", bd=8, highlightthickness=0)
    entry.pack(padx=24, fill="x")

    # Progress bar
    bar = ttk.Progressbar(root, length=380, mode="determinate", style="TProgressbar")
    bar.pack(padx=24, pady=(20, 6), fill="x")

    # Status
    status = tk.Label(root, text="Ready", font=("Segoe UI", 9), bg=BG, fg=MUTED)
    status.pack(pady=(0, 18))

    # Buttons
    btn_frame = tk.Frame(root, bg=BG)
    btn_frame.pack(pady=(0, 28))

    btn_kw = dict(font=("Segoe UI", 10, "bold"), bd=0, relief="flat",
                  cursor="hand2", width=13, pady=8)

    tk.Button(btn_frame, text="Download MP3",
              bg=BLUE, fg=BG, activebackground="#74c7ec", activeforeground=BG,
              command=lambda: start_download(entry, bar, status, root, "mp3"),
              **btn_kw).pack(side="left", padx=6)

    tk.Button(btn_frame, text="Download MP4",
              bg=GREEN, fg=BG, activebackground="#94e2d5", activeforeground=BG,
              command=lambda: start_download(entry, bar, status, root, "mp4"),
              **btn_kw).pack(side="left", padx=6)

    root.mainloop()


if __name__ == "__main__":
    main()
