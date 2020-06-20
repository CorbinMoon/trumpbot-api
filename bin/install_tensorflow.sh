#!/bin/bash

#bazel installation
wget https://github.com/bazelbuild/bazel/releases/download/3.1.0/bazel-3.1.0-installer-linux-x86_64.sh
chmod +x bazel-3.1.0-installer-linux-x86_64.sh
./bazel-3.1.0-installer-linux-x86_64.sh

# get tensorflow sources
git clone https://github.com/tensorflow/tensorflow.git
cd tensorflow

# build from source
chmod +x ./configure
./configure
bazel build --config=opt //tensorflow/tools/pip_package:build_pip_package
./bazel-bin/tensorflow/tools/pip_package/build_pip_package /tmp/tensorflow_pkg
pip install /tmp/tensorflow_pkg/tensorflow-version-tags.whl
cd ..