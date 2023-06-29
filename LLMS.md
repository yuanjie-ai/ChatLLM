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
