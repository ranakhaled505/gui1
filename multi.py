import tkinter as tk
from tkinter import messagebox
import cv2
import threading
import os
import subprocess

# Utility function to check if required dependencies are available
def check_dependencies():
    try:
        subprocess.run(["yt-dlp", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["ffplay", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError as e:
        return str(e)
    return None

# Function to play audio only
def play_audio(video_path):
    if not os.path.exists(video_path):
        messagebox.showerror("Error", "Video file not found!")
        return

    try:
        subprocess.run(
            ["ffplay", "-nodisp", "-autoexit", video_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception as e:
        messagebox.showerror("Error", f"Error playing audio: {e}")

# Function to download video using yt-dlp
def download_video(url):
    output_path = "downloaded_video.mp4"
    try:
        subprocess.run(["yt-dlp", "-f", "mp4", "-o", output_path, url], check=True)
        return output_path
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Failed to download video. Check the URL or network connection.")
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error: {e}")
    return None

# Function to play video
def play_video(video_path, resolution):
    if not os.path.exists(video_path):
        messagebox.showerror("Error", "Video file not found!")
        return

    cap = cv2.VideoCapture(video_path)

    if resolution == "low":
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    elif resolution == "high":
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Video Player", frame)
        if cv2.waitKey(25) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

# Function to handle button clicks
def handle_button_click(mode):
    video_url = entry.get()
    if not video_url:
        messagebox.showerror("Error", "Please enter a video URL.")
        return

    video_path = download_video(video_url)
    if not video_path:
        return

    if mode == "audio":
        threading.Thread(target=play_audio, args=(video_path,)).start()
    else:
        threading.Thread(target=play_video, args=(video_path, mode)).start()

# Initialize GUI
root = tk.Tk()
root.title("Video Player")

# Check for dependencies
missing_dependency = check_dependencies()
if missing_dependency:
    messagebox.showerror("Dependency Error", f"Missing dependency: {missing_dependency}\nPlease install yt-dlp and FFmpeg.")
    root.destroy()

# Input field for video URL
tk.Label(root, text="Paste Link Video:").pack(pady=5)
entry = tk.Entry(root, width=50)
entry.pack(pady=5)

# Buttons for different resolutions and audio
btn_high = tk.Button(root, text="High Resolution", command=lambda: handle_button_click("high"))
btn_high.pack(pady=5)

btn_low = tk.Button(root, text="Low Resolution", command=lambda: handle_button_click("low"))
btn_low.pack(pady=5)

btn_audio = tk.Button(root, text="Audio Only", command=lambda: handle_button_click("audio"))
btn_audio.pack(pady=5)

# Start GUI mainloop
root.mainloop()