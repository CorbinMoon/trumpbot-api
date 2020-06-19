#!/bin/bash
tag="v1.15.0"
echo "deb [arch=amd64] https://storage.googleapis.com/bazel-apt stable jdk1.8" | sudo tee /et
c/apt/sources.list.d/bazel.list
curl https://bazel.build/bazel-release.pub.gpg | sudo apt-key add -
sudo apt-get update && sudo apt-get install bazel
sudo apt-get install --only-upgrade bazel
git clone --branch ${tag} https://github.com/tensorflow/tensorflow --single-branch
chmod +x ./tensorflow/configure
./tensorflow/configure