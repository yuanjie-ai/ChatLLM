# Chatgpt*
> 计划推出国内 oneapi，支持各种主流大模型，兼容openai客户端生态。

```python
import os

os.environ['OPEN_API_KEY'] = "sk-..."
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI()
c = LLMChain(llm=llm, prompt=ChatPromptTemplate.from_template("{question}"))
print(c.run('你是谁'))
```
# [腾讯混元](https://hunyuan.tencent.com)
```python
import os

os.environ['HUNYUAN_API_KEY'] = "appid:secret_id:secret_key"
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from chatllm.llmchain.llms import HuanYuan

llm = HuanYuan()
c = LLMChain(llm=llm, prompt=ChatPromptTemplate.from_template("{question}"))
print(c.run('你是谁'))
# 您好！我是腾讯混元大模型，由腾讯公司研发的大型语言模型。我具备丰富的专业领域知识，强大的语义理解能力和逻辑思维能力。我的目标是帮助用户解决问题、提供有用的信息和建议，涵盖文本创作、工作计划、数学计算和聊天对话等领域。若您需要任何帮助，请告诉我，我将尽力满足您的需求。
```

# Chatglm

```python
import os

os.environ['CHATGLM_API_KEY'] = "apikey"
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from chatllm.llmchain.llms import ChatGLM

llm = ChatGLM()
c = LLMChain(llm=llm, prompt=ChatPromptTemplate.from_template("{question}"))
print(c.run('你是谁'))
```


# LLAMA*【适配中。。。】

```python
from meutils.pipe import *
from chatllm.applications import ChatBase

qa = ChatBase()
qa.load_llm(model_name_or_path="LLAMA")
for i in qa(query='数据治理简约流程'):
    print(i, end='')
```

# 百度文心

```python
import os
os.environ['ERNIE_API_KEY'] = "apikey:apisecret"
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from chatllm.llmchain.llms import ErnieBot

llm = ErnieBot()
c = LLMChain(llm=llm, prompt=ChatPromptTemplate.from_template("{question}"))
print(c.run('你是谁'))
```

# 讯飞星火

```python
import os
os.environ['SPARK_API_KEY'] = "appid:apikey:apisecret"
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from chatllm.llmchain.llms import SparkBot

llm = SparkBot()
c = LLMChain(llm=llm, prompt=ChatPromptTemplate.from_template("{question}"))
print(c.run('你是谁'))

```
