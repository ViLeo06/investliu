#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
老刘投资笔记OCR处理器 - 完整版
处理所有剩余的图片文件
"""

import os
import base64
import json
import time
import requests
from pathlib import Path
import re

def get_sorted_image_files(directory):
    """获取按文件名排序的图片文件列表"""
    image_dir = Path(directory)
    if not image_dir.exists():
        raise ValueError(f"目录不存在: {directory}")
    
    # 获取所有jpg文件
    image_files = list(image_dir.glob("*.jpg"))
    
    # 按文件名中的数字排序（68-94顺序）
    def extract_number(filename):
        # 提取文件名中的最后两位数字
        match = re.search(r'_(\d{2})\.jpg$', str(filename))
        return int(match.group(1)) if match else 999
    
    sorted_files = sorted(image_files, key=extract_number)
    return [str(f) for f in sorted_files]

def extract_text_from_image(image_path, api_key):
    """从图片中提取文字"""
    
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        # 编码图片
        with open(image_path, 'rb') as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        # 构建请求数据
        payload = {
            "model": "qwen-vl-max-latest",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        },
                        {
                            "type": "text",
                            "text": "请准确识别图片中的所有手写文字内容，保持原有的换行和标点符号，不要添加任何解释或分析，只输出识别到的文字内容。"
                        }
                    ]
                }
            ],
            "temperature": 0.1,
            "max_tokens": 4096
        }
        
        # 发送请求
        response = requests.post(
            f"{base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=120
        )
        
        if response.status_code == 200:
            result = response.json()
            extracted_text = result['choices'][0]['message']['content'].strip()
            return extracted_text
        else:
            error_msg = f"API调用失败，状态码: {response.status_code}"
            print(f"❌ {error_msg}")
            return f"[OCR识别失败: {error_msg}]"
            
    except Exception as e:
        error_msg = f"处理失败: {str(e)}"
        print(f"❌ {error_msg}")
        return f"[OCR识别失败: {error_msg}]"

def main():
    """主函数 - 处理所有剩余文件"""
    
    # 配置
    API_KEY = "sk-2eee3571d9954f5282586c576e33bfd5"
    IMAGES_DIR = "/mnt/c/Users/M2814/.cursor/investliu/investnotebook"
    OUTPUT_FILE = "/mnt/c/Users/M2814/.cursor/investliu/laoliu_notes_ocr_complete.txt"
    
    # 获取图片文件列表
    image_files = get_sorted_image_files(IMAGES_DIR)
    print(f"找到 {len(image_files)} 个图片文件")
    
    # 处理第6个文件开始（前5个已经处理）
    remaining_files = image_files[5:]
    
    print(f"开始处理剩余 {len(remaining_files)} 个文件...")
    print("=" * 50)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("# 老刘投资笔记 - OCR文字提取结果 (剩余文件)\n")
        f.write(f"# 处理时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# 处理文件数: {len(remaining_files)}\n\n")
        
        for i, image_path in enumerate(remaining_files, 6):  # 从第6个开始编号
            filename = os.path.basename(image_path)
            print(f"[{i}/{len(image_files)}] 处理: {filename}")
            
            # 提取文字
            extracted_text = extract_text_from_image(image_path, API_KEY)
            
            # 写入文件
            f.write(f"## 第{i}页 - {filename}\n\n")
            f.write(f"{extracted_text}\n\n")
            f.write("-" * 80 + "\n\n")
            
            print(f"✓ 完成: {filename}")
            
            # 避免API调用过快
            time.sleep(2)
    
    print("=" * 50)
    print(f"✓ 剩余文件处理完成！结果已保存到: {OUTPUT_FILE}")
    print(f"现在需要合并batch1和complete两个文件")

if __name__ == "__main__":
    main()