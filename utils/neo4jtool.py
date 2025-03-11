from py2neo import Graph, Node, Relationship, Transaction
from typing import List, Dict
import os
from urllib.parse import urlparse

def get_neo4j_connection():
    """从环境变量获取neo4j连接配置"""
    neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    username = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "123456789a")
    
    # 解析URI格式
    parsed = urlparse(neo4j_uri)
    secure = parsed.scheme == 'bolt+s' or parsed.scheme == 'neo4j+s'
    
    return Graph(
        host=parsed.hostname,
        port=parsed.port or 7687,
        scheme=parsed.scheme,
        secure=secure,
        user=username,
        password=password
    )

def save_to_neo4j(relations: List[Dict]):
    """将关系三元组持久化到Neo4j数据库"""
    graph = get_neo4j_connection()
    tx = graph.begin()
    
    try:
        # # 新增清空数据库代码
        # tx.run("MATCH (n) DETACH DELETE n")  # 删除所有节点和关系

        for rel in relations:
            # 创建/匹配头节点
            head = Node(
                rel["head_entity"]["entity_type"],
                name=rel["head_entity"]["entity_cn_name"],
                raw_name=rel["head_entity"]["entity_raw_name"]
            )
            tx.merge(head, primary_label=rel["head_entity"]["entity_type"], primary_key="name")

            # 创建/匹配尾节点
            tail = Node(
                rel["tail_entity"]["entity_type"],
                name=rel["tail_entity"]["entity_cn_name"],
                raw_name=rel["tail_entity"]["entity_raw_name"]
            )
            tx.merge(tail, primary_label=rel["tail_entity"]["entity_type"], primary_key="name")

            # 创建关系
            relationship = Relationship(
                head,
                rel["relation_type"].upper().replace(" ", "_"),
                tail,
                subtype=rel["relation_subtype"],
                context_cn=rel["relation_context_cn"],
                context_raw=rel["relation_context_raw"],
                confidence=rel["confidence"]
            )
            tx.create(relationship)

        tx.commit()
        print(f"成功存储{len(relations)}条关系")
    except Exception as e:
        tx.rollback()
        print(f"存储失败: {str(e)}")
        raise