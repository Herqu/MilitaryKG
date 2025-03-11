from typing import List, Optional
from pydantic import BaseModel, Field
from langchain.prompts import ChatPromptTemplate, PromptTemplate, SystemMessagePromptTemplate
from langchain.schema import SystemMessage
from langchain.schema.runnable import RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser
from .entity_node_few_shot_example import few_shot_example_1


# 首先定义实体数据结构模型
class EntityNode(BaseModel):
    entity_type: str = Field(..., description="实体类型，如人物、地点、组织等")
    entity_cn_name: str = Field(..., description="实体标准中文翻译名称")
    entity_raw_name: str = Field(..., description="实体标准原文名称")
    context_cn: str = Field(..., description="实体出现的上下文中文翻译片段")
    context_raw: str = Field(..., description="实体出现的上下文原文片段")

class EntityExtractionOutput(BaseModel):
    entities: List[EntityNode] = Field(..., description="提取的实体列表")

def create_extract_entity_nodes_chain(llm, entity_types=None, few_shot_examples=None):
    """
    创建实体抽取链
    
    参数：
    llm - 语言模型实例
    entity_types - 需要识别的实体类型列表（可选）
    few_shot_examples - 少样本学习示例列表
    """
    
    # 设置默认实体类型
    if entity_types is None:
        entity_types = ["人物", "组织", "地点", "时间", "事件", "专业术语"]
        
    # 设置默认少样本示例
    if few_shot_examples is None:
        few_shot_examples = few_shot_example_1

    # 构建系统提示
    system_template = """你是一个专业的实体抽取助手，需要从文本中准确识别以下类型的实体：{entity_types}。

        任务要求：
        1. 严格识别指定类型的实体，不添加额外类型
        2. 对每个实体提供准确的标准化命名
        3. 包含实体出现的上下文片段
        4. 确保不遗漏任何提及的实体
        5. 对模糊指代需要结合上下文明确具体指代对象

        输出要求：
        - 使用严格JSON格式
        - 实体类型只能使用预定义类型
        - 每个实体至少包含entity_type, entity_cn_name, entity_raw_name, context_cn, context_raw三个字段

        以下是示例参考：
        {few_shot_examples}"""

    # 构建提示模板
    prompt = PromptTemplate(
        template=system_template,
        input_variables=["text"],
        partial_variables={
            "entity_types": ", ".join(entity_types),
            "few_shot_examples": "\n\n".join(few_shot_examples)
        }
    )

    # 构建完整提示
    chat_prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate(prompt=prompt),
        ("user", "待分析文本：\n{text}")
    ])

    # 构建处理链
    chain = (
        {"text": RunnablePassthrough()}  # 直接传递文本输入
        | chat_prompt
        | llm
        | JsonOutputParser(pydantic_object=EntityExtractionOutput)
    )



