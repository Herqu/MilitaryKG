import json
import sys
import os

def process_and_save(input_path):
    try:
        # 生成输出路径：在文件名后插入 _output
        dir_name = os.path.dirname(input_path)  # 获取目录路径
        base_name = os.path.basename(input_path)  # 获取文件名
        name_part, ext_part = os.path.splitext(base_name)  # 分离文件名和扩展名
        output_name = f"{name_part}_output{ext_part}"  # 添加 _output
        output_path = os.path.join(dir_name, output_name)  # 拼接完整路径

        return output_path

    except FileNotFoundError:
        print(f"错误：输入文件 {input_path} 不存在")
    except json.JSONDecodeError:
        print(f"错误：文件 {input_path} 不是有效的JSON格式")
    except PermissionError:
        print(f"权限错误：无法写入目录 {dir_name}")
    except Exception as e:
        print(f"未知错误：{str(e)}")


def clean_json_data(input_file):
    """清理JSON数据，删除contentext字段为空的条目"""
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 过滤保留contentext非空条目
    cleaned_records = [
        record for record in data['RECORDS'] 
        if record.get('contentext', '').strip()
    ]
    
    # 更新数据并写回原文件
    data['RECORDS'] = cleaned_records
    output_file = process_and_save(input_file)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python json_data_clear.py 文件路径")
        sys.exit(1)
        
    file_path = sys.argv[1]
    clean_json_data(file_path)