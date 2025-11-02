#
# VSCode devcontainer for development with: Ubuntu + Python + Poetry
#
ARG UBUNTU_VERSION=24.04
ARG PYTHON_VERSION=3.11
ARG POETRY_VERSION=1.8.3

FROM ubuntu:$UBUNTU_VERSION
# FROM creates a new build stage, so we need to redeclare any arguments we want to keep
# see: https://docs.docker.com/engine/reference/builder/#understand-how-arg-and-from-interact
ARG PYTHON_VERSION
ARG POETRY_VERSION

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
RUN unset DISPLAY
ENV DEBIAN_FRONTEND=noninteractive

# ----------------------------------------------------------------------------------------------------
# Install python
# ----------------------------------------------------------------------------------------------------

# switch to automatic mirror select mode, makes building much faster down here
RUN sed -i 's http://archive.ubuntu.com/ubuntu/ mirror://mirrors.ubuntu.com/mirrors.txt ' /etc/apt/sources.list

RUN echo python${PYTHON_VERSION}

# install build dependencies
# this will bloat the image, but is necessary to "poetry install" the dependencies
# then install specific Python version
RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
 && apt-get install -y curl software-properties-common git \
 && add-apt-repository ppa:deadsnakes/ppa && apt-get install -y python${PYTHON_VERSION} python${PYTHON_VERSION}-venv python${PYTHON_VERSION}-dev python3-dev
RUN python${PYTHON_VERSION} -m venv /opt/venv
# Make sure we use the virtualenv
ENV PATH="/opt/venv/bin:$PATH"

# ----------------------------------------------------------------------------------------------------
# Install pip
# ----------------------------------------------------------------------------------------------------

# install latest pip
RUN /opt/venv/bin/python${PYTHON_VERSION} -m pip install --upgrade pip

# note that we don't clear out the APT-GET cache -- one often needs to install
# packages inside the devcontainer.
RUN apt-get update && apt-get -qqy install apt-transport-https iputils-ping sudo gnupg2 tzdata

# ----------------------------------------------------------------------------------------------------
# Setup devcontainer user.
# ----------------------------------------------------------------------------------------------------

# It is important that the devcontainer user has the same uid as the user on the host machine. If your
# user on the host machine has a different uid, you should ensure that the devcontainer user also has
# that id. This implementation assumes your user has id 1000. Devcontainer images before ubuntu 24.04
# can use any user since it the user created here will be assigned uid 1000. However, since ubuntu
# 24.04, the image has a default user called "ubuntu" with uid 1000 and the user you set for the
# devcontainer should be that user, "ubuntu".

# If you need to create a user, uncomment this line.
# -m: create home
# -s: set shell
# -G sudo: add to sudo group
# RUN useradd -ms /bin/bash -G sudo vscode

# Ensure that the whole sudo group does not need to supply password when sudoing.
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# Set the user to ubuntu, which is the default user in Ubuntu 24.04 and onwards.
USER ubuntu

# In-case base image sets this to root, we have to reset to ubuntu's home (USER statement not
# sufficient)
ENV HOME=/home/ubuntu

# Pre-create the pypoetry cache directory by the non-root user so that the named-volume we mount
# there will be writable to ubuntu.
RUN mkdir -p ~/.cache/pypoetry/

# ----------------------------------------------------------------------------------------------------
# Install poetry
# ----------------------------------------------------------------------------------------------------

# this is the canonical new location, used to be raw.githubusercontent.com
# install for user ubuntu in ~/.local/bin
RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=${POETRY_VERSION} python${PYTHON_VERSION} -

# ----------------------------------------------------------------------------------------------------
# Setups for specific dependencies
# ----------------------------------------------------------------------------------------------------

RUN sudo apt-get update && sudo apt-get install -y \
    # Requirement for cv2.
    ffmpeg libsm6 libxext6 \
    # Requirement for calibration tool GUI.
    python3.11-tk \
    nodejs \
    npm

# Install Claude Code globally so it can be used in the devcontainer.
RUN sudo npm install -g @anthropic-ai/claude-code

# Default command to run if nothing else is specified.
CMD ["/bin/bash"]
