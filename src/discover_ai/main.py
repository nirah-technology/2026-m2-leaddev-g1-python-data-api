import cv2
import time
import numpy as np

from .color_tracker import ColorFilter, ColorTracker

def main():
    capture = cv2.VideoCapture("vehicle-flow.mp4")

    fps = capture.get(cv2.CAP_PROP_FPS)
    delay = int(1000/fps)

    is_streaming: bool = True

    # Instanciation en dehors de la boucle pour éviter de recréer les objets à chaque frame
    color_filter = ColorFilter()

    zoom = 0.65

    while is_streaming:
        color_tracker = ColorTracker.create()
        has_frame, frame = capture.read()
        if has_frame:
            # Redimensionnement de l'image source
            resized_original_frame = cv2.resize(frame, (0, 0), fx=zoom, fy=zoom)
            
            # Récupération de la hauteur (h), largeur (w) et canaux (c)
            h, w, c = resized_original_frame.shape

            # Création du fond vertical : hauteur x 2, largeur originale
            background_frame = np.zeros((h * 2, w, c), np.uint8)

            # Application du filtre
            filtered_color_frame = color_filter.filter_color(resized_original_frame, color_tracker)

            # Image originale en haut (de la ligne 0 à h)
            background_frame[0:h, 0:w] = resized_original_frame

            # Image filtrée en bas (de la ligne h à 2*h)
            background_frame[h:2*h, 0:w] = filtered_color_frame

            cv2.imshow("Entre OpenCV", background_frame)

        else:
            capture.set(cv2.CAP_PROP_POS_FRAMES, 0)

        if cv2.waitKey(delay) == ord('q'):
            is_streaming = False

    capture.release()
    cv2.destroyAllWindows()

if (__name__ == "__main__"):
    main()
