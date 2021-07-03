import cv2
import mediapipe as mp
import math
import numpy as np

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils


def get_angle(v1, v2):
    dot = np.dot(v1, v2)
    mod_v1 = np.linalg.norm(v1)
    mod_v2 = np.linalg.norm(v2)
    cos_theta = dot/(mod_v1*mod_v2)
    theta = math.acos(cos_theta)
    return theta



def get_params(results):
    points = {}
    nose = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE]
    points["NOSE"] = np.array([nose.x, nose.y, nose.z])
    left_eye = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EYE]
    points["LEFT_EYE"] = np.array([left_eye.x, left_eye.y, left_eye.z])
    right_eye = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EYE]
    points["RIGHT_EYE"] = np.array([right_eye.x, right_eye.y, right_eye.z])
    mouth_left = results.pose_landmarks.landmark[mp_pose.PoseLandmark.MOUTH_LEFT]
    points["MOUTH_LEFT"] = np.array([mouth_left.x, mouth_left.y, mouth_left.z])
    mouth_right = results.pose_landmarks.landmark[mp_pose.PoseLandmark.MOUTH_RIGHT]
    points["MOUTH_RIGHT"] = np.array([mouth_right.x, mouth_right.y, mouth_right.z])
    left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
    points["LEFT_SHOULDER"] = np.array([left_shoulder.x, left_shoulder.y, left_shoulder.z])
    right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    points["RIGHT_SHOULDER"] = np.array([right_shoulder.x, right_shoulder.y, right_shoulder.z])
    left_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
    points["LEFT_HIP"] = np.array([left_hip.x, left_hip.y, left_hip.z])
    right_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]
    points["RIGHT_HIP"] = np.array([right_hip.x, right_hip.y, right_hip.z])
    left_knee = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE]
    points["LEFT_KNEE"] = np.array([left_knee.x, left_knee.y, left_knee.z])
    right_knee = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE]
    points["RIGHT_KNEE"] = np.array([right_knee.x, right_knee.y, right_knee.z])
    left_heel = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HEEL]
    points["LEFT_HEEL"] = np.array([left_heel.x, left_heel.y, left_heel.z])
    right_heel = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HEEL]
    points["RIGHT_HEEL"] = np.array([right_heel.x, right_heel.y, right_heel.z])
    left_foot_index = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_FOOT_INDEX]
    points["LEFT_FOOT_INDEX"] = np.array([left_foot_index.x, left_foot_index.y, left_foot_index.z])
    right_foot_index = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX]
    points["RIGHT_FOOT_INDEX"] = np.array([right_foot_index.x, right_foot_index.y, right_foot_index.z])
    left_ankle = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE]
    points["LEFT_ANKLE"] = np.array([left_ankle.x, left_ankle.y, left_ankle.z])
    right_ankle = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE]
    points["RIGHT_ANKLE"] = np.array([right_ankle.x, right_ankle.y, right_ankle.z])

    points["MID_SHOULDER"] = (points["LEFT_SHOULDER"] + points["RIGHT_SHOULDER"]) / 2
    points["MID_HIP"] = (points["LEFT_HIP"] + points["RIGHT_HIP"]) / 2

    z_eyes = (points["RIGHT_EYE"][2] + points["LEFT_EYE"][2]) / 2
    z_mouth = (points["MOUTH_LEFT"][2] + points["MOUTH_RIGHT"][2]) / 2

    theta_neck = get_angle(np.array([0, 0, -1]),
                           points["NOSE"] - points["MID_SHOULDER"])

    # theta_neck = get_angle(points["MID_HIP"] - points["MID_SHOULDER"],
    #                             points["NOSE"] - points["MID_SHOULDER"])

    z_face = z_eyes - z_mouth

    theta_k1 = get_angle(points["RIGHT_HIP"] - points["RIGHT_KNEE"],
                         points["RIGHT_ANKLE"] - points["RIGHT_KNEE"])

    theta_k2 = get_angle(points["LEFT_HIP"] - points["LEFT_KNEE"],
                         points["LEFT_ANKLE"] - points["LEFT_KNEE"])

    theta_k = (theta_k1 + theta_k2) / 2

    theta_h1 = get_angle(points["RIGHT_KNEE"] - points["RIGHT_HIP"],
                         points["RIGHT_SHOULDER"] - points["RIGHT_HIP"])

    theta_h2 = get_angle(points["LEFT_KNEE"] - points["LEFT_HIP"],
                         points["LEFT_SHOULDER"] - points["LEFT_HIP"])

    theta_h = (theta_h1 + theta_h2) / 2

    z1 = (points["RIGHT_ANKLE"][2] + points["RIGHT_HEEL"][2]) / 2 - points["RIGHT_FOOT_INDEX"][2]

    z2 = (points["LEFT_ANKLE"][2] + points["LEFT_HEEL"][2]) / 2 - points["LEFT_FOOT_INDEX"][2]

    z = (z1 + z2) / 2

    left_foot_y = (points["LEFT_ANKLE"][1] + points["LEFT_HEEL"][1] + points["LEFT_FOOT_INDEX"][1]) / 3
    right_foot_y = (points["RIGHT_ANKLE"][1] + points["RIGHT_HEEL"][1] + points["RIGHT_FOOT_INDEX"][1]) / 3

    left_ky = points["LEFT_KNEE"][1] - left_foot_y
    right_ky = points["RIGHT_KNEE"][1] - right_foot_y

    ky = (left_ky + right_ky) / 2

    params = np.array([theta_neck, theta_k, theta_h, z, ky])

    return params