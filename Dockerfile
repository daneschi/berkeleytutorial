FROM ubuntu:16.04

MAINTAINER Aaron Culich / Berkeley Research Computing <brc+aculich@berkeley.edu>

## Please feel free to contact Berkeley Research Computing (BRC) if you have
## questions or if you want dedicated computational infrastructure if
## http://beta.mybinder.org/ does not provide enough power or if you need a
## dedicated resource for your own research or workshop.
##
## - http://research-it.berkeley.edu/brc
## - http://research-it.berkeley.edu/services/cloud-computing-support
##
## Contact: Aaron Culich <brc+aculich@berkeley.edu>


## Jupyter notebook setup derived from:
##   https://github.com/data-8/singleuser-data8/blob/master/Dockerfile

ENV APP_DIR /srv/app
ENV PATH ${APP_DIR}/venv/bin:$PATH

RUN apt-get update && \
    apt-get install --yes \
            python \
            python-dev \
            python-pip \
            python-wheel \
            python3 \
            python3-venv \
            python3-dev \
            python3-wheel \
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


## Base Docker image with dependencies customized to build and run:
##   https://github.com/daneschi/berkeleytutorial
##   https://bitbucket.org/danschi/tuliplib

USER root

RUN apt-get update && \
    apt-get install --yes \
            libarmadillo-dev \
            libboost-all-dev \
            swig \
            doxygen \
            python-breathe \
            python-pip \
            python-wheel \
            mpich \
            cmake \
            cmake-curses-gui \
            && \
    apt-get purge && apt-get clean

RUN pip install sphinxcontrib-bibtex

## Note: Because tuliplib is currently (as of June 2017) a private repo it is
## built separately and the binaries have been checked into this git repo as
## of this commit hash: https://bitbucket.org/danschi/tuliplib/src/de4686a
##
##     cd tutorial/
##     git clone https://bitbucket.org/danschi/tuliplib/src/de4686a
##     mkdir tulipBin ; cd tulipBin ; ccmke ../tuliplib

USER jovyan
