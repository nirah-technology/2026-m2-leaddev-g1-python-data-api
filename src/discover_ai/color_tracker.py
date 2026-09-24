from dataclasses import dataclass
from json import load
import cv2
import numpy as np

@dataclass
class ColorRange:
    min: int
    max: int

@dataclass
class ColorTracker:
    red: ColorRange
    green: ColorRange
    blue: ColorRange

    @staticmethod
    def create() -> "ColorTracker":

        with open("settings.json", 'r') as file:
            loaded_data = load(file)

        red = ColorRange(
            min=loaded_data["color_filter"]["red"]["min"], 
            max=loaded_data["color_filter"]["red"]["max"]
        )
        green = ColorRange(
                    min=loaded_data["color_filter"]["green"]["min"], 
                    max=loaded_data["color_filter"]["green"]["max"]
                )
        blue = ColorRange(
                    min=loaded_data["color_filter"]["blue"]["min"], 
                    max=loaded_data["color_filter"]["blue"]["max"]
                )

        color_tracker = ColorTracker(
            blue=blue,
            green=green, 
            red=red
        )
        return color_tracker

class ColorFilter:

    def filter_color(self, frame, color_tracker: ColorTracker):
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        min_filter_color = np.array([
                color_tracker.blue.min,
                color_tracker.green.min,
                color_tracker.red.min
            ])

        max_filter_color = np.array([
                color_tracker.blue.max,
                color_tracker.green.max,
                color_tracker.red.max
            ])

        mask = cv2.inRange(hsv_frame, min_filter_color, max_filter_color)

        masked_frame = cv2.bitwise_and(frame, frame, mask=mask)


        return masked_frame