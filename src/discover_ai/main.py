import cv2
import time

from .color_tracker import ColorFilter, ColorTracker

def main():
    capture = cv2.VideoCapture(0)
    is_streaming: bool = True

    while is_streaming:
        has_frame, frame = capture.read()
        if (has_frame):

            # print(frame.shape)

            zoom = 0.25
            resized_frame = cv2.resize(frame, (0,0), fx=zoom, fy=zoom)

            #  rotated_frame = cv2.rotate(resized_frame, cv2.ROTATE_90_CLOCKWISE)

            gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
            gray_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)
            flipped_frame = cv2.flip(gray_frame, 1)

            little_height, little_width, _ = flipped_frame.shape

            frame[10:10+little_height, 10:10+little_width] = flipped_frame
            flipped_frame = cv2.flip(flipped_frame, 1)
            frame[110:110+little_height, 110:110+little_width] = flipped_frame


            color_filter = ColorFilter()
            color_tracker = ColorTracker.create()

            filtered_color_frame = color_filter.filter_color(frame, color_tracker)

            cv2.imshow("Enetre OpenCV", filtered_color_frame)

        if (cv2.waitKey(1) == ord('q')):
            is_streaming = False
            cv2.destroyAllWindows()

if (__name__ == "__main__"):
    main()
