#!/bin/bash

__GIT_BRANCH=`git symbolic-ref --short HEAD`

if [ "$__GIT_BRANCH" == "master" ]; then
    __GIT_BRANCH="latest"
fi
echo "current branch: ${__GIT_BRANCH}"

__SERVICE_NAME=`grep "SERVICE_NAME" settings.py | awk -F "=" '{print $2}' | xargs echo`
__SERVICE_PORT=`grep "SERVICE_PORT" settings.py | awk -F "=" '{print $2}' | xargs echo`
__RUN_NAME=${__SERVICE_NAME}_${__SERVICE_PORT}

docker stop $__RUN_NAME
docker rm -v $__RUN_NAME

__NET_MODE="host"
__PLATFORM=`uname`
if [ "$__PLATFORM" == "Darwin" ]; then
	__NET_MODE="bridge"
fi

docker run -d --rm \
--name=$__RUN_NAME \
--net=$__NET_MODE \
-p $__SERVICE_PORT:$__SERVICE_PORT \
--env _SERVICE_PORT=$__SERVICE_PORT \
--env _SERVICE_MODE=deploy \
--env _ENABLE_API_SERVICE_CONSOLE=1 \
--env _DB_HOST=db.local.com \
--env _DB_NAME=iscrum \
--env _DB_PORT=3306 \
--env _DB_USER=iscrum \
--env _DB_PASSWORD=test \
--env _DB_CHARSET=utf8mb4 \
--env _API_GATEWAY=api.local.com \
--add-host db.local.com:127.0.0.1 \
registry.cn-hangzhou.aliyuncs.com/aix/${__SERVICE_NAME}:$__GIT_BRANCH
