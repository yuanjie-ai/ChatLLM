# Chatgpt*

```python
from meutils.pipe import *
from chatllm.applications import ChatBase

os.environ['API_KEY'] = 'sk-...'

qa = ChatBase()
qa.load_llm(model_name_or_path="chatgpt")
for i in qa(query='数据治理简约流程'):
    print(i, end='')
```

# Chatglm*

```python
from meutils.pipe import *
from chatllm.applications import ChatBase

qa = ChatBase()
qa.load_llm(model_name_or_path="THUDM/chatglm2-6b")
for i in qa(query='数据治理简约流程'):
    print(i, end='')
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
