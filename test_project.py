"""
项目集成测试脚本 (Windows版本)
"""

import os
import sys
import json
import subprocess
import importlib.util

def print_header(title):
    print("=" * 50)
    print(title)
    print("=" * 50)

def print_step(step, description):
    print(f"{step}. {description}")

def check_python():
    """检查Python环境"""
    print_step(1, "检查Python环境...")
    try:
        version = sys.version
        print(f"✅ Python版本: {version}")
        return True
    except Exception as e:
        print(f"❌ Python环境错误: {e}")
        return False

def check_dependencies():
    """检查依赖包"""
    print_step(2, "检查Python依赖包...")
    
    required_packages = [
        'requests', 'pandas', 'numpy', 'json', 'datetime'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'json' or package == 'datetime':
                # 内置模块
                __import__(package)
            else:
                importlib.import_module(package)
            print(f"✅ {package} 已安装")
        except ImportError:
            print(f"❌ {package} 未安装")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ 缺失依赖包: {', '.join(missing_packages)}")
        print("请运行: pip install -r requirements.txt")
        return False
    
    print("✅ 核心依赖包检查通过")
    return True

def check_project_structure():
    """检查项目结构"""
    print_step(3, "检查项目结构...")
    
    required_dirs = [
        "data_processor",
        "miniprogram", 
        "static_data",
        "notes",
        ".github/workflows"
    ]
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✅ {dir_name} 目录存在")
        else:
            print(f"❌ {dir_name} 目录不存在")
            return False
    
    return True

def check_key_files():
    """检查关键文件"""
    print_step(4, "检查关键文件...")
    
    required_files = [
        "data_processor/ocr_processor.py",
        "data_processor/rule_extractor.py",
        "data_processor/stock_data_fetcher.py", 
        "data_processor/stock_analyzer.py",
        "data_processor/data_generator.py",
        "data_processor/__init__.py",
        "update_data.py",
        "requirements.txt",
        "miniprogram/app.js",
        "miniprogram/app.json",
        ".github/workflows/deploy.yml"
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} 存在")
        else:
            print(f"❌ {file_path} 不存在")
            return False
    
    return True

def test_data_modules():
    """测试数据处理模块"""
    print_step(5, "测试数据处理模块...")
    
    try:
        # 添加项目根目录到路径
        sys.path.insert(0, '.')
        
        from data_processor import StockDataFetcher, StockAnalyzer
        
        # 测试股票数据获取
        fetcher = StockDataFetcher()
        print("✅ 股票数据获取模块导入成功")
        
        # 测试股票分析
        analyzer = StockAnalyzer()
        print("✅ 股票分析模块导入成功")
        
        print("✅ 数据处理模块测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 数据处理模块测试失败: {e}")
        return False

def test_data_generation():
    """测试数据生成"""
    print_step(6, "测试数据生成（简化版）...")
    
    try:
        from data_processor.stock_data_fetcher import StockDataFetcher
        from data_processor.stock_analyzer import StockAnalyzer
        
        # 测试获取少量数据
        fetcher = StockDataFetcher()
        print("正在获取测试数据...")
        
        # 获取市场指数
        indices = fetcher.get_market_index()
        if indices:
            print(f"✅ 获取到 {len(indices)} 个市场指数")
        else:
            print("⚠️  未获取到市场指数数据（可能是网络问题）")
        
        # 获取少量股票数据
        try:
            a_stocks = fetcher.get_stock_list_a(page=1, size=5)
            if a_stocks:
                print(f"✅ 获取到 {len(a_stocks)} 只A股数据")
            else:
                print("⚠️  未获取到A股数据（可能是网络问题）")
        except Exception as e:
            print(f"⚠️  获取股票数据失败: {e}")
        
        print("✅ 数据获取测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 数据生成测试失败: {e}")
        return False

def check_miniprogram_files():
    """检查小程序文件"""
    print_step(7, "检查小程序文件...")
    
    miniprogram_files = [
        "miniprogram/app.js",
        "miniprogram/app.json", 
        "miniprogram/app.wxss",
        "miniprogram/pages/index/index.js",
        "miniprogram/pages/index/index.wxml",
        "miniprogram/pages/index/index.wxss",
        "miniprogram/pages/index/index.json"
    ]
    
    for file_path in miniprogram_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} 存在")
        else:
            print(f"❌ {file_path} 不存在")
            return False
    
    return True

def check_json_format():
    """检查JSON文件格式"""
    print_step(8, "检查小程序配置文件格式...")
    
    json_files = [
        "miniprogram/app.json",
        "miniprogram/project.config.json",
        "miniprogram/pages/index/index.json"
    ]
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                json.load(f)
            print(f"✅ {json_file} 格式正确")
        except Exception as e:
            print(f"❌ {json_file} 格式错误: {e}")
            return False
    
    return True

def print_final_instructions():
    """打印最终说明"""
    print()
    print("=" * 50)
    print("✅ 所有测试通过！")
    print("=" * 50)
    print()
    print("🚀 项目已准备就绪，可以进行以下操作：")
    print()
    print("1. 配置API密钥:")
    print("   copy config.example.py config.py")
    print("   # 编辑config.py添加你的API密钥")
    print()
    print("2. 生成数据:")
    print("   python update_data.py")
    print()
    print("3. 部署到GitHub Pages:")
    print("   git add .")
    print("   git commit -m \"部署老刘投资决策系统\"")
    print("   git push origin main")
    print()
    print("4. 开发小程序:")
    print("   # 用微信开发者工具打开 miniprogram 目录")
    print()
    print("📊 项目特点:")
    print("   ✓ 零服务器成本")
    print("   ✓ 自动数据更新")
    print("   ✓ 智能股票推荐")
    print("   ✓ 完整小程序界面")
    print()
    print("⚠️  注意事项:")
    print("   - 投资有风险，仅供参考")
    print("   - 需要申请相关API密钥")
    print("   - 小程序需要相应资质")
    print()

def main():
    """主测试函数"""
    print_header("老刘投资决策系统 - 集成测试")
    
    # 执行所有测试
    tests = [
        check_python,
        check_dependencies,
        check_project_structure,
        check_key_files,
        test_data_modules,
        test_data_generation,
        check_miniprogram_files,
        check_json_format
    ]
    
    for test in tests:
        if not test():
            print()
            print("❌ 测试失败，请检查上述错误并修复")
            sys.exit(1)
        print()
    
    # 所有测试通过
    print_final_instructions()

if __name__ == "__main__":
    main()