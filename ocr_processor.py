#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
老刘投资笔记OCR处理器
使用阿里云qwen-vl-max模型进行图片文字识别
"""

import os
import base64
import json
import time
import requests
from pathlib import Path
import re
from typing import List, Dict, Tuple

class QwenOCRProcessor:
    def __init__(self, api_key: str):
        """初始化OCR处理器"""
        self.api_key = api_key
        self.base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
    def encode_image_to_base64(self, image_path: str) -> str:
        """将图片文件转换为base64编码"""
        with open(image_path, 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def extract_text_from_image(self, image_path: str, retry_count: int = 3) -> str:
        """从图片中提取文字"""
        for attempt in range(retry_count):
            try:
                # 编码图片
                base64_image = self.encode_image_to_base64(image_path)
                
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
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json=payload,
                    timeout=60
                )
                
                if response.status_code == 200:
                    result = response.json()
                    extracted_text = result['choices'][0]['message']['content'].strip()
                    print(f"✓ 成功处理: {os.path.basename(image_path)}")
                    return extracted_text
                else:
                    error_msg = f"API调用失败，状态码: {response.status_code}, 响应: {response.text}"
                    print(f"✗ API错误: {error_msg}")
                    raise Exception(error_msg)
                
            except Exception as e:
                print(f"✗ 处理失败 (尝试 {attempt + 1}/{retry_count}): {os.path.basename(image_path)} - {str(e)}")
                if attempt < retry_count - 1:
                    time.sleep(2)  # 重试前等待2秒
                else:
                    return f"[OCR识别失败: {str(e)}]"
        
        return "[OCR识别失败: 超过最大重试次数]"

    def get_sorted_image_files(self, directory: str) -> List[str]:
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

    def batch_process_images(self, directory: str, output_file: str = None) -> Dict[str, str]:
        """批量处理图片文件"""
        if output_file is None:
            output_file = "laoliu_notes_ocr_raw.txt"
        
        image_files = self.get_sorted_image_files(directory)
        results = {}
        
        print(f"开始处理 {len(image_files)} 个图片文件...")
        print("=" * 50)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# 老刘投资笔记 - OCR原始文字提取结果\n")
            f.write(f"# 处理时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# 处理文件数: {len(image_files)}\n\n")
            
            for i, image_path in enumerate(image_files, 1):
                filename = os.path.basename(image_path)
                print(f"[{i}/{len(image_files)}] 处理: {filename}")
                
                # 提取文字
                extracted_text = self.extract_text_from_image(image_path)
                results[filename] = extracted_text
                
                # 写入文件
                f.write(f"## 第{i}页 - {filename}\n\n")
                f.write(f"{extracted_text}\n\n")
                f.write("-" * 80 + "\n\n")
                
                # 避免API调用过快
                time.sleep(1)
        
        print("=" * 50)
        print(f"✓ 批量处理完成！结果已保存到: {output_file}")
        return results

def main():
    """主函数"""
    # 配置
    API_KEY = "sk-2eee3571d9954f5282586c576e33bfd5"
    IMAGES_DIR = "/mnt/c/Users/M2814/.cursor/investliu/investnotebook"
    OUTPUT_FILE = "/mnt/c/Users/M2814/.cursor/investliu/laoliu_notes_ocr_raw.txt"
    
    try:
        # 初始化OCR处理器
        processor = QwenOCRProcessor(API_KEY)
        
        # 批量处理图片
        results = processor.batch_process_images(IMAGES_DIR, OUTPUT_FILE)
        
        # 生成处理统计
        total_files = len(results)
        successful_files = sum(1 for text in results.values() if not text.startswith("[OCR识别失败"))
        
        print(f"\n📊 处理统计:")
        print(f"   总文件数: {total_files}")
        print(f"   成功处理: {successful_files}")
        print(f"   失败文件: {total_files - successful_files}")
        print(f"   成功率: {successful_files/total_files*100:.1f}%")
        
        if successful_files < total_files:
            print(f"\n⚠️  有 {total_files - successful_files} 个文件处理失败，请检查:")
            for filename, text in results.items():
                if text.startswith("[OCR识别失败"):
                    print(f"   - {filename}: {text}")
        
    except Exception as e:
        print(f"❌ 程序执行出错: {str(e)}")

if __name__ == "__main__":
    main()