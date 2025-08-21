#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整OCR处理器 - 处理所有27张图片
支持多种OCR方法进行比对验证
"""

import os
import base64
import json
import time
import requests
from pathlib import Path
import re
from typing import List, Dict, Tuple

class CompleteOCRProcessor:
    def __init__(self, api_key: str):
        """初始化OCR处理器"""
        self.api_key = api_key
        self.base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.results = {}

    def get_sorted_image_files(self, directory: str) -> List[str]:
        """获取按文件名排序的图片文件列表"""
        image_dir = Path(directory)
        if not image_dir.exists():
            raise ValueError(f"目录不存在: {directory}")
        
        # 获取所有jpg文件
        image_files = list(image_dir.glob("*.jpg"))
        
        # 按文件名中的数字排序（68-94顺序）
        def extract_number(filename):
            match = re.search(r'_(\d{2})\.jpg$', str(filename))
            return int(match.group(1)) if match else 999
        
        sorted_files = sorted(image_files, key=extract_number)
        return [str(f) for f in sorted_files]

    def extract_with_qwen_vl_max(self, image_path: str) -> str:
        """使用qwen-vl-max提取文字"""
        try:
            with open(image_path, 'rb') as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            
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
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
            else:
                return f"[qwen-vl-max识别失败: HTTP {response.status_code}]"
                
        except Exception as e:
            return f"[qwen-vl-max识别失败: {str(e)}]"

    def extract_with_qwen_vl_ocr(self, image_path: str) -> str:
        """使用qwen-vl-ocr模型提取文字（专业OCR模型）"""
        try:
            with open(image_path, 'rb') as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            
            payload = {
                "model": "qwen-vl-ocr-latest",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}",
                                    "min_pixels": 28 * 28 * 4,
                                    "max_pixels": 28 * 28 * 8192
                                }
                            }
                        ]
                    }
                ],
                "temperature": 0,
                "max_tokens": 4096
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
            else:
                return f"[qwen-vl-ocr识别失败: HTTP {response.status_code}]"
                
        except Exception as e:
            return f"[qwen-vl-ocr识别失败: {str(e)}]"

    def extract_with_different_prompts(self, image_path: str) -> str:
        """使用不同提示词再次提取，提高准确性"""
        try:
            with open(image_path, 'rb') as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            
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
                                "text": "这是老刘的投资笔记手写稿。请仔细逐字识别图片中的所有手写中文内容，包括：1)股票投资相关术语 2)人名和机构名 3)数字和日期 4)标点符号。请按原文布局输出，不要遗漏任何文字。"
                            }
                        ]
                    }
                ],
                "temperature": 0,
                "max_tokens": 4096
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
            else:
                return f"[备用方法识别失败: HTTP {response.status_code}]"
                
        except Exception as e:
            return f"[备用方法识别失败: {str(e)}]"

    def compare_and_choose_best(self, results: Dict[str, str]) -> Tuple[str, str]:
        """比较多种方法的结果，选择最佳的"""
        # 过滤掉失败的结果
        valid_results = {k: v for k, v in results.items() if not v.startswith('[')}
        
        if not valid_results:
            return "所有方法都失败", list(results.values())[0]
        
        if len(valid_results) == 1:
            method, text = list(valid_results.items())[0]
            return method, text
        
        # 选择最长的结果（通常更完整）
        best_method = max(valid_results.keys(), key=lambda k: len(valid_results[k]))
        best_text = valid_results[best_method]
        
        return best_method, best_text

    def process_single_image(self, image_path: str, page_num: int) -> Dict:
        """处理单个图片，使用多种方法"""
        filename = os.path.basename(image_path)
        print(f"\n[{page_num}/27] 处理: {filename}")
        
        results = {}
        
        # 方法1: qwen-vl-max
        print("  - 使用 qwen-vl-max...")
        results['qwen-vl-max'] = self.extract_with_qwen_vl_max(image_path)
        time.sleep(1)
        
        # 方法2: qwen-vl-ocr (专业OCR模型)
        print("  - 使用 qwen-vl-ocr...")
        results['qwen-vl-ocr'] = self.extract_with_qwen_vl_ocr(image_path)
        time.sleep(1)
        
        # 方法3: 不同提示词
        print("  - 使用优化提示词...")
        results['optimized-prompt'] = self.extract_with_different_prompts(image_path)
        time.sleep(1)
        
        # 比较结果选择最佳
        best_method, best_text = self.compare_and_choose_best(results)
        
        print(f"  ✓ 最佳方法: {best_method} (长度: {len(best_text)})")
        
        return {
            'filename': filename,
            'page_num': page_num,
            'results': results,
            'best_method': best_method,
            'best_text': best_text
        }

    def process_all_images(self, directory: str) -> List[Dict]:
        """处理所有图片"""
        image_files = self.get_sorted_image_files(directory)
        print(f"开始处理所有 {len(image_files)} 个图片文件...")
        print("=" * 60)
        
        all_results = []
        
        for i, image_path in enumerate(image_files, 1):
            result = self.process_single_image(image_path, i)
            all_results.append(result)
            
            # 每处理5个文件保存一次中间结果
            if i % 5 == 0:
                self.save_intermediate_results(all_results, f"ocr_progress_{i}.json")
                print(f"  💾 已保存进度: {i}/{len(image_files)}")
        
        print("=" * 60)
        print("✓ 所有图片处理完成!")
        return all_results

    def save_intermediate_results(self, results: List[Dict], filename: str):
        """保存中间结果"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

    def generate_complete_documents(self, results: List[Dict]):
        """生成完整文档"""
        
        # 生成文档1：原始OCR结果
        doc1_file = "老刘投资笔记_完整文档1_原始OCR提取.txt"
        with open(doc1_file, 'w', encoding='utf-8') as f:
            f.write("# 老刘投资笔记 - 完整文档1：原始OCR文字提取结果\n")
            f.write(f"# 生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("# 说明：本文档为老刘投资笔记手写内容的完整OCR识别结果\n")
            f.write("# 处理模型：阿里云 qwen-vl-max + qwen-vl-ocr 多重验证\n")
            f.write("# 文件总数：27张图片，按68-94顺序排列\n\n")
            f.write("=" * 80 + "\n\n")
            
            for result in results:
                f.write(f"## 第{result['page_num']}页 - {result['filename']}\n")
                f.write(f"### 最佳识别方法: {result['best_method']}\n\n")
                f.write(f"{result['best_text']}\n\n")
                f.write("-" * 80 + "\n\n")
        
        # 生成比对文档：包含所有方法的结果
        comparison_file = "老刘投资笔记_OCR方法比对.txt"
        with open(comparison_file, 'w', encoding='utf-8') as f:
            f.write("# 老刘投资笔记 - OCR方法比对文档\n")
            f.write(f"# 生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("# 说明：多种OCR方法的详细比对结果\n\n")
            f.write("=" * 80 + "\n\n")
            
            for result in results:
                f.write(f"## 第{result['page_num']}页 - {result['filename']}\n\n")
                
                for method, text in result['results'].items():
                    f.write(f"### {method} 结果:\n")
                    f.write(f"长度: {len(text)} 字符\n")
                    f.write(f"{text}\n\n")
                    f.write("-" * 40 + "\n")
                
                f.write(f"**最佳选择**: {result['best_method']}\n\n")
                f.write("=" * 80 + "\n\n")
        
        print(f"✓ 完整文档已生成:")
        print(f"  - 主文档: {doc1_file}")
        print(f"  - 比对文档: {comparison_file}")

def main():
    """主函数"""
    API_KEY = "sk-2eee3571d9954f5282586c576e33bfd5"
    IMAGES_DIR = "/mnt/c/Users/M2814/.cursor/investliu/investnotebook"
    
    processor = CompleteOCRProcessor(API_KEY)
    
    try:
        # 处理所有图片
        all_results = processor.process_all_images(IMAGES_DIR)
        
        # 保存完整结果
        processor.save_intermediate_results(all_results, "complete_ocr_results.json")
        
        # 生成文档
        processor.generate_complete_documents(all_results)
        
        # 统计结果
        total_pages = len(all_results)
        successful_pages = len([r for r in all_results if not r['best_text'].startswith('[')])
        
        print(f"\n📊 处理统计:")
        print(f"  总页数: {total_pages}")
        print(f"  成功处理: {successful_pages}")
        print(f"  成功率: {successful_pages/total_pages*100:.1f}%")
        
        # 各方法统计
        method_stats = {}
        for result in all_results:
            method = result['best_method']
            method_stats[method] = method_stats.get(method, 0) + 1
        
        print(f"\n🏆 最佳方法统计:")
        for method, count in sorted(method_stats.items(), key=lambda x: x[1], reverse=True):
            print(f"  {method}: {count} 页 ({count/total_pages*100:.1f}%)")
        
    except Exception as e:
        print(f"❌ 程序执行出错: {str(e)}")

if __name__ == "__main__":
    main()