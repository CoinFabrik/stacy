FROM ubuntu:latest

LABEL maintainer="your-email@example.com"

RUN apt-get update && apt-get install -y \
    git \
    make \
    curl \
    python3 \
    python3.12-venv \
    build-essential \
    npm \
    python3-dev \
    && apt-get clean



RUN git clone --recurse-submodules https://github.com/faculerena/stacy /opt/stacy

WORKDIR /opt/stacy/stacks_analyzer/tree-sitter-clarity
RUN npm install tree-sitter-cli
RUN npx tree-sitter generate
WORKDIR /opt/stacy

ENV INPUT_TARGET="."
ENTRYPOINT ["sh", "-c", "git config --global --add safe.directory /github/workspace && git submodule update --init --recursive && make action"]
