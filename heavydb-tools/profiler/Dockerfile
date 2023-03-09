FROM heavyai/core-os-cuda:v6.4.0

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
