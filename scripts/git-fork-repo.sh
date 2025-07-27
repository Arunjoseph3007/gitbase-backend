#!/bin/bash

# Script for forking a bare git repo 

GIT_DIR="/var/www/git"
OLD_REPO_USER=$1
OLD_REPO_NAME=$2
NEW_REPO_USER=$3
NEW_REPO_NAME=$4

OLD_REPO="${GIT_DIR}/${OLD_REPO_USER}/${OLD_REPO_NAME}.git"
NEW_REPO="${GIT_DIR}/${NEW_REPO_USER}/${NEW_REPO_NAME}.git"

mkdir -p "${NEW_REPO}"
cd "${NEW_REPO}"

git clone --bare "${OLD_REPO}" . &> /dev/null
touch git-daemon-export-ok
cp hooks/post-update.sample hooks/post-update
git config http.receivepack true
git update-server-info
git config --global --add safe.directory "${NEW_REPO}"
chown -Rf www-data:www-data "${NEW_REPO}"
echo "Git repository '${OLD_REPO}' forked into ${NEW_REPO}"