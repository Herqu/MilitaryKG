from utils.storage import mem_store
from utils.llm import llm
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from .chains import create_keywords_from_scaffold_text_chain, create_scaffold_text_parsing_chain, create_scaffold_node_extraction_chain
from functools import partial
import json
from .pyg_utils import build_hetero_graph_from_scaffold_keywords_v2
from colorama import Fore, Style

scaffold_node_extraction_chain = create_scaffold_node_extraction_chain(llm)
scaffold_text_parsing_chain = create_scaffold_text_parsing_chain(llm)
keywords_from_scaffold_text_chain = create_keywords_from_scaffold_text_chain(llm)

def save_pyg_graph_to_mem(x):
    mem_store.mset([("pyg_graph", x["pyg_graph"])])
    return x

def parse_keywords_from_scaffold_texts(x, chain=keywords_from_scaffold_text_chain):
    scaffold_texts = x["scaffold_texts_parsing_output"]["scaffold_texts"]
    keywords = {}
    for item in scaffold_texts:
        keywords[item["node_id"]] = chain.invoke({"input": item["text"]})["keywords"]
    return keywords

def print_lambda(message, color=Fore.RESET):
    return lambda x: (print(color + message + json.dumps(x, indent=4) + Style.RESET_ALL), x)[1]


# 分为 四部
# 首先生成节点
# 然后拆分文本。
# 然后生成keyword，
# 然后链接节点和keyword
# 
agent = (
    RunnablePassthrough.assign(scaffold_nodes_extraction_output=scaffold_node_extraction_chain)
    | print_lambda("SCAFFOLD NODES DISCOVERY: ", Fore.CYAN)
    | RunnablePassthrough.assign(scaffold_texts_parsing_output=scaffold_text_parsing_chain)
    | print_lambda("KNOWLEDGE AUGMENTATION: ", Fore.GREEN)
    | RunnablePassthrough.assign(keywords=partial(parse_keywords_from_scaffold_texts, chain=keywords_from_scaffold_text_chain))
    | print_lambda("SCAFFOLD NODES DISCOVERY-2 (KEYWORDS): ", Fore.MAGENTA)
    | print_lambda("GRAPH GROUNDING... ", Fore.YELLOW)
    | RunnablePassthrough.assign(pyg_graph=build_hetero_graph_from_scaffold_keywords_v2) # 这里输出的是一个异构图文件。heterodata，就是知识图谱。
    # | heterodata_to_neo4j
    | RunnableLambda(save_pyg_graph_to_mem)
    | RunnableLambda(lambda x: f"I have constructed a heterogeneous graph based on your request: {x.get('pyg_graph')}")
)


if __name__ == "__main__":
    pass