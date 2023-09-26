#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : prompt_templates
# @Time         : 2023/8/6 15:41
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate

context_prompt_template = """
根据提供的信息，以简洁、专业的方式回答用户的问题。如果无法提供答案，请回复：“根据提供的信息无法回答该问题”或“没有提供足够的信息”。请不要编造信息，答案必须使用中文。

已知信息：
```
{context}
```

问题：
{question}

让我们逐步思考并给出答案：
""".strip()  # Let's think step by step

summary_prompt_template = """
请你充当“文本摘要模型”，要求：
1. 能够从文本中提取关键信息，抓住内容本质。
2. 生成准确、没有个人意见或偏见的公正连贯的摘要。
3. 在生成的摘要中尽量减少重复和冗余，在保留基本信息的同时保持可读性与连贯性。

输入文本：{text}
Let's think step by step, 根据输入文本生成一个清晰简洁的摘要：
""".strip()

question_generation_prompt_template = """
请扮演一个“问题生成模型”，要求：
1. 理解语义上下文、预测用户意图、生成清晰、有针对性的问题
2. 从给定的信息或文本中提取关键信息，理解语境，然后根据需要产生有启发性和相关性的问题。
3. 你的目标是产生与输入文本相关且有用的问题，以帮助用户进一步思考和探索。

输入文本：{text}
Let's think step by step, 根据输入文本生成最相关的5个问题：
""".strip()

"""
请扮演阅读理解模型。
1. 描述角色的特征：应具有良好的理解能力、快速而准确地分析和回答问题的能力，同时保持客观并有效地提供相关信息。
2. 必备技能：熟练掌握阅读和语言理解技巧，具备广泛的知识储备和信息检索能力，能够理解不同类型的文本并提供准确的答案。
3. 典型活动示例：阅读和理解文章、故事、新闻报道、指南和其他各种文本形式，从中提取关键信息，回答相关问题，并进行综合分析和总结。
4. 目标设定：提供准确、全面且有意义的回答，为用户提供最佳的阅读理解经验，帮助他们更好地理解和拓展知识。
5. 合理且清晰简洁的提示，使用明确的语言描述要求。

请马上以阅读理解模型的身份开始。
""".strip()

# https://mp.weixin.qq.com/s/rtdTnlrZHuHjB1paUNTssQ
system_template = """
你将会得到一个由三个引号分隔的文档内容和一个问题，请使用三个引号内的内容，简洁、专业地回答用户的问题。
如果无法得到答案，请回复：“根据已知信息无法回答该问题”或“没有提供足够的信息”。请勿编造信息，答案必须使用中文。
""".strip()

messages = [
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template('"""{context}"""\n问题：{question}'),
]
CHAT_CONTEXT_PROMPT = ChatPromptTemplate.from_messages(messages)

system_template = """
你将会得到一个由三个引号分隔的文档内容和一个问题。
你的任务是只使用提供的文档内容来回答问题，并引用“用于回答问题的文档内容段落”。
如果文档内容中没有包含用于回答该问题所需的信息，则简单地返回：“信息不足”。
如果文档内容中提供了问题的答案，则必须使用“引文”进行注释。使用以下格式引用相关的段落。("引文": …)
""".strip()

messages = [
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template('"""{context}"""\n问题：{question}'),
]
CHAT_CONTEXT_PROMPT_WITH_SOURCE = ChatPromptTemplate.from_messages(messages)

if __name__ == '__main__':
    from meutils.pipe import *
    from langchain.chat_models import ChatOpenAI
    from langchain.chains import LLMChain

    llm = ChatOpenAI()
    prompt = CHAT_CONTEXT_PROMPT_WITH_SOURCE

    context = """
2022年的某一天，李明开着摩托车去给客户送货，路上遇到了一只小狗，他停下车去看了一下小狗，回去开车的时候货物不见了。李明在2023年进了一批货物，货物里面居然有一只小狗。
    """

    c = LLMChain(llm=llm, prompt=prompt)
    print(c.run(context=context, question="2022年李明开摩托车遇到了什么动物？"))
