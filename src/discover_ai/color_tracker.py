from dataclasses import dataclass
from json import load
import cv2
import numpy as np

@dataclass
class Range:
    min: int
    max: int

@dataclass
class ColorTracker:
    hue: Range
    saturation: Range
    value: Range

    @staticmethod
    def create() -> "ColorTracker":
        with open("settings.json", "r") as file:
            loaded_data = load(file)

        # Structure JSON attendue : "color_filter": { "hue": {...}, "saturation": {...}, "value": {...} }
        cfg = loaded_data["color_filter"]
        hue = "hue"
        saturation = "saturation"
        value = "value"
        min_range = "min"
        max_range = "max"

        assert 0 <= cfg[hue][min_range] <= cfg[hue][max_range] <= 179
        assert 0 <= cfg[saturation][min_range] <= cfg[saturation][max_range] <= 255
        assert 0 <= cfg[value][min_range] <= cfg[value][max_range] <= 255

        return ColorTracker(
            hue=Range(min=cfg[hue][min_range], max=cfg[hue][max_range]),
            saturation=Range(min=cfg[saturation][min_range], max=cfg[saturation][max_range]),
            value=Range(min=cfg[value][min_range], max=cfg[value][max_range])
        )


class ColorFilter:

    def filter_color(self, frame, color_tracker: ColorTracker):
        # 1. Atténuation du bruit sur l'image source (noyau 5x5 est un bon compromis)
        blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)

        # 2. Conversion en HSV
        hsv_frame = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

        # 3. Seuillage selon les bornes HSV
        min_hsv = np.array([
            color_tracker.hue.min,        # H: 0 à 179
            color_tracker.saturation.min, # S: 0 à 255
            color_tracker.value.min       # V: 0 à 255
        ])

        max_hsv = np.array([
            color_tracker.hue.max,
            color_tracker.saturation.max,
            color_tracker.value.max
        ])

        mask = cv2.inRange(hsv_frame, min_hsv, max_hsv)

        # 4. Nettoyage morphologique du masque binaire
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)   # Supprime le bruit extérieur
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # Comble les trous intérieurs

        # 5. Application du masque sur l'image d'origine
        return cv2.bitwise_and(frame, frame, mask=mask)