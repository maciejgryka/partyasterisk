FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

# install system dependencies
RUN apt-get update && apt-get install -y \
#     awscli \
    curl \
    build-essential \
#     ffmpeg \
    git \
#     golang \
    libbz2-dev \
#     libjpeg-turbo8-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libffi-dev \
    liblzma-dev \
    libreadline-dev \
    libsqlite3-dev \
#     libsm6 \
    libssl-dev \
#     libxext6 \
#     libxrender-dev \
    llvm \
    make \
    python-openssl \
#     python3 \
#     python3-pip \
    python3-dev \
    tk-dev \
    wget \
    xz-utils \
    zlib1g-dev \
    && apt-get clean

# set up the app
RUN mkdir /app
WORKDIR /app
RUN chmod -R 777 /app

# set up the user
RUN useradd -m partyuser
USER partyuser

# install pyenv
RUN git clone git://github.com/pyenv/pyenv.git ~/.pyenv
ENV HOME /home/partyuser
ENV PYENV_ROOT $HOME/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH
# build optimized python
ENV CFLAGS -O2
# make sure pyenv python can use python3-dev
ENV PYTHON_CONFIGURE_OPTS --enable-shared

RUN pyenv install 3.7.1
RUN pyenv global 3.7.1
RUN pyenv rehash

# install python deps
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN pip install -U pip pipenv setuptools
RUN pipenv install --system --deploy
RUN pyenv rehash

ADD . /app

EXPOSE 5000
CMD ["gunicorn", "partyasterisk:app"]
# CMD bash
