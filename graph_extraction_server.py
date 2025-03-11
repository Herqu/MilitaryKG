import sys
import os
# from graph_agent import GraphActionAgent
# from graph_action_agent import GraphActionAgent
from utils.storage import mem_store
from utils.args_parser import args
from graph_generation_agent.agent import agent as graph_generation_agent
from triple_extra_agent.agent import agent as triple_extra_agent
from utils.storage import mem_store
import torch
import json
from colorama import Fore, Style
from tqdm import tqdm  # 用于进度显示
from utils.neo4jtool import save_to_neo4j





def main():

    while True:
        user_input = input("Please enter a user instruction or file path (or type 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break
        elif user_input.lower() == 'test':
            user_input = os.environ['DEFAULT_DATA_PATH']

        

        #    """批量处理JSON文件"""
        # 读取JSON数据
        with open(user_input, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # 进度条显示处理过程
        for record in tqdm(data["RECORDS"], desc="Processing records"):
            # """处理单个记录并返回异构图数据"""
            # 组合输入文本（根据需求调整字段组合逻辑）
            input_text = "\n".join([f"{key}：{value}" for key, value in record.items()])
            
            # 执行处理链
            result = triple_extra_agent.invoke({"input": input_text})
            
            # 转换异构图格式并导入Neo4j
            if "relation_extraction_output" in result:
                save_to_neo4j(result["relation_extraction_output"])  # 确保该函数使用MERGE操作





if __name__ == "__main__":
    main()