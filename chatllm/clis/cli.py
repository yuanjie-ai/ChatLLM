#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : __init__.py
# @Time         : 2021/1/31 10:20 下午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *

cli = typer.Typer(name="ChatLLM CLI")

if LOCAL_HOST.startswith('10.219'):
    MODEL_PATH = "/CHAT_MODEL/chatglm-6b"


def f(a=1, **kw):
    print(a)
    print(kw)


@cli.command(help="help")  # help会覆盖docstring
def clitest(**kwargs):  # 不支持 **kwargs
    f(**kwargs)


@cli.command()  # help会覆盖docstring
def webui(name: str = 'chatpdf', port=8501):
    """
        chatllm-run webui --name chatpdf --port 8501
    """
    main = get_resolve_path(f'../webui/{name}.py', __file__)
    os.system(f'streamlit run {main} --server.port {port}')


@cli.command()  # help会覆盖docstring
def openapi(llm_model, host='127.0.0.1', port: int = 8000, debug='1'):
    """
        chatllm-run openapi <MODEL_PATH> --host 127.0.0.1 --port 8000
    """

    os.environ['LLM_MODEL'] = llm_model
    os.environ['DEBUG'] = debug

    from meutils.serving.fastapi import App
    from chatllm.api.routes.api import router

    app = App()
    app.include_router(router)
    app.run(host=host, port=port)


if __name__ == '__main__':
    cli()
