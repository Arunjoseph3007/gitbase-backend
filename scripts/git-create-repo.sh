#!/bin/bash

# Script for creating a new bare git repo 

GIT_DIR="/var/www/git"
REPO_NAME=$1
USER_NAME=$2

mkdir -p "${GIT_DIR}/${USER_NAME}/${REPO_NAME}.git"
cd "${GIT_DIR}/${USER_NAME}/${REPO_NAME}.git"

git init --shared --bare &> /dev/null
touch git-daemon-export-ok
cp hooks/post-update.sample hooks/post-update
git config http.receivepack true
git update-server-info
git config --global --add safe.directory "${GIT_DIR}/${USER_NAME}/${REPO_NAME}.git"
chown -Rf www-data:www-data "${GIT_DIR}/${USER_NAME}/${REPO_NAME}.git"
echo "Git repository '${REPO_NAME}' created in ${GIT_DIR}/${USER_NAME}/${REPO_NAME}.git"