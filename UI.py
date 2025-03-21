import cv2
import tkinter as tk
from PIL import Image, ImageTk
import pygame
import os
import json
import tkinter.ttk as ttk
import numpy as np
import sys

arg1 = sys.argv[1]
arg2 = sys.argv[2]

# Initialize pygame mixer for audio playback
pygame.mixer.init()
current_frame_time_stamp = 0

rgb_file = arg1
width, height = 480, 270


def read_rgb_file(file_name):
    global width, height
    with open(file_name, 'rb') as f:
        data = f.read()
    # print(data.shape)
    frame_count = len(data) // (width * height * 3)
    frames = np.frombuffer(data, dtype=np.uint8).reshape(
        (frame_count, height, width, 3))

    return frames


oldrgb_frames = read_rgb_file(rgb_file)

rgb_frames = []
for i in oldrgb_frames:
    rgb_frame = cv2.cvtColor(i, cv2.COLOR_BGR2RGB)
    rgb_frames.append(rgb_frame)

frame_count = len(rgb_frames)
fps = 30  # Replace with the correct frames per second value
current_frame_index = 0

# Load the audio file
audio_file = arg2

# Define a flag to keep track of whether the video is playing or paused
is_playing = True

# Check if audio file exists, if not, extract audio from video
# if not os.path.exists(audio_file):
#     os.system(f"ffmpeg -i InputVideo.mp4 -q:a 0 -map a {audio_file}")


def data_json(file_name):
    with open(file_name) as f:
        data = json.load(f)
    return data


time_stamps = []
label_video = []

data = data_json('long_dark_v2.json')
for key in data:
    scene_num = int(key)+1
    scene_timestamp = data[key]["timestamp"]
    time_stamps.append(scene_timestamp)
    scenelabel = "scene"+str(scene_num)
    label_video.append(scenelabel)
    shots = data[key]["shots"]
    # Gives the scene_num , scene_timestamp , shot_num , shot_timestamp
    for index, shot in enumerate(shots):
        # print(scene_num , scene_timestamp , shot , shots[shot]["timestamp"])
        time_stamps.append(shots[shot]["timestamp"])
        shotlabel = scenelabel + " shot" + str(index+1)
        label_video.append(shotlabel)
        subshots = shots[shot]["subshots"]
        print(len(subshots))
        for subindex, pair in enumerate(subshots):
            keysubshot = str(subindex)
            time_stamps.append(pair[keysubshot])
            subshotlabel = shotlabel + " subshot" + str(subindex+1)
            print(shotlabel, " subshot ", pair[keysubshot])
            label_video.append(subshotlabel)


# Define a list of time stamps for the video
# time_stamps = [0, 10, 20, 30, 40, 50]

# Define a variable to keep track of the playback speed
playback_speed = 1.0
update_scheduled = False
playing_timestamp = 0
update_id = None
current_frame_index = 0

# Define a function to handle the play button click event


def play():
    global is_playing
    is_playing = True

    if (update_id):
        root.after_cancel(update_id)

    # Start playing audio only if it's not already playing
    if pygame.mixer.music.get_busy() == 0:

        # current_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
        current_time = current_frame_index / fps
        print("play time:", current_time)
        pygame.mixer.music.play(-1, current_time)

    pygame.mixer.music.unpause()
    update_video()


def pause():
    global is_playing
    is_playing = False
    pygame.mixer.music.pause()

# Define a function to handle the stop button click event


def stop():
    global is_playing, playback_speed, current_frame_index
    is_playing = False
    playback_speed = 1.0
    print("stop time:", current_frame_time_stamp)
    current_frame_index = int(current_frame_time_stamp * fps)
    # cap.set(cv2.CAP_PROP_POS_FRAMES, int(current_frame_time_stamp * cap.get(cv2.CAP_PROP_FPS)))
    pygame.mixer.music.stop()
    # update_video(only_frame=True)
    # play()

# Define a function to handle the time stamp button click event


def seek(time):
    global current_frame_time_stamp, current_frame_index
    current_frame_time_stamp = time
    global playback_speed, playing_timestamp
    playback_speed = 1.0
    playing_timestamp = time
    current_frame_time_stamp = time
    current_frame_index = int(time * fps)
    # cap.set(cv2.CAP_PROP_POS_FRAMES, int(time * cap.get(cv2.CAP_PROP_FPS)))
    print("seek time:", current_frame_time_stamp)
    if is_playing:
        pygame.mixer.music.set_pos(time)
    else:
        play()
        pygame.mixer.music.set_pos(time)
        pause()


root = tk.Tk()
root.title('Video Player')

player_frame = tk.Frame(root)
player_frame.pack(side=tk.RIGHT)

# sidebar_frame = tk.Frame(root)
# sidebar_frame.pack(side=tk.LEFT)

sidebar_treeview = ttk.Treeview(root)
sidebar_treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(root, orient="vertical",
                          command=sidebar_treeview.yview)
scrollbar.pack(side=tk.LEFT, fill=tk.Y)
sidebar_treeview.configure(yscrollcommand=scrollbar.set)


label = tk.Label(player_frame)
label.pack(side=tk.TOP)

controls_frame = tk.Frame(player_frame)
controls_frame.pack(side=tk.BOTTOM)

play_button = tk.Button(controls_frame, text='Play', command=play)
play_button.pack(side=tk.LEFT)

pause_button = tk.Button(controls_frame, text='Pause', command=pause)
pause_button.pack(side=tk.LEFT)

stop_button = tk.Button(controls_frame, text='Stop', command=stop)
stop_button.pack(side=tk.LEFT)


# Creating Buttons for timestamps

# for time in time_stamps:
#     time_button = tk.Button(sidebar_frame, text=str(time), command=lambda t=time: seek(t))
#     time_button.pack(side=tk.TOP, fill=tk.X)


# for index, time in enumerate(time_stamps):
#     time_button = tk.Button(sidebar_frame, text=label_video[index], command=lambda t=time: seek(t))
#     time_button.pack(side=tk.TOP, fill=tk.X)


# Create a dictionary to store the timestamps for each Treeview item
timestamp_dict = {}

# Create timestamp buttons and add them as items in the Treeview
for index, time in enumerate(time_stamps):
    item_text = f"{label_video[index]}"  # Use only the label for the button
    item_id = sidebar_treeview.insert('', 'end', text=item_text)
    timestamp_dict[item_id] = time  # Store the timestamp in the dictionary


def on_treeview_select(event):
    item = sidebar_treeview.focus()
    # item = sidebar_treeview.selection()[0]
    # Retrieve the timestamp value from the dictionary
    time = timestamp_dict[item]
    # sidebar_treeview.selection_set(item)
    seek(time)


sidebar_treeview.bind('<<TreeviewSelect>>', on_treeview_select)
sidebar_treeview.tag_configure("highlight", background="yellow")


def update_video(only_frame=False):
    global is_playing, playback_speed, playing_timestamp, update_id, current_frame_index
    print(timestamp_dict)
    if is_playing or only_frame:
        # current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
        current_time = current_frame_index / fps
        selected_button = None
        for button in timestamp_dict.items():
            if abs(button[1] - current_time) < 0.1:
                selected_button = button
                break

        # Scroll to and highlight the selected button
        if selected_button is not None:
            sidebar_treeview.see(selected_button[0])
            # sidebar_treeview.selection_set(selected_button[0])
            for child in sidebar_treeview.get_children():
                sidebar_treeview.item(child, tags="")
            sidebar_treeview.item(selected_button[0], tags=("highlight",))
            sidebar_treeview.focus(selected_button[0])

        # ret, frame = cap.read()
        frame = rgb_frames[current_frame_index]
        current_frame_index += 1

        # print("ret value", ret)

        if current_frame_index >= frame_count:
            is_playing = False
            pygame.mixer.music.stop()
            return

        # if not ret:
        #    is_playing = False
        #    pygame.mixer.music.stop()
        #    return

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)

        label.configure(image=image)
        label.image = image
        if is_playing:
            print("playing at ", fps)
            update_id = root.after(int(1000 / fps), update_video)

    # else:
    #     # If the video is paused, we still need to schedule an update to check if the video starts playing again
    #     root.after(100, update_video)
    #     pass


update_video()

# Loading audio
pygame.mixer.music.load(audio_file)
pygame.mixer.music.play(-1)

# Start the tkinter event loop

root.mainloop()
# Release the VideoCapture object when the window is closed
# cap.release()

# Stop the pygame mixer when the window is closed
pygame.mixer.quit()
