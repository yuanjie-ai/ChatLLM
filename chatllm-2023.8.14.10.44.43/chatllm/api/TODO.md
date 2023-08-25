在 FastAPI 中，BackgroundTasks 是用来在后台异步执行任务的工具。当你调用 BackgroundTasks 的 add_task
方法添加任务时，它会在后台异步执行这些任务。这些任务会在当前请求处理完成之后执行。

- 增加异步写入数据库
