import cv2
import numpy as np

class ColorTracker:
    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            raise ValueError("无法打开摄像头")
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        self.lower_red1 = np.array([0, 120, 70])
        self.upper_red1 = np.array([10, 255, 255])
        self.lower_red2 = np.array([170, 120, 70])
        self.upper_red2 = np.array([180, 255, 255])
        
        self.lower_blue = np.array([100, 100, 100])
        self.upper_blue = np.array([130, 255, 255])
        
        self.lower_yellow = np.array([20, 100, 100])
        self.upper_yellow = np.array([40, 255, 255])
        
        self.colors = {
            'red': ((0, 0, 255), (self.lower_red1, self.upper_red1), (self.lower_red2, self.upper_red2)),
            'blue': ((255, 0, 0), (self.lower_blue, self.upper_blue), None),
            'yellow': ((0, 255, 255), (self.lower_yellow, self.upper_yellow), None)
        }
        
        self.current_frame = None
        self.counts = {'red': 0, 'blue': 0, 'yellow': 0}

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        self.current_frame = frame.copy()
        return frame

    def detect_colors(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        self.counts = {'red': 0, 'blue': 0, 'yellow': 0}
        
        for color_name, (bgr_color, range1, range2) in self.colors.items():
            mask = cv2.inRange(hsv, range1[0], range1[1])
            
            if range2 is not None:
                mask2 = cv2.inRange(hsv, range2[0], range2[1])
                mask = cv2.bitwise_or(mask, mask2)
            
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)
            
            contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 500:
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), bgr_color, 2)
                    self.counts[color_name] += 1
        
        return frame

    def get_counts(self):
        return self.counts.copy()

    def save_frame(self, filename='1.jpg'):
        if self.current_frame is not None:
            cv2.imwrite(filename, self.current_frame)
            return True
        return False

    def release(self):
        self.cap.release()
