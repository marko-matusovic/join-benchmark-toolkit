FROM nvidia/cuda:11.8.0-devel-ubuntu20.04

# Install base utilities
RUN apt-get update && \
    apt-get install -y wget && \
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install miniconda
ENV CONDA_DIR /opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
     /bin/bash ~/miniconda.sh -b -p /opt/conda

# Put conda in path so we can use conda activate
ENV PATH=$CONDA_DIR/bin:$PATH

RUN conda init bash
RUN conda update conda
# RUN conda config --set channel_priority strict

RUN conda install Cython matplotlib numpy pandas plotly scipy setuptools tqdm
RUN conda install -c intel mkl

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