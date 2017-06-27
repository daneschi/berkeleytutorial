FROM ubuntu:16.04

## Base Docker image with dependencies installed to build and run:
##   https://github.com/daneschi/berkeleytutorial
##   https://bitbucket.org/danschi/tuliplib

RUN apt-get update
RUN apt-get install --yes libarmadillo-dev libboost-all-dev swig doxygen python-breathe python-pip mpich cmake
RUN pip install sphinxcontrib-bibtex

ENV APP_DIR /srv/app
ENV PATH ${APP_DIR}/venv/bin:$PATH

RUN apt-get update && \
    apt-get install --yes \
            python \
            python-dev \
            python-pip \
            python3 \
            python3-venv \
            python3-dev \
            build-essential \
            tar \
            git \
            locales && \
    apt-get purge && apt-get clean

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

RUN adduser --disabled-password --gecos "Default Jupyter user" jovyan

RUN mkdir -p ${APP_DIR} && chown -R jovyan:jovyan ${APP_DIR}

WORKDIR /home/jovyan

USER jovyan
RUN python3 -m venv ${APP_DIR}/venv

RUN pip install --no-cache-dir notebook==5.0.0 jupyterhub==0.7.2 ipywidgets==5.2.3 jupyterlab==0.23.2 && \
    jupyter nbextension enable --py widgetsnbextension --sys-prefix && \
    jupyter serverextension enable --py jupyterlab --sys-prefix

# interact notebook extension
RUN pip install git+https://github.com/data-8/nbpuller.git@8142e3c && \
	jupyter serverextension enable --sys-prefix --py nbpuller && \
	jupyter nbextension install --sys-prefix --py nbpuller && \
	jupyter nbextension enable --sys-prefix --py nbpuller

ADD requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

EXPOSE 8888
USER jovyan
