# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# 老刘投资决策程序 - WeChat Mini Program Investment System

## Project Overview
A stock investment decision support system based on "老刘" (Lao Liu)'s handwritten investment notes, delivered as a WeChat Mini Program. Uses OCR processing, Python data analysis, and static JSON hosting via GitHub Pages.

## Essential Commands

### Primary Data Generation
```bash
# Main command to generate all investment data
cd data_processor && python3 main.py

# Install dependencies
pip install -r requirements.txt

# Validate generated data
python -m json.tool summary.json
```

### OCR Processing Pipeline
```bash
# Process handwritten investment notes (27 images)
python complete_ocr_processor.py
python extract_quotes.py  # Extract investment quotes

# Validate OCR results
python -m json.tool static_data/laoliu_quotes.json
```

### WeChat Mini Program Development
```bash
# Open miniprogram/ in WeChat Developer Tools
# AppID: wx2aad9cd988058c1f
# Preview: Scan QR for testing
# Upload: For release submission

# Validate mini program structure
find miniprogram/pages -name "*.wxml" -o -name "*.wxss" -o -name "*.js"
```

### Deployment
```bash
# Full deployment workflow
cd data_processor && python3 main.py
git add *.json static_data/
git commit -m "update investment data"
git push origin master

# Verify deployment
curl -I https://vileo06.github.io/investliu/summary.json
```

## High-Level Architecture

### System Flow
```
Handwritten Notes → OCR Processing → Python Analysis → Static JSON → GitHub Pages → WeChat Mini Program
```

### Core Components

#### 1. Data Processing Layer (`data_processor/`)
- **`main.py`**: Primary orchestrator - runs complete data generation workflow
- **`stock_analyzer.py`**: Four-dimensional scoring (Valuation + Growth + Profitability + Safety)
- **`laoliu_analyzer.py`**: Implements Lao Liu's investment philosophy and rules
- **`stock_data_fetcher.py`**: Stock data retrieval with mock data support
- **`rule_extractor.py`**: Investment rule extraction from OCR text

#### 2. OCR Processing (Root scripts)
- **`complete_ocr_processor.py`**: Processes 27 investment notebook images
- **`extract_quotes.py`**: Extracts investment quotes into structured JSON
- **`structure_analyzer.py`**: Converts OCR text into structured investment rules

#### 3. WeChat Mini Program (`miniprogram/`)
- **`app.js`**: Global config with API wrapper, retry mechanism, caching
- **Pages**: index, stocks, analysis, portfolio, settings
- **`components/quote-card/`**: Reusable quote display with sharing
- **`utils/shareCard.js`**: Canvas-based share card generator

#### 4. Data Architecture
- **Static JSON files**: Hosted on GitHub Pages for free
- **API Base URL**: https://vileo06.github.io/investliu/
- **Caching**: 1-hour local cache with auto-refresh
- **Data Files**: summary.json, stocks_a.json, stocks_hk.json, market_timing.json

## Key Development Patterns

### Investment Analysis Algorithm
```python
# Four-dimensional scoring model (stock_analyzer.py)
total_score = (valuation_score * 0.25 + 
               growth_score * 0.25 + 
               profitability_score * 0.25 + 
               safety_score * 0.25) * industry_weight
```

### UI Design System (Modern Financial Theme)
- **Color Scheme**: Primary gradient `linear-gradient(135deg, #667eea 0%, #764ba2 100%)`
- **Key CSS Classes**: `.card`, `.btn-primary`, `.tag-success`, `.stock-item`
- **TabBar**: Modern design with scale effects, gradient indicators, glass morphism
- **Animations**: `.fade-in`, `.slide-up`, `.bounce`

### Data Update Workflow
1. Run `cd data_processor && python3 main.py` to generate latest data
2. JSON files output to both `static_data/` and project root
3. Commit and push to GitHub triggers Pages auto-deployment
4. Mini program auto-fetches updated data on next launch

### WeChat Mini Program Configuration
- **AppID**: wx2aad9cd988058c1f
- **API Base**: https://vileo06.github.io/investliu/
- **Caching Strategy**: 1-hour local cache with retry mechanism
- **Error Handling**: Automatic retry (2 attempts), graceful degradation

## Important Configuration

### Required Dependencies
```txt
requests==2.31.0
pandas==2.0.3
baidu-aip==4.16.13          # OCR processing
tencentcloud-sdk-python==3.0.944
akshare==1.11.80            # Stock data APIs
```

### GitHub Pages Setup
- **Repository**: ViLeo06/investliu
- **Branch**: master
- **URL**: https://vileo06.github.io/investliu/

## Debugging Commands

```bash
# Test Python data generation
cd data_processor && python3 -c "import main; print('Import successful')"

# Validate JSON format
python3 -m json.tool summary.json > /dev/null && echo "JSON valid"

# Test GitHub Pages accessibility
curl -f https://vileo06.github.io/investliu/summary.json

# Check mini program file structure
find miniprogram/pages -name "*.wxml" -o -name "*.wxss" -o -name "*.js"
```

## Release Process
Use `docs/release_checklist.md` for comprehensive pre-release validation including:
- Function testing across all pages
- Data validation and API response checks
- UI/UX verification and performance testing
- Security and compliance checks for financial applications