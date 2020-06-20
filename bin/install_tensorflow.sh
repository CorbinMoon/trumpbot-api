#!/bin/bash
tag="v1.15.0"
wget https://github.com/bazelbuild/bazel/releases/download/0.24.1/bazel-0.24.1-installer-linux-x86_64.sh
chmod +x bazel-0.24.1-installer-linux-x86_64.sh
./bazel-0.24.1-installer-linux-x86_64.sh
git clone --branch ${tag} https://github.com/tensorflow/tensorflow --single-branch
chmod +x ./tensorflow/configure
./tensorflow/configure
bazel build --config=v1 //tensorflow/tools/pip_package:build_pip_package
./bazel-bin/tensorflow/tools/pip_package/build_pip_package /tmp/tensorflow_pkg
pip install /tmp/tensorflow_pkg/tensorflow-version-tags.whl