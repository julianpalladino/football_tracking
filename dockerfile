FROM python:3.9

RUN apt-get update

RUN apt-get install ffmpeg libsm6 libxext6 -y

RUN mkdir /app

ADD . /app

WORKDIR /app

RUN pip install -r requirements.txt

# Copy goturn files to the root directory so opencv can use them
RUN cat model_files/goturn.caffemodel.zip.001 model_files/goturn.caffemodel.zip.002 \
    model_files/goturn.caffemodel.zip.003 model_files/goturn.caffemodel.zip.004  > model_files/goturn.caffemodel.zip && \
    unzip model_files/goturn.caffemodel.zip -d .

COPY model_files/goturn.caffemodel /app/goturn.caffemodel

RUN pwd

RUN ls

COPY model_files/goturn.prototxt ./

# Same for DaSiamRPN
COPY model_files/dasiamrpn_kernel_cls1.onnx \
    model_files/dasiamrpn_kernel_r1.onnx \
    model_files/dasiamrpn_model.onnx ./

ENTRYPOINT ["python", "/app/main.py"]