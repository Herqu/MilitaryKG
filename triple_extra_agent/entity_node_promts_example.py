# few_shot_example_1 = \
# (
#     """
#     Input:
#     Knowledge Text:
#     Paper Title: Simple Neural Network for Image Classification
#     Abstract: We present a basic neural network architecture for image classification. Our model uses three layers and achieves 85% accuracy on the test dataset. The implementation is straightforward and suitable for educational purposes. Experimental results show that this simple architecture can serve as a good baseline for more complex models.

#     User Annotation:
#     Which category should the paper be classified into? You have the following choices: Distributed Parallel and Cluster Computing (cs.DC), Computer Vision and Pattern Recognition (cs.CV), Machine Learning (cs.LG), Artificial Intelligence (cs.AI), Neural and Evolutionary Computing (cs.NE)
#     """.strip()
#     ,
#     """
#     Output:
#     {{
#         "思考过程": "1. 理解任务: 这是一个论文分类任务，需要将研究论文归类到不同的计算机科学领域
#                  2. 分析输入: 我们有一篇关于神经网络和图像分类的论文，包含标题和摘要
#                  3. 论文分类任务通常需要理解:
#                     - 论文的研究主题
#                     - 研究背景和上下文
#                     - 解决的研究问题
#                     - 采用的方法论
#                     - 取得的关键成果
#                  4. 这些要素帮助确定所属的计算机领域",
#         "骨架节点": [
#             {{"id": 0, "类型": "论文", "名称": "简单神经网络图像分类"}},
#             {{"id": 1, "类型": "研究背景", "名称": "研究背景"}},
#             {{"id": 2, "类型": "研究问题", "名称": "研究问题"}},
#             {{"id": 3, "类型": "方法论", "名称": "方法论"}},
#             {{"id": 4, "类型": "关键成果", "名称": "关键成果"}}
#         ]
#     }}
#     """.strip()
# )

# few_shot_example_2 = \
# (
# """
# Input:
# Knowledge Text:
# Story Title: Romeo and Juliet (Act 1 Scene 1)
# Text: Two households, both alike in dignity, In fair Verona, where we lay our scene, From ancient grudge break to new mutiny, Where civil blood makes civil hands unclean. From forth the fatal loins of these two foes, A pair of star-cross'd lovers take their life. The fearful passage of their death-mark'd love, And the continuance of their parents' rage, Which, but their children's end, nought could remove.
# User Annotation:
# Analyze the key themes, characters, and relationships in this story. Focus on how family dynamics and social conflicts influence the plot development.
# """.strip()
# ,
# """
# Output:
# {{
# "思考过程": "1. 理解任务: 这是文学分析任务，聚焦主题、人物和关系
# 2. 分析输入: 包含家族冲突、爱情悲剧的复杂叙事
# 3. 故事分析需要理解:
# - 关键人物及其关系
# - 社会与家族背景
# - 推动叙事的核心冲突
# - 这些要素的互动演变
# - 最终呈现的主题思想
# 4. 这些要素帮助分析家族动态如何影响故事发展",
# "骨架节点": [
#     {{"id": 0, "类型": "家族群体", "名称": "对立家族"}},
