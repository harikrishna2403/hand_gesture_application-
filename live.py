import mediapipe as mp
from mediapipe import Timestamp
import cv2

class Live:
    def __init__(self, gesture_callback):
        self.gesture_callback = gesture_callback
        BaseOptions = mp.tasks.BaseOptions
        GestureRecognizer = mp.tasks.vision.GestureRecognizer
        GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
        GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
        VisionRunningMode = mp.tasks.vision.RunningMode
        cap = cv2.VideoCapture(0)
        # Create a gesture recognizer instance with the live stream mode:
        def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
            if result and result.gestures:
                top_gesture = result.gestures[0][0]
                print('Top gesture category: {}'.format(top_gesture.category_name))

        options = GestureRecognizerOptions(
            base_options=BaseOptions(model_asset_path='My_model_new1.task'),min_hand_detection_confidence=0.8, 
            running_mode=VisionRunningMode.LIVE_STREAM,
            result_callback=print_result)
        with GestureRecognizer.create_from_options(options) as recognizer:
            if not cap.isOpened():
                print('Error: Could not open video capture device')
                exit()

            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
                frame_timestamp = Timestamp(int(cap.get(cv2.CAP_PROP_POS_MSEC)))
                result = recognizer.recognize_async(mp_image, int(frame_timestamp.microseconds()))
                if result:
                    top_gesture = result.gestures[0][0]
                    self.recog(top_gesture.category_name)

                cv2.imshow('Hand Gesture Recognition', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cap.release()
            cv2.destroyAllWindows()
    def recog(self, category):
        # Call the callback function in the Media class with the recognized category
        if category:
            self.gesture_callback(category)
