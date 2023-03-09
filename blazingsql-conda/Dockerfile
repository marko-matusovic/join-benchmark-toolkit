FROM continuumio/miniconda3:latest

RUN apt update
RUN apt-get update
RUN apt-get install -y git

# RUN conda install Cython==0.29.28 matplotlib numpy pandas plotly scipy setuptools tqdm
# RUN conda install -c intel mkl

RUN conda create -n bsql python=3.7
RUN conda install -n bsql cudatoolkit=11.2 -c nvidia
RUN conda install -n bsql blazingsql -c blazingsql
RUN conda install -n bsql jupyter
RUN conda activate bsql

EXPOSE 9999
CMD ["jupyter notebook --port 9999"]