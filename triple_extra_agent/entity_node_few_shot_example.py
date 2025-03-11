few_shot_example_1 = \
(
    """示例1:
        输入: Jack Ma met with Apple CEO Tim Cook at Alibaba's Hangzhou headquarters
        输出:
        {\"entities\":
            [
                {
                    \"entity_type\":\"人物\",
                    \"entity_cn_name\":\"马云\",
                    \"entity_raw_name\":\"马云\",
                    \"context_cn\":\"马云在阿里巴巴杭州总部会见\",
                    \"context_raw\":\"Jack Ma met at Alibaba Hangzhou Headquarters\" 
                },
                {
                    \"entity_type\":\"组织\",
                    \"entity_cn_name\":\"阿里巴巴集团\",
                    \"entity_raw_name\":\"Alibaba Group\",
                    \"context_cn\":\"阿里巴巴杭州总部\",
                    \"context_raw\":\"Alibaba's Hangzhou headquarters\"
                },
                {
                    \"entity_type\":\"地点\",
                    \"entity_cn_name\":\"杭州\",
                    \"entity_raw_name\":\"Hangzhou\",
                    \"context_cn\":\"杭州总部\",
                    \"context_raw\":\"Hangzhou headquarters\"
                },
                {
                    \"entity_type\":\"人物\",
                    \"entity_cn_name\":\"蒂姆·库克\",
                    \"entity_raw_name\":\"Tim Cook\", 
                    \"context_cn\":\"苹果CEO库克\",
                    \"context_raw\":\"Apple CEO Tim Cook\"
                },
                {
                    \"entity_type\":\"组织\",
                    \"entity_cn_name\":\"苹果公司\",
                    \"entity_raw_name\":\"Apple Inc.\",
                    \"context_cn\":\"苹果CEO\",
                    \"context_raw\":\"Apple CEO\"
                },
                {
                    \"entity_type\":\"事件\",
                    \"entity_cn_name\":\"马云在阿里巴巴杭州总部会见了库克\",
                    \"entity_raw_name\":\"Jack Ma met with Apple CEO Tim Cook at Alibaba's Hangzhou headquarters\",
                    \"context_cn\":\"马云在阿里巴巴杭州总部会见了苹果CEO库克\",
                    \"context_raw\":\"Jack Ma met with Apple CEO Tim Cook at Alibaba's Hangzhou headquarters\"
                }
            ]
        }
    """.strip(),
)
