name: Build APK

on:
  push:
    branches: [ main, master ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y \
            python3-pip \
            build-essential \
            git \
            python3-dev \
            ccache \
            bison \
            flex \
            make \
            zip \
            unzip \
            zlib1g-dev \
            openjdk-17-jdk \
            pkg-config \
            autoconf \
            libtool \
            libffi-dev \
            libssl-dev \
            libtool-bin

    - name: Install Buildozer and Cython
      run: |
        pip install --upgrade pip
        pip install cython==0.29.33 buildozer

    - name: Build APK with Buildozer
      run: |
        buildozer -v android debug

    - name: Upload APK
      uses: actions/upload-artifact@v4
      with:
        name: package
        path: bin/*.apk
