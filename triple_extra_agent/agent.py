from utils.storage import mem_store
from utils.llm import llm
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from .entitity_chains import  create_extract_entity_nodes_chain
from .relation_chain import  create_extract_entity_relation_chain
from functools import partial
import json
from colorama import Fore, Style
from tqdm import tqdm  # 用于进度显示
from .tool import print_lambda


# 实体提取链
# 当前的设计没有提供few_shot 的example案例。
extract_entity_nodes_chain = create_extract_entity_nodes_chain(llm)
extract_entity_relation_chain = create_extract_entity_relation_chain(llm)


# 定义处理单个记录的流水线

# 分为 四部
# 首先生成节点
# 然后拆分文本。
# 然后生成keyword，
# 然后链接节点和keyword
# 
agent = (
    print_lambda("START KNOWLEDGE EXTRAT:\n ", Fore.CYAN)
    # | RunnablePassthrough.assign(entity_nodes_extraction_output=extract_entity_nodes_chain)  # 先抽取实体
    # | print_lambda("Entity NODES DISCOVERY: ", Fore.CYAN)
    | RunnablePassthrough.assign(relation_extraction_output=extract_entity_relation_chain)
    | print_lambda("RELATION TRIPLE DISCOVERY: \n", Fore.GREEN)
    # | print_lambda("FINISHED", Fore.RED)
)



