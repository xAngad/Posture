import mediapipe as mp
import SquatPosture as sp
from flask import Flask, Response, render_template
import cv2
import tensorflow as tf
import numpy as np
from utils import landmarks_list_to_array, label_params, label_final_results
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

model = tf.keras.models.load_model("working_model_1")

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

def gen(camera):
    cap = camera.video
    i = 0
    with mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            success, image = cap.read()
            image = cv2.flip(image, 1)

            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                # continue
                break

            image_height, image_width, _ = image.shape

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            dim = (image_width//5, image_height//5)

            resized_image = cv2.resize(image, dim)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            results = pose.process(resized_image)

            params = sp.get_params(results)
            flat_params = np.reshape(params, (5, 1))

            # params will be run through the model

            output = model.predict(flat_params.T)

            output[0][0] *= 0.7
            output[0][1] *= 1.7
            output[0][2] *= 4
            output[0][3] *= 0
            output[0][4] *= 5

            output = output * (1 / np.sum(output))

            output_name = ['c', 'k', 'h', 'r', 'x', 'i']

            output[0][2] += 0.1

            # print(output[0][2], output[0][3])

            label = ""

            for i in range(1, 4):
                label += output_name[i] if output[0][i] > 0.5 else ""

            if label == "":
                label = "c"

            label += 'x' if output[0][4] > 0.15 and label=='c' else ''


            # print(label, output)

            label_final_results(image, label)

            i += 1

            # mp_drawing.draw_landmarks(
            #     image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            #
            # coords = landmarks_list_to_array(results.pose_landmarks, image.shape)
            # label_params(image, params, coords)


            ret, jpeg = cv2.imencode('.jpg', image)
            frame = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


app = Flask(__name__, template_folder="./web/templates", static_folder="./web/static")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/video")
def video_feed():
    return Response(gen(VideoCamera()), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    app.run(debug=True)