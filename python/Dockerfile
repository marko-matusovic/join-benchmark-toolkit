FROM continuumio/miniconda3:master

SHELL ["bash", "-lc"]

RUN apt update
RUN apt-get update
RUN apt-get install -y git

RUN conda init bash
RUN conda update conda
# RUN conda config --set channel_priority strict

RUN conda create -n env

# RUN conda install Cython==0.29.28 matplotlib numpy pandas plotly scipy setuptools tqdm
# RUN conda install -c intel mkl

RUN conda activate env
RUN pip install numpy
RUN pip install pandas

# NVIDIA Nsight Systems 2020.2.1
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        apt-transport-https \
        ca-certificates \
        gnupg \
        wget && \
    rm -rf /var/lib/apt/lists/*
RUN wget -qO - https://developer.download.nvidia.com/devtools/repos/ubuntu2004/amd64/nvidia.pub | apt-key add - && \
    echo "deb https://developer.download.nvidia.com/devtools/repos/ubuntu2004/amd64/ /" >> /etc/apt/sources.list.d/nsight.list && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        nsight-systems-2020.2.1 && \
    rm -rf /var/lib/apt/lists/* 

# from this guide
# https://developer.nvidia.com/blog/nvidia-nsight-systems-containers-cloud/

# RUN WITH
# docker build -t mm_python_img .