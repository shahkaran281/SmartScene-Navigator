import cv2
import time
from scenedetect import SceneManager, open_video, ContentDetector, AdaptiveDetector
import numpy as np
from shot import Shot
from blockmatching import *
from blockmatching import block_matching
from blockmatching import clustering

from numpy import int64
from typing import Dict, List
from dataclasses import dataclass, asdict
import json
import argparse


@dataclass
class describe_shot():
    timestamp: int64
    shots: Dict


@dataclass
class Build_JSON():

    @classmethod
    def populate_dict(self, dict_scene_and_shot, dict_shot_and_subshot, frame_to_time):
        scene_dict = {}
        shot_count = 0
        for scene in dict_scene_and_shot:
            shot_dict = {}
            scene_count = 0
            for shot_timestamp in dict_scene_and_shot[scene]:
                subsots = []
                subshot_count = 0
                if (shot_timestamp in dict_shot_and_subshot):
                    for val in dict_shot_and_subshot[shot_timestamp]:
                        subsots.append(
                            {str(subshot_count): frame_to_time[val]})
                        subshot_count += 1
                shot_dict[scene_count] = {
                    "timestamp":   frame_to_time[shot_timestamp], "subshots": subsots}
                scene_count += 1
            shot = asdict(describe_shot(
                timestamp=frame_to_time[scene], shots=shot_dict))
            scene_dict[shot_count] = shot
            shot_count += 1
        return scene_dict


class Video:
    def __init__(self, frame_path):
        self.file_name = frame_path
        self.frames = None
        self.cutting_list = None
        self.subshot_list = None
        self.shots = None
        self.timestamps = None
        self.detect_scenes()
        self.get_frames()
        self.get_shots()
        self.get_subshots()

    def on_new_scene(self, frame_img: np.ndarray, frame_num: int):
        self.cutting_list.append(frame_num)

    def on_new_subshot(self, frame_img: np.ndarray, frame_num: int):
        self.subshot_list.append(frame_num)

    def get_frames(self):
        cap = cv2.VideoCapture(self.file_name)
        frames = []
        while (True):
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)
        frames = np.array(frames)
        self.frames = frames
        cap.release()

    def get_shots(self):
        shots = []
        i = 0
        s = 0
        for frame in self.cutting_list:
            shot = Shot(num=s, start=i, end=frame)
            shots.append(shot)
            s += 1
            i = frame
        self.shots = shots

    # Method which finds the scenes after doing block matching

    def block_matching_python(self):
        shots = []
        for i in range(len(self.cutting_list)):
            old_frame = cv2.cvtColor(
                self.frames[self.cutting_list[i]], cv2.COLOR_BGR2GRAY)
            curr_frame = cv2.cvtColor(
                self.frames[self.cutting_list[i]+1], cv2.COLOR_BGR2GRAY)
            XP, YP, XD, YD = block_matching(old_frame, curr_frame, 4, 4)
            U, V, object_tops, meand = clustering(XP, YP, XD, YD)
            meand = np.atleast_2d(meand)
            motion_score = self.get_motion_score_of_two_frames(np.array(meand))
            print("Between frame " + str(self.cutting_list[i]) + " " + str(
                self.cutting_list[i]+1) + " " + str(motion_score))
            if (motion_score > 190 or i == 0):
                shots.append(self.cutting_list[i])
        return shots

    def get_timestamp(self):
        timestamps = {}
        cap = cv2.VideoCapture(self.file_name)
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        for i in range(len(self.cutting_list)):
            timestamp = self.cutting_list[i] / fps
            timestamps[self.cutting_list[i]] = timestamp

        for i in range(len(self.subshot_list)):
            timestamp = self.subshot_list[i] / fps
            timestamps[self.subshot_list[i]] = timestamp

        self.timestamps = timestamps
        return self.timestamps

    def get_motion_score_of_two_frames(self, meand):
        if meand.size == 0 or meand.shape[1] == 0:
            return 0
        return sum(np.sqrt(np.square(meand[:, 0]) + np.square(meand[:, 1])))

    def detect_scenes(self):
        self.cutting_list = [0]
        video = open_video(self.file_name)
        scene_manager = SceneManager()
        scene_manager.add_detector(ContentDetector(threshold=25))
        scene = scene_manager.detect_scenes(
            video=video, callback=self.on_new_scene)
        print("cutting list")
        print(self.cutting_list)

    def get_subshots(self):
        self.subshot_list = []
        video = open_video(self.file_name)
        scene_manager = SceneManager()
        scene_manager.add_detector(ContentDetector(threshold=10))
        scene = scene_manager.detect_scenes(
            video=video, callback=self.on_new_subshot)
        print(self.subshot_list)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, required=True)
    parser.add_argument('--folder', type=str, required=True)
    args = parser.parse_args()
    folder = args.folder
    video_name = 'output.mp4'
    video = Video(folder+'/' + video_name)

    scenes = video.block_matching_python()

    # Gets the scene and the corresponding shots.

    dict_scene_and_shot = {}
    for i in range(len(scenes)-1):
        left_index = scenes[i]
        right_index = scenes[i+1]
        for shot in video.cutting_list:
            if (shot >= left_index and shot < right_index):
                if scenes[i] not in dict_scene_and_shot:
                    dict_scene_and_shot[scenes[i]] = [shot]
                else:
                    dict_scene_and_shot[scenes[i]].append(shot)

    for shot in video.cutting_list:
        if (shot > scenes[-1]):
            if (scenes[-1] not in dict_scene_and_shot):
                dict_scene_and_shot[scenes[-1]] = [shot]
            else:
                dict_scene_and_shot[scenes[-1]].append(shot)

    print(dict_scene_and_shot)
    dict_shot_and_subshot = {}

    subshot_array = []
    for key, value in dict_scene_and_shot.items():
        subshot_array.append(key)
        subshot_array.extend(value)
    subshot_array.pop(0)

    for i in range(len(subshot_array)-1):
        left_val = subshot_array[i]
        right_val = subshot_array[i+1]
        if (left_val not in dict_scene_and_shot):
            for subshot in video.subshot_list:
                if (subshot > left_val and subshot < right_val):
                    if (left_val not in dict_shot_and_subshot):
                        dict_shot_and_subshot[left_val] = [subshot]
                    else:
                        dict_shot_and_subshot[left_val].append(subshot)

    print(dict_shot_and_subshot)

    scene_dict = Build_JSON().populate_dict(dict_scene_and_shot,
                                            dict_shot_and_subshot, video.get_timestamp())
    json_out = json.dumps(scene_dict, indent=4)
    f = open(args.file, "w")
    f.write(json_out)
