# FROM continuumio/miniconda3:latest
FROM continuumio/miniconda3:master

SHELL ["bash", "-lc"]

RUN apt update
RUN apt-get update
RUN apt-get install -y git

RUN conda init bash
RUN conda update conda
# RUN conda config --set channel_priority strict

RUN conda create -n heavyai -c rapidsai -c nvidia -c conda-forge -c defaults python cudf cudatoolkit heavyai

# RUN conda install Cython==0.29.28 matplotlib numpy pandas plotly scipy setuptools tqdm
# RUN conda install -c intel mkl

RUN conda activate heavyai
RUN pip install pyheavydb
