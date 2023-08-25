#!/usr/bin/env bash
# @Project      : MeUtils
# @Time         : 2022/4/27 下午1:35
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : ${DESCRIPTION}

#1.切换到新的分支
git checkout --orphan latest_branch

#2.缓存所有文件（除了.gitignore中声明排除的）
git add -A

#3.提交跟踪过的文件（Commit the changes）
git commit -am "init"

#4.删除master分支（Delete the branch）
git branch -D master

#5.重命名当前分支为master（Rename the current branch to master）
git branch -m master

#6.提交到远程master分支 （Finally, force update your repository）
git push -f origin master
