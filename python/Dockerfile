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

# With version to make build faster
RUN conda install -c rapidsai -c conda-forge -c nvidia -c intel \
    python=3.10.11 \
    cudf=23.04.01 \
    cudatoolkit=11.8.0 \
    Cython=0.29.33 \
    matplotlib=3.7.1 \
    numpy=1.23.5 \
    pandas=1.5.3 \
    plotly=5.9.0 \
    scipy=1.10.0 \
    setuptools=65.6.3 \
    tqdm=4.65.0 \
    sqlparse=0.4.3 \
    mkl=2021.4.0

# # NVIDIA Nsight Systems 2020.2.1
# # from this guide
# # https://developer.nvidia.com/blog/nvidia-nsight-systems-containers-cloud/
# RUN apt-get update -y && \
#     DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
#         apt-transport-https \
#         ca-certificates \
#         gnupg \
#         wget && \
#     rm -rf /var/lib/apt/lists/*
# RUN wget -qO - https://developer.download.nvidia.com/devtools/repos/ubuntu2004/amd64/nvidia.pub | apt-key add - && \
#     echo "deb https://developer.download.nvidia.com/devtools/repos/ubuntu2004/amd64/ /" >> /etc/apt/sources.list.d/nsight.list && \
#     apt-get update -y && \
#     DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
#         nsight-systems-2020.2.1 && \
#     rm -rf /var/lib/apt/lists/* 

# Nsight Compute 
# from guide
# https://developer.nvidia.com/blog/using-nsight-compute-in-containers/
RUN apt-get update -y && \
     DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
         apt-transport-https \
         ca-certificates \
         gnupg \
         wget && \
     rm -rf /var/lib/apt/lists/*
RUN  echo "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64 /" > /etc/apt/sources.list.d/cuda.list && \
     wget -qO - https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub | apt-key add - && \
         apt-get update -y && \
     DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
         nsight-compute-2020.1.0 && \
     rm -rf /var/lib/apt/lists/*

RUN apt update
RUN apt install bc

# # Keeps Python from generating .pyc files in the container
# ENV PYTHONDONTWRITEBYTECODE=1

# # Turns off buffering for easier container logging
# ENV PYTHONUNBUFFERED=1

# WORKDIR /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
# RUN adduser -u 5678 --disabled-password --gecos "" appuser && chmod -R  appuser /app
# USER appuser
