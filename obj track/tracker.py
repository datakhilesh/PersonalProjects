import os
import random
import cv2
import streamlit as st
import numpy as np
from ultralytics import YOLO
from deep_sort.deep_sort.tracker import Tracker as DeepSortTracker
from deep_sort.tools import generate_detections as gdet
from deep_sort.deep_sort import nn_matching
from deep_sort.deep_sort.detection import Detection

class Tracker:
    tracker = None
    encoder = None
    tracks = None

    def __init__(self):
        max_cosine_distance = 0.4
        nn_budget = None

        # Use a placeholder URL to load the model from Ultralytics repository
        model_url = "https://ultralytics.com/assets/models/yolov5/yolov5s.pt"

        metric = nn_matching.NearestNeighborDistanceMetric("cosine", max_cosine_distance, nn_budget)
        self.tracker = DeepSortTracker(metric)
        self.encoder = gdet.create_box_encoder(model_url, batch_size=1)

    def update(self, frame, detections):
        if len(detections) == 0:
            self.tracker.predict()
            self.tracker.update([])  
            self.update_tracks()
            return

        bboxes = np.asarray([d[:-1] for d in detections])
        bboxes[:, 2:] = bboxes[:, 2:] - bboxes[:, 0:2]
        scores = [d[-1] for d in detections]

        features = self.encoder(frame, bboxes)

        dets = []
        for bbox_id, bbox in enumerate(bboxes):
            dets.append(Detection(bbox, scores[bbox_id], features[bbox_id]))

        self.tracker.predict()
        self.tracker.update(dets)
        self.update_tracks()

    def update_tracks(self):
        tracks = []
        for track in self.tracker.tracks:
            if not track.is_confirmed() or track.time_since_update > 1:
                continue
            bbox = track.to_tlbr()

            id = track.track_id

            tracks.append(Track(id, bbox))

        self.tracks = tracks

class Track:
    track_id = None
    bbox = None

    def __init__(self, id, bbox):
        self.track_id = id
        self.bbox = bbox

def main():
    st.title("Object Tracking with YOLO and DeepSORT")

    # File upload widget for video
    uploaded_file = st.file_uploader("Choose a video file", type=["mp4"])

    if uploaded_file is not None:
        # Video processing
        cap = cv2.VideoCapture(uploaded_file)
        ret, frame = cap.read()

        # Initialize YOLO and Tracker
        model = YOLO("yolov5s.pt")  # Model file will be downloaded automatically
        tracker = Tracker()
        colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(10)]
        detection_threshold = 0.5

        # Video output setup
        video_out = st.video("", format="mp4", start_time=0)

        while ret:
            results = model(frame)

            for result in results:
                detections = []
                for r in result.boxes.data.tolist():
                    x1, y1, x2, y2, score, class_id = r
                    x1 = int(x1)
                    x2 = int(x2)
                    y1 = int(y1)
                    y2 = int(y2)
                    class_id = int(class_id)
                    if score > detection_threshold:
                        detections.append([x1, y1, x2, y2, score])

                tracker.update(frame, detections)

                for track in tracker.tracks:
                    bbox = track.bbox
                    x1, y1, x2, y2 = bbox
                    track_id = track.track_id

                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), colors[track_id % len(colors)], 3)

            # Display the frame in Streamlit
            video_out.frame(frame)

            ret, frame = cap.read()

        cap.release()
        st.info("Video processing completed!")

if __name__ == "__main__":
    main()
