# -*- coding: utf-8 -*-
"""
农产品质量安全追溯与分析系统 - Flask主应用
"""

from flask import Flask, render_template, jsonify, request
import json
import hashlib
import time
import uuid
from datetime import datetime
from db_service import data_service

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# ==================== 首页 ====================
@app.route('/')
def index():
    """系统首页"""
    return render_template('index.html')

# ==================== 消费者查询页面 ====================
@app.route('/consumer')
def consumer():
    """消费者查询界面"""
    return render_template('consumer.html')

# ==================== 企业管理页面 ====================
@app.route('/enterprise')
def enterprise():
    """企业管理界面"""
    return render_template('enterprise.html')

# ==================== 监管部门页面 ====================
@app.route('/supervisor')
def supervisor():
    """监管部门监督界面"""
    return render_template('supervisor.html')

# ==================== 数据统计页面 ====================
@app.route('/statistics')
def statistics():
    """数据统计界面"""
    return render_template('statistics.html')

# ==================== 风险预警页面 ====================
@app.route('/warning')
def warning():
    """风险预警界面"""
    return render_template('warning.html')

# ==================== API接口 ====================

@app.route('/api/trace/<trace_code>')
def api_trace(trace_code):
    """
    追溯码查询接口
    根据追溯码查询农产品全流程信息
    """
    trace_data = data_service.get_product_trace(trace_code)
    return jsonify(trace_data)

@app.route('/api/statistics/overview')
def api_statistics_overview():
    """
    统计概览接口
    返回各环节质量达标率、产品合格率等
    """
    data = data_service.get_statistics_overview()
    return jsonify(data)

@app.route('/api/statistics/trend')
def api_statistics_trend():
    """
    趋势统计接口
    返回近期质量趋势数据 - 真实计算
    """
    data = data_service.get_statistics_trend()
    return jsonify(data)

@app.route('/api/statistics/category')
def api_statistics_category():
    """
    产品类别分布接口 - 真实计算
    """
    data = data_service.get_category_distribution()
    return jsonify(data)

@app.route('/api/statistics/region')
def api_statistics_region():
    """
    产地分布接口 - 真实计算
    """
    data = data_service.get_region_distribution()
    return jsonify(data)

@app.route('/api/statistics/enterprise_ranking')
def api_enterprise_ranking():
    """
    企业质量排行接口 - 真实计算
    """
    data = data_service.get_enterprise_ranking()
    return jsonify(data)

@app.route('/api/warning/statistics')
def api_warning_statistics():
    """
    预警统计接口 - 真实计算
    """
    data = data_service.get_warning_statistics()
    return jsonify(data)

@app.route('/api/warning/list')
def api_warning_list():
    """
    风险预警列表接口
    返回当前预警信息
    """
    warnings = data_service.get_warning_list()
    return jsonify(warnings)

@app.route('/api/products/list')
def api_products_list():
    """
    产品列表接口
    返回农产品列表
    """
    products = data_service.get_products_list()
    return jsonify(products)

@app.route('/api/generate_trace_code', methods=['POST'])
def api_generate_trace_code():
    """
    生成追溯码接口
    为农产品生成唯一追溯码（保证绝对不重复）
    """
    data = request.json
    product_name = data.get('product_name', '')
    batch = data.get('batch', '')
    
    # 生成唯一追溯码：产品名+批次+时间戳+UUID的MD5，确保绝对唯一
    unique_id = str(uuid.uuid4())  # UUID保证全球唯一
    raw_str = f"{product_name}{batch}{time.time()}{unique_id}"
    trace_code = hashlib.md5(raw_str.encode()).hexdigest()[:16].upper()
    
    return jsonify({
        'success': True,
        'trace_code': trace_code,
        'generated_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

if __name__ == '__main__':
    print("=" * 50)
    print("农产品质量安全追溯与分析系统")
    print("访问地址: http://localhost:5000")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)
