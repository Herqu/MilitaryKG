# 模型配置
export OPENAI_API_KEY="sk-ioxhfxvyzszzulnoeraavatqzrtbbuzbpoxrtophokxjzeyi" # Set your Planner API key here as environment variable
PLANNER="silicon"
# 模型名称
export DEEPSEEKR1="Pro/deepseek-ai/DeepSeek-R1"
export DEEPSEEKv3="Pro/deepseek-ai/DeepSeek-V3"

# neo4j代码
export NEO4J_URL="bolt://localhost:7687"
export NEO4J_USER="neo4j"
export NEO4J_PASSWORD="123456789a"

# 默认格式路径
export DEFAULT_DATA_PATH='/root/autodl-tmp/GraphAgent/MilitaryKG/data/test_data_wljk3113.json'

# CUDA_VISIBLE_DEVICES=1,2,3 python run.py --planner $PLANNER
CUDA_VISIBLE_DEVICES=1,2,3 python graph_extraction_server.py --planner $PLANNER