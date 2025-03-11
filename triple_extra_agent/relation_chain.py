from typing import List, Optional, Sequence
from enum import Enum
from pydantic import BaseModel, Field
from langchain.prompts import ChatPromptTemplate, PromptTemplate, SystemMessagePromptTemplate
from langchain.schema import SystemMessage
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import Runnable
from .relation_few_shot_example import few_shot_example_1

class EntityType(str, Enum):
    PERSON = "人物"
    ORGANIZATION = "组织"
    LOCATION = "地点"
    EVENT = "事件"
    OTHER = "其他"

class EntityNode(BaseModel):
    entity_type: EntityType = Field(..., description="实体类型")
    entity_cn_name: str = Field(..., description="实体中文名称")
    entity_raw_name: str = Field(..., description="实体原始名称")
    entity_context_cn: str = Field(..., description="实体出现的上下文中文翻译片段")
    entity_context_raw: str = Field(..., description="实体出现的上下文原文片段")
    

class RelationNode(BaseModel):
    relation_type: str = Field(..., description="关系主类型，如'相关人物','相关事件'等")
    relation_subtype: str = Field(..., description="关系子类型，如'发起人','影响人'等")
    head_entity: EntityNode = Field(..., description="关系头实体")
    tail_entity: EntityNode = Field(..., description="关系尾实体")
    relation_context_cn: str = Field(..., description="关系出现的上下文中文翻译片段")
    relation_context_raw: str = Field(..., description="关系出现的上下文原文片段")
    confidence: float = Field(..., ge=0, le=1, description="关系置信度")

class RelationExtractionOutput(BaseModel):
    relations: List[RelationNode] = Field(..., description="提取的关系列表")

def create_extract_entity_relation_chain(
    llm, 
    relation_types: Optional[List[str]] = None,
    few_shot_examples: Optional[List[str]] = None
) -> Runnable:
    """
    创建实体关系抽取链
    
    参数：
    llm - 语言模型实例
    relation_types - 需要识别的关系类型列表（可选）
    few_shot_examples - 少样本学习示例列表（原始字符串列表）
    """
    
    # 设置默认关系类型
    if relation_types is None:
        relation_types = [
            # 基础通用类型（保留原有核心关系）
            "相关地点"
            "相关人物或组织"
            "相关事件"
        ]
        
    # 设置默认少样本示例
    if few_shot_examples is None:
        few_shot_examples = [few_shot_example_1]

    # 预处理示例数据
    processed_examples = [
        f"""```json
        {example}
        ```"""
        for example in few_shot_examples
    ]

    # 构建系统提示
    system_template = """你是一个专业的关系抽取助手，需要从文本中准确识别以下类型的关系：
    
    可用关系类型（格式：主类型::子类型）：
    {relation_types}

    任务要求：
    1. 严格识别指定类型的关系，不添加额外类型
    2. 每个关系必须包含明确的主实体和客实体
    3. 实体类型必须标注为：人物、组织、地点、事件或其他
    4. 包含关系出现的上下文片段
    5. 需要识别关系的子类型
    6. 为每个关系提供置信度评分（0-1）

    输出要求：
    - 使用严格JSON格式
    - 关系类型必须使用预定义的"主类型::子类型"格式
    - 每个关系必须包含以下字段：
      relation_type, relation_subtype, 
      head_entity（含entity_type, entity_cn_name, entity_raw_name）, 
      tail_entity, relation_context_cn, relation_context_raw, confidence

    示例参考（注意使用正确的JSON格式）：
    {few_shot_examples}"""

    # 构建提示模板
    prompt = PromptTemplate(
        template=system_template,
        input_variables=["text"],
        partial_variables={
            "relation_types": "\n".join(relation_types),
            "few_shot_examples": "\n\n".join(processed_examples)
        }
    )

    # 构建完整提示
    chat_prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate(prompt=prompt),
        ("user", "请分析以下文本：\n{text}")
    ])

    # 构建处理链
    chain = (
        {"text": RunnablePassthrough()}  # 直接传递文本输入
        | chat_prompt
        | llm
        | JsonOutputParser(pydantic_object=RelationExtractionOutput)
        | RunnableLambda(lambda x: x["relations"])
    ).with_types(
        input_type=dict,
        output_type=List[RelationNode]
    )

    return chain
