#!/bin/bash

GIT_BRANCH=`git symbolic-ref --short HEAD`

if [ "$GIT_BRANCH" == "master" ]; then
    GIT_BRANCH="latest"
fi
echo "current branch: ${GIT_BRANCH}"

docker build . -t registry.cn-hangzhou.aliyuncs.com/aix/iscrum:${GIT_BRANCH} \
    --no-cache --rm