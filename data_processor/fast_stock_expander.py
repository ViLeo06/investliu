# 快速扩展股票数据库 - 基于现有数据模式
import json
import random
from datetime import datetime

# 中国知名公司和股票代码
REAL_A_STOCKS = [
    # 银行股
    {"code": "000001", "name": "平安银行", "industry": "银行"},
    {"code": "600036", "name": "招商银行", "industry": "银行"},
    {"code": "601398", "name": "工商银行", "industry": "银行"},
    {"code": "601939", "name": "建设银行", "industry": "银行"},
    {"code": "601288", "name": "农业银行", "industry": "银行"},
    {"code": "600000", "name": "浦发银行", "industry": "银行"},
    {"code": "601166", "name": "兴业银行", "industry": "银行"},
    {"code": "000002", "name": "万科A", "industry": "房地产"},
    {"code": "600519", "name": "贵州茅台", "industry": "食品饮料"},
    {"code": "000858", "name": "五粮液", "industry": "食品饮料"},
    {"code": "002415", "name": "海康威视", "industry": "电子"},
    {"code": "000063", "name": "中兴通讯", "industry": "通信设备"},
    {"code": "002594", "name": "比亚迪", "industry": "汽车"},
    {"code": "600276", "name": "恒瑞医药", "industry": "医药"},
    {"code": "300015", "name": "爱尔眼科", "industry": "医疗服务"},
    {"code": "000725", "name": "京东方A", "industry": "电子"},
    {"code": "002304", "name": "洋河股份", "industry": "食品饮料"},
    {"code": "600309", "name": "万华化学", "industry": "化工"},
    {"code": "000568", "name": "泸州老窖", "industry": "食品饮料"},
    {"code": "002142", "name": "宁波银行", "industry": "银行"},
    {"code": "600887", "name": "伊利股份", "industry": "食品饮料"},
    {"code": "000002", "name": "万科A", "industry": "房地产"},
    {"code": "600036", "name": "招商银行", "industry": "银行"},
    {"code": "000001", "name": "平安银行", "industry": "银行"},
    {"code": "600519", "name": "贵州茅台", "industry": "食品饮料"},
    {"code": "000858", "name": "五粮液", "industry": "食品饮料"},
    {"code": "600036", "name": "招商银行", "industry": "银行"},
    {"code": "000001", "name": "平安银行", "industry": "银行"},
    {"code": "601318", "name": "中国平安", "industry": "保险"},
    {"code": "600028", "name": "中国石化", "industry": "石油石化"}
]

# 扩展股票代码和名称
EXTENDED_STOCKS = []

# 生成更多A股
for i in range(600001, 605000):  # 主板
    EXTENDED_STOCKS.append({
        "code": f"{i:06d}",
        "name": f"股票{i}",
        "industry": random.choice(["银行", "食品饮料", "医药", "房地产", "汽车", "电子", "通信设备", "化工", "机械设备"])
    })

for i in range(1, 3000):  # 深交所
    EXTENDED_STOCKS.append({
        "code": f"{i:06d}",
        "name": f"深股{i}",
        "industry": random.choice(["银行", "食品饮料", "医药", "房地产", "汽车", "电子", "通信设备", "化工", "机械设备"])
    })

for i in range(300001, 301000):  # 创业板
    EXTENDED_STOCKS.append({
        "code": f"{i:06d}",
        "name": f"创业板{i}",
        "industry": random.choice(["科技", "电子", "医药", "新能源", "软件", "互联网"])
    })

def generate_stock_data(stock_info):
    """生成股票数据"""
    code = stock_info["code"]
    name = stock_info["name"]
    industry = stock_info["industry"]
    
    # 使用代码作为随机种子保证数据一致性
    random.seed(int(code[-4:]) if code[-4:].isdigit() else 1000)
    
    # 根据行业设定价格范围
    if industry == "银行":
        current_price = round(random.uniform(4, 50), 2)
        pe_ratio = round(random.uniform(4, 15), 1)
        pb_ratio = round(random.uniform(0.5, 2.5), 2)
    elif industry == "食品饮料":
        current_price = round(random.uniform(20, 200), 2)
        pe_ratio = round(random.uniform(15, 35), 1) 
        pb_ratio = round(random.uniform(2, 8), 2)
    elif industry == "医药":
        current_price = round(random.uniform(15, 100), 2)
        pe_ratio = round(random.uniform(20, 45), 1)
        pb_ratio = round(random.uniform(1.5, 6), 2)
    elif industry == "房地产":
        current_price = round(random.uniform(3, 30), 2)
        pe_ratio = round(random.uniform(6, 20), 1)
        pb_ratio = round(random.uniform(0.8, 3), 2)
    elif industry in ["科技", "电子"]:
        current_price = round(random.uniform(10, 150), 2)
        pe_ratio = round(random.uniform(25, 60), 1)
        pb_ratio = round(random.uniform(2, 12), 2)
    else:
        current_price = round(random.uniform(5, 80), 2)
        pe_ratio = round(random.uniform(8, 30), 1)
        pb_ratio = round(random.uniform(1, 5), 2)
    
    change_percent = round(random.uniform(-10, 10), 2)
    volume = random.randint(100000, 100000000)
    market_cap = round(current_price * random.randint(1000000, 100000000), 0)
    
    # 计算老刘评分
    laoliu_score = calculate_laoliu_score(pe_ratio, pb_ratio, industry, change_percent)
    
    return {
        "code": code,
        "name": name,
        "market": "A",
        "current_price": current_price,
        "change_percent": change_percent,
        "volume": volume,
        "market_cap": market_cap,
        "pe_ratio": pe_ratio,
        "pb_ratio": pb_ratio,
        "turnover_rate": round(random.uniform(0.1, 10), 2),
        "amplitude": round(random.uniform(0.5, 15), 2),
        "industry": industry,
        "laoliu_score": laoliu_score,
        "investment_advice": get_investment_advice(laoliu_score),
        "recommendation": get_recommendation(laoliu_score),
        "analysis_points": get_analysis_points(pe_ratio, pb_ratio, industry),
        "risk_warnings": get_risk_warnings(pe_ratio, pb_ratio),
        "update_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

def calculate_laoliu_score(pe, pb, industry, change):
    """计算老刘评分"""
    score = 50
    
    if 0 < pe <= 15:
        score += 20
    elif 15 < pe <= 25:
        score += 10
    elif pe > 30:
        score -= 10
    
    if 0 < pb <= 2:
        score += 15
    elif pb > 5:
        score -= 10
    
    if industry == "银行":
        score += 15
    elif industry in ["食品饮料", "医药"]:
        score += 10
    
    if change < -5:
        score += 5
    
    return max(0, min(100, score))

def get_investment_advice(score):
    if score >= 80:
        return "强烈推荐：基本面优秀，符合老刘理念"
    elif score >= 65:
        return "推荐：基本面良好，可适当配置"
    elif score >= 50:
        return "观望：存在投资价值，建议观察"
    else:
        return "不推荐：风险较高，暂不建议"

def get_recommendation(score):
    if score >= 80:
        return "strong_buy"
    elif score >= 65:
        return "buy"
    elif score >= 50:
        return "hold"
    else:
        return "sell"

def get_analysis_points(pe, pb, industry):
    points = []
    if pe <= 15:
        points.append(f"PE仅{pe}倍，估值偏低")
    if pb <= 2:
        points.append(f"PB仅{pb}倍，账面价值安全")
    if industry == "银行":
        points.append("银行业符合老刘投资偏好")
    elif industry == "食品饮料":
        points.append("消费行业，品牌价值稳定")
    return points[:3] if points else ["基本面分析中"]

def get_risk_warnings(pe, pb):
    warnings = []
    if pe > 30:
        warnings.append("市盈率偏高，注意估值风险")
    if pb > 5:
        warnings.append("市净率较高，账面价值风险")
    return warnings[:2]

def main():
    print("快速生成扩展股票数据...")
    
    # 合并真实股票和扩展股票
    all_stocks_info = REAL_A_STOCKS + EXTENDED_STOCKS[:5000]  # 总计约5000只
    
    print(f"准备生成 {len(all_stocks_info)} 只A股数据...")
    
    # 生成股票数据
    a_stocks = []
    for i, stock_info in enumerate(all_stocks_info):
        if i % 500 == 0:
            print(f"进度: {i+1}/{len(all_stocks_info)}")
        
        stock_data = generate_stock_data(stock_info)
        a_stocks.append(stock_data)
    
    print(f"A股数据生成完成: {len(a_stocks)} 只")
    
    # 生成港股数据 (简化版)
    hk_stocks = []
    for i in range(1, 2001):  # 2000只港股
        code = f"{i:05d}"
        stock_data = {
            "code": code,
            "name": f"港股{i}",
            "market": "HK", 
            "current_price": round(random.uniform(1, 500), 2),
            "change_percent": round(random.uniform(-5, 5), 2),
            "volume": random.randint(1000000, 50000000),
            "market_cap": 0,
            "pe_ratio": round(random.uniform(5, 30), 1),
            "pb_ratio": round(random.uniform(0.8, 5), 2),
            "turnover_rate": round(random.uniform(0.1, 8), 2),
            "amplitude": round(random.uniform(0.5, 10), 2),
            "industry": random.choice(["科技", "金融", "地产", "零售", "制造"]),
            "laoliu_score": random.randint(40, 85),
            "investment_advice": "港股分析中",
            "recommendation": "hold",
            "analysis_points": ["港股市场"],
            "risk_warnings": ["汇率风险"],
            "update_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        hk_stocks.append(stock_data)
    
    print(f"港股数据生成完成: {len(hk_stocks)} 只")
    
    # 创建数据结构
    a_stock_data = {
        "total_count": len(a_stocks),
        "market": "A股",
        "update_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "stocks": a_stocks
    }
    
    hk_stock_data = {
        "total_count": len(hk_stocks),
        "market": "港股",
        "update_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "stocks": hk_stocks
    }
    
    # 生成分析样本
    top_stocks = sorted(a_stocks, key=lambda x: x['laoliu_score'], reverse=True)[:100]
    analysis_results = []
    
    for stock in top_stocks:
        analysis_result = {
            "basic_info": {
                "code": stock['code'],
                "name": stock['name'],
                "market_type": "A",
                "current_price": stock['current_price'],
                "change_percent": stock['change_percent'],
                "volume": stock['volume'],
                "market_cap": stock['market_cap'],
                "industry": stock['industry'],
                "update_time": stock['update_time']
            },
            "laoliu_evaluation": {
                "laoliu_score": stock['laoliu_score'],
                "analysis_points": stock['analysis_points'],
                "risk_warnings": stock['risk_warnings'],
                "investment_advice": stock['investment_advice']
            },
            "investment_summary": {
                "comprehensive_score": stock['laoliu_score'],
                "recommendation": stock['recommendation']
            }
        }
        analysis_results.append(analysis_result)
    
    analysis_data = {
        "total_count": len(analysis_results),
        "update_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "analysis_results": analysis_results
    }
    
    # 生成汇总数据
    summary_data = {
        "update_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "total_stocks": len(a_stocks) + len(hk_stocks),
        "a_stocks_count": len(a_stocks),
        "hk_stocks_count": len(hk_stocks),
        "markets": {
            "a_stocks": {"total": len(a_stocks)},
            "hk_stocks": {"total": len(hk_stocks)}
        }
    }
    
    # 保存文件
    print("保存数据文件...")
    
    with open("../stocks_a.json", 'w', encoding='utf-8') as f:
        json.dump(a_stock_data, f, ensure_ascii=False, indent=2)
    print(f"A股数据已保存: {len(a_stocks)} 只")
    
    with open("../stocks_hk.json", 'w', encoding='utf-8') as f:
        json.dump(hk_stock_data, f, ensure_ascii=False, indent=2)
    print(f"港股数据已保存: {len(hk_stocks)} 只")
    
    with open("../analysis_samples.json", 'w', encoding='utf-8') as f:
        json.dump(analysis_data, f, ensure_ascii=False, indent=2)
    print(f"分析样本已保存: {len(analysis_results)} 个")
    
    with open("../summary.json", 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
    print("汇总数据已保存")
    
    # 复制到小程序和static目录
    import shutil
    files = ["stocks_a.json", "stocks_hk.json", "analysis_samples.json", "summary.json"]
    
    for filename in files:
        try:
            shutil.copy2(f"../{filename}", f"../miniprogram/{filename}")
            shutil.copy2(f"../{filename}", f"../static_data/{filename}")
        except Exception as e:
            print(f"复制文件 {filename} 失败: {e}")
    
    print(f"\n数据生成完成!")
    print(f"A股: {len(a_stocks)} 只")
    print(f"港股: {len(hk_stocks)} 只")
    print(f"总计: {len(a_stocks) + len(hk_stocks)} 只")
    print("小程序现在可以搜索数千只股票!")

if __name__ == "__main__":
    main()