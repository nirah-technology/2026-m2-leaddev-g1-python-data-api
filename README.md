class ColorFilter:

    def filter_color(self, frame, color_tracker: ColorTracker):
        # 1. Atténuation du bruit sur l'image source avec un flou gaussien
        blurred_frame = cv2.GaussianBlur(frame, (11, 11), 0)

        hsv_frame = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

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

        # 2. Nettoyage des petits points parasites restants sur le masque binaire
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        # (Optionnel) Flou médian direct sur le masque pour adoucir les contours
        # mask = cv2.medianBlur(mask, 5)

        masked_frame = cv2.bitwise_and(frame, frame, mask=mask)

        return masked_frame