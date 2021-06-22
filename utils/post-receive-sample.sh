#!/bin/bash
# conserva ese script como ejemplo para replicar en otros
# proyectos con hooks de git bare
echo "post receive desde servidor con operation-patch-request.git"
deployDir="../deploy"
TEMP="/home/admin/operation-patch-request"
GIT_DIR="/home/admin/operation-patch-request.git"
echo "ejecutando comando ls"
ls
echo "-------------------------"
while read oldrev newrev ref
do
    branch="main"
    if [ "$ref" == "refs/heads/main" ]; then
        mkdir $TEMP
        git --work-tree=$TEMP --git-dir=$GIT_DIR checkout -f main
        cd $TEMP
    fi
done