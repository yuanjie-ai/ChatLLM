#!/usr/bin/env bash

#git init
# shellcheck disable=SC2035
git add *
#git commit -m "add: 支持chatbox客户端"
#git commit -m "fix: pandas2.0 `df.drop` bug"
git commit -m "add:  ChatMind"

#git remote add origin git@github.com:yuanjie-ai/llm4gpt.git
#git branch -M master

git pull
git push -u origin master -f

# git remote remove origin
