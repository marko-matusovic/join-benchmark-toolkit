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
