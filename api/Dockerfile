FROM tensorflow/tensorflow:2.10.0

# install python 3
RUN apt-get update \
    && apt-get install -y python3 python3-pip ffmpeg libsm6 libxext6 \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 5000

RUN pip install --upgrade pip setuptools wheel

WORKDIR /api

ADD requirements_docker.txt /api/requirements_docker.txt
RUN pip --no-cache-dir install -r requirements_docker.txt

## Install the dataset and download the model
ADD src/install/install_dataset.py /api/src/install/install_dataset.py
RUN python3 src/install/install_dataset.py

# Usually you should hide this in a .env file
# But here for the sake of the demo we will leave it here
ENV MODEL_URL=https://drive.google.com/uc?id=1tIPCklNqihzPTR4OrnACPDQRBu3Eb9zJ
ADD src/install/install_model.py /api/src/install/install_model.py
RUN python3 src/install/install_model.py

RUN pip install pyyaml h5py

## Run the app

COPY . ./

ENTRYPOINT ["python3", "-m", "src.app"]