#!/bin/bash
tag="v1.15.0"
wget https://github.com/bazelbuild/bazel/releases/download/0.22.0/bazel-0.22.0-installer-linux-x86_64.sh
chmod u+x bazel-0.22.0-installer-linux-x86_64.sh
sudo ./bazel-0.22.0-installer-linux-x86_64.sh --user
git clone --branch ${tag} https://github.com/tensorflow/tensorflow --single-branch
chmod +x ./tensorflow/configure
./tensorflow/configure