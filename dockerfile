FROM python:3.9

RUN apt-get update

RUN apt-get install ffmpeg libsm6 libxext6 -y

RUN pip install opencv-python==4.5.5.62\
    && pip install opencv-contrib-python==4.5.5.62 \
    && pip install opencv-contrib-python-headless==4.5.5.62 \
    && pip install ffmpeg \
    && pip install tqdm \
    && pip install pytest \
    && pip install sklearn \
    && pip install -U scikit-image==0.17.2 
