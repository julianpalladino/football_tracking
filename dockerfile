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

ADD . /app

# Copy goturn files to the root directory so opencv can use them
COPY ./goturn.prototxt goturn.caffemodel /
COPY ./goturn-files /goturn-files

# Same for DaSiamRPN
COPY dasiamrpn_kernel_cls1.onnx dasiamrpn_kernel_r1.onnx dasiamrpn_model.onnx /


ENTRYPOINT ["python", "/app/main.py"]
