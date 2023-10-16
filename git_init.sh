#!/usr/bin/env bash

git init
# shellcheck disable=SC2035
git add *
git rm -r chatllm-202*
#git commit -m "add: 支持chatbox客户端"
#git commit -m "fix: pandas2.0 `df.drop` bug"
git commit -m "add: chatgpt api分发站点"

#git remote add origin git@github.com:yuanjie-ai/llm4gpt.git
#git branch -M master

git pull
git push -u origin master -f
