#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : 格式化
# @Time         : 2023/9/4 17:09
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
# 解析输出并获取结构化的数据
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.chat_models import ChatOpenAI

response_schemas = [
    ResponseSchema(name="artist", description="The name of the musical artist"),
    ResponseSchema(name="song", description="The name of the song that the artist plays")
]

# 解析器将会把LLM的输出使用我定义的schema进行解析并返回期待的结构数据给我
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)  # output_parser
format_instructions = output_parser.get_format_instructions()

# 这个 Prompt 与之前我们构建 Chat Model 时 Prompt 不同
# 这个 Prompt 是一个 ChatPromptTemplate，它会自动将我们的输出转化为 python 对象
prompt = ChatPromptTemplate(
    messages=[
        HumanMessagePromptTemplate.from_template(
            "Given a command from the user, extract the artist and song names \n \
                                                    {format_instructions}\n{user_prompt}")
    ],
    input_variables=["user_prompt"],
    partial_variables={"format_instructions": format_instructions}
)

artist_query = prompt.format_prompt(user_prompt="I really like So Young by Portugal. The Man")
print(artist_query.messages[0].content)

llm = ChatOpenAI(temperature=0)
artist_output = llm(artist_query.to_messages())
output = output_parser.parse(artist_output.content)
# artist_output = llm.predict(artist_query.to_string())
# output = output_parser.parse(artist_output)

print(output)
print(type(output))
# 这里要注意的是，因为我们


