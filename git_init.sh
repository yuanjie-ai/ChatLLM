#!/usr/bin/env bash

#git init
# shellcheck disable=SC2035
git add *
#git commit -m "[feat] add ChatWhoosh"
git commit -m "add: 兼容openai客户端"

#git remote add origin git@github.com:yuanjie-ai/llm4gpt.git
#git branch -M master

git pull
git push -u origin master -f

# git remote remove origin
