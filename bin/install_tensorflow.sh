#!/bin/bash

#bazel installation
wget https://github.com/bazelbuild/bazel/releases/download/0.24.1/bazel-0.24.1-installer-linux-x86_64.sh
chmod +x bazel-0.24.1-installer-linux-x86_64.sh && ./bazel-0.24.1-installer-linux-x86_64.sh

# get tensorflow sources
git clone https://github.com/tensorflow/tensorflow.git && cd tensorflow
git checkout r1.14

# build from source
chmod +x ./configure && ./configure
bazel build --config=v1 //tensorflow/tools/pip_package:build_pip_package
./bazel-bin/tensorflow/tools/pip_package/build_pip_package /tmp/tensorflow_pkg
pip install /tmp/tensorflow_pkg/tensorflow-version-tags.whl
cd ..