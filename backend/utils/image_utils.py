import cv2
import numpy as np
from typing import List
from models.detection import Detection
from config import CLASS_NAMES

class ImageUtils:
    @staticmethod
    def crop_from_detections(frame: np.ndarray, detections: List[Detection]) -> List[np.ndarray]:
        return [frame[d.box[1]:d.box[3], d.box[0]:d.box[2]] for d in detections]

    @staticmethod
    def encode_to_jpeg(images: List[np.ndarray]) -> List[bytes]:
        encoded = []
        for img in images:
            success, buffer = cv2.imencode('.jpg', img)
            if success:
                encoded.append(buffer.tobytes())
        return encoded
    
    @staticmethod
    def draw_boxes(frame, detections):
        for d in detections:
            x1, y1, x2, y2 = d.box
            label = f"{CLASS_NAMES[d.cls_id]} {d.conf:.2f}"
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        return frame