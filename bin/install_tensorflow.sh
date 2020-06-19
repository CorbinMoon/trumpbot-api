#!/bin/bash
wget https://github.com/bazelbuild/bazel/releases/download/0.24.1/bazel-0.24.1-installer-linux-x86_64.sh
chmod +x bazel-0.24.1-installer-linux-x86_64.sh
./bazel-0.24.1-installer-linux-x86_64.sh
git clone --branch v1.15.0 https://github.com/tensorflow/tensorflow --single-branch
chmod +x ./tensorflow/configure
echo "y y y y y y y" | ./tensorflow/configure