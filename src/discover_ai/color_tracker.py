from dataclasses import dataclass
from json import load
import cv2

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


        return hsv_frame