# Posture: Pose Tracking and Machine Learning for prescribing corrective suggestions to improve posture and form while exercising.

##### THIS REPOSITORY CONTAINS MY __FORKED__ VERSION OF [Posture](https://github.com/twixupmysleeve/Posture).

> _Differences between this fork and the original:_
> - _`app_squat.py` ie. the final web app runs purely on Flask instead of Dash-Plotly_
> - _reorganized file structure, especially for front-end rendering_
> - _cleaned and pruned code_

Our project is an AI-based Personalised Exercise Feedback Assistant: an algorithm that views your exercise posture in real time and tells what you're getting right, and what you're getting wrong! 

## Demo

To run the app:
- Clone the repository: `git clone https://github.com/xAngad/Posture`
- cd into the cloned repo: `cd Posture`
- install dependencies: `python3 -m pip install -r requirements.txt`
- run app:  `python3 app_squat.py`
- click the numeric link that appears in your terminal window
- squat!

## About the project
> _Read the devpost [here](https://devpost.com/software/posture-w5670m)_

### Inspiration and Introduction
Imagine this: your days are marked by a Covid lockdown. You’re living entirely within the confines of home - a couch potato with no physical exercise outlet. With countless indefinite restrictions still imposed, basic necessities like access to gyms, gym trainers and recreational activities are still a luxury. Normally, while working out, your gym trainer would have ensured your training form was good - but alas, now you can never be sure that you got that perfect Squat, Plank, or Push-up! Performing elaborate exercises over Zoom meetings is tiring, and your form simply doesn’t get the close attention it needs.

But fret not! A group of students, boasting questionable degrees of fitness, have engineered a solution for you: an AI algorithm that views your exercise posture in real time and tells what you're getting right, and more importantly, what you're getting wrong!

We, at Posture, have taken a step towards making personal welfare infrastructure accessible at home by creating an AI-based Personalised Exercise Feedback Assistant.

### What does it do?
It’s simple! Our brilliantly named service, Posture, has got your back when you exercise. You can run our algorithm on any device by setting the camera to point at you, and viewing yourself live on screen. The best part? Once you’ve picked your exercise, our algorithm immediately begins to __provide real time audio-visual feedback about mistakes you’re making in your Posture, and also gives instructions to correct yourself!__

### Our approach
In order to get pose information from the camera, we use mediapipe’s computer vision infrastructure, coupled with our own data filtering and math to produce concise metrics describing limb displacements and joint angles. We knew the next step, training our Neural Net model, would require immense amounts of data - and so we settled on training our model to detect and correct Squats for now.

### Challenges we ran into
With no available dataset online, we took it upon ourselves to generate data (shoutout to our families and friends who volunteered to record themselves on a quaint Sunday evening). After collecting hours of labelled videos of people performing Squats in a multitude of correct and incorrect ways, we used each frame of video (at 12fps) as a labeled training example - which got us a training set size of tens of thousands.

We also realised that, at times, some of the mediapipe metrics obtained from the image were noisy and imprecise. So we analytically cut down data to calculate only the relevant limb displacements and joint angles to ensure that we were extracting the best data that mediapipe could give us!

### How we built it
We used Google’s TensorFlow library to create and train our Neural Net by employing algorithms for supervised machine learning. After hours of parameter and hyperparameter tuning, we struck gold! With a training accuracy of 80%, and validation accuracy of 75%, we knew we had proof of concept - and testing using live demos via our webcams only boosted our confidence.

Our real-time algorithm can be broken down into a few steps:
- Get Body Position from live image
- Extract relevant metrics about limb displacements and joint angles from body positions
- Plug in vector of extracted metrics into our Neural Net tensorflow model
- Interpret output vector into textual labels annotated onto display in real time

### Video Demo
Watch [this](https://www.youtube.com/watch?v=eAoDXikzj-A)!

### Accomplishments that we're proud of

What we’re extremely proud of is that we were able to cleverly reduce the space of our problem significantly - from our input being a full image from camera, to our simplified Neural Network input vector being __just 3 angles and 2 limb displacement measures__, that outputs 5 unique and independent labels describing the Squat that we had identified through research. This simplification is what makes our approach modular, and easily adaptable to all kinds of forms and exercises.

### What's next for Posture
Our focus during this Hackathon was limited to perfecting Squats. However, we’re certain that by feeding in the right labeled training data, our pipeline can easily be used for any arbitrary exercise - be it a work-out, yoga, or pilates!

### Built with:
- [x] Tensorflow
- [x] OpenCV
- [x] Mediapipe
- [x] Flask  
- [x] Plotly
- [x] Dash
