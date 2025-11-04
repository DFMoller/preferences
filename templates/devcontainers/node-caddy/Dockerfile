#
# VSCode devcontainer for development with: Node + Caddy
#
ARG NODE_VERSION=22.6

FROM node:$NODE_VERSION
# FROM creates a new build stage, so we need to redeclare any arguments we want to keep
# see: https://docs.docker.com/engine/reference/builder/#understand-how-arg-and-from-interact

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
RUN unset DISPLAY
ENV DEBIAN_FRONTEND=noninteractive

########
# Install general dependencies
########

# note that we don't clear out the APT-GET cache -- one often needs to install
# packages inside the devcontainer.
RUN apt-get update && apt-get -y upgrade && apt-get -qqy install \
  apt-transport-https \
  iputils-ping \
  sudo \
  gnupg2 \
  tzdata

# Install claude code globally.
RUN sudo npm install -g @anthropic-ai/claude-code

########
# Install project-specific dependencies
########

RUN apt-get -qqy install caddy

########
# Setup user
########

# Ensure default `node` user has access to `sudo`
ARG USERNAME=node
RUN echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# default command to run if nothing else is specified
CMD ["/bin/bash"]
