# -*- coding: utf-8 -*-
"""
农产品质量安全追溯与分析系统 - Spark质量分析脚本
功能：
1. 种植用药合规性分析
2. 加工卫生达标率分析
3. 运输温度异常检测
4. 各环节质量达标率统计
5. 风险预警生成
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import json

def create_spark_session():
    """创建Spark会话，连接Hive"""
    spark = SparkSession.builder \
        .appName("农产品质量安全分析") \
        .config("spark.sql.warehouse.dir", "/user/hive/warehouse") \
        .config("hive.metastore.uris", "thrift://hive-metastore:9083") \
        .enableHiveSupport() \
        .getOrCreate()
    return spark

def analyze_pesticide_compliance(spark):
    """
    分析种植用药合规性
    检查农药使用是否符合国家标准
    """
    print("=" * 50)
    print("分析种植用药合规性...")
    print("=" * 50)
    
    # 从Hive读取用药记录
    pesticide_df = spark.sql("""
        SELECT 
            product_id,
            pesticide_name,
            pesticide_type,
            amount,
            apply_date,
            safety_interval,
            compliant
        FROM agri_trace.pesticide_record
    """)
    
    # 统计合规率
    compliance_stats = pesticide_df.groupBy("compliant").count()
    
    total = pesticide_df.count()
    compliant_count = pesticide_df.filter(col("compliant") == True).count()
    compliance_rate = (compliant_count / total * 100) if total > 0 else 0
    
    print(f"总用药记录数: {total}")
    print(f"合规记录数: {compliant_count}")
    print(f"用药合规率: {compliance_rate:.2f}%")
    
    # 找出不合规的记录
    non_compliant = pesticide_df.filter(col("compliant") == False)
    print(f"\n不合规记录数: {non_compliant.count()}")
    
    return {
        "total_records": total,
        "compliant_count": compliant_count,
        "compliance_rate": compliance_rate
    }

def analyze_processing_hygiene(spark):
    """
    分析加工卫生达标率
    卫生评分>=90分为达标
    """
    print("\n" + "=" * 50)
    print("分析加工卫生达标率...")
    print("=" * 50)
    
    processing_df = spark.sql("""
        SELECT 
            product_id,
            factory_name,
            process_date,
            hygiene_score,
            qualified
        FROM agri_trace.processing_data
    """)
    
    total = processing_df.count()
    qualified_count = processing_df.filter(col("hygiene_score") >= 90).count()
    qualified_rate = (qualified_count / total * 100) if total > 0 else 0
    
    # 计算平均卫生评分
    avg_score = processing_df.agg(avg("hygiene_score")).collect()[0][0]
    
    print(f"总加工记录数: {total}")
    print(f"达标记录数: {qualified_count}")
    print(f"卫生达标率: {qualified_rate:.2f}%")
    print(f"平均卫生评分: {avg_score:.1f}")
    
    # 按工厂统计
    factory_stats = processing_df.groupBy("factory_name") \
        .agg(
            count("*").alias("record_count"),
            avg("hygiene_score").alias("avg_score")
        ) \
        .orderBy(desc("avg_score"))
    
    print("\n各工厂卫生评分排名:")
    factory_stats.show(10)
    
    return {
        "total_records": total,
        "qualified_count": qualified_count,
        "qualified_rate": qualified_rate,
        "avg_score": avg_score
    }

def analyze_transport_temperature(spark):
    """
    分析运输温度异常
    检测温度是否在要求范围内
    """
    print("\n" + "=" * 50)
    print("分析运输温度异常...")
    print("=" * 50)
    
    temp_df = spark.sql("""
        SELECT 
            t.record_id,
            t.transport_id,
            t.record_time,
            t.temperature,
            t.is_normal,
            td.required_temp_range
        FROM agri_trace.transport_temperature t
        JOIN agri_trace.transport_data td ON t.transport_id = td.record_id
    """)
    
    total = temp_df.count()
    normal_count = temp_df.filter(col("is_normal") == True).count()
    abnormal_count = total - normal_count
    normal_rate = (normal_count / total * 100) if total > 0 else 0
    
    print(f"总温度记录数: {total}")
    print(f"正常记录数: {normal_count}")
    print(f"异常记录数: {abnormal_count}")
    print(f"温度正常率: {normal_rate:.2f}%")
    
    # 找出异常温度记录
    if abnormal_count > 0:
        print("\n异常温度记录:")
        temp_df.filter(col("is_normal") == False).show(10)
    
    return {
        "total_records": total,
        "normal_count": normal_count,
        "abnormal_count": abnormal_count,
        "normal_rate": normal_rate
    }

def calculate_stage_qualified_rates(spark):
    """
    计算各环节质量达标率
    """
    print("\n" + "=" * 50)
    print("计算各环节质量达标率...")
    print("=" * 50)
    
    # 种植环节
    planting_df = spark.sql("SELECT qualified FROM agri_trace.planting_data")
    planting_total = planting_df.count()
    planting_qualified = planting_df.filter(col("qualified") == True).count()
    planting_rate = (planting_qualified / planting_total * 100) if planting_total > 0 else 0
    
    # 加工环节
    processing_df = spark.sql("SELECT qualified FROM agri_trace.processing_data")
    processing_total = processing_df.count()
    processing_qualified = processing_df.filter(col("qualified") == True).count()
    processing_rate = (processing_qualified / processing_total * 100) if processing_total > 0 else 0
    
    # 运输环节
    transport_df = spark.sql("SELECT qualified FROM agri_trace.transport_data")
    transport_total = transport_df.count()
    transport_qualified = transport_df.filter(col("qualified") == True).count()
    transport_rate = (transport_qualified / transport_total * 100) if transport_total > 0 else 0
    
    # 销售环节
    sales_df = spark.sql("SELECT qualified FROM agri_trace.sales_data")
    sales_total = sales_df.count()
    sales_qualified = sales_df.filter(col("qualified") == True).count()
    sales_rate = (sales_qualified / sales_total * 100) if sales_total > 0 else 0
    
    results = {
        "planting": {"total": planting_total, "qualified": planting_qualified, "rate": planting_rate},
        "processing": {"total": processing_total, "qualified": processing_qualified, "rate": processing_rate},
        "transport": {"total": transport_total, "qualified": transport_qualified, "rate": transport_rate},
        "sales": {"total": sales_total, "qualified": sales_qualified, "rate": sales_rate}
    }
    
    print(f"种植环节达标率: {planting_rate:.2f}%")
    print(f"加工环节达标率: {processing_rate:.2f}%")
    print(f"运输环节达标率: {transport_rate:.2f}%")
    print(f"销售环节达标率: {sales_rate:.2f}%")
    
    return results

def generate_risk_warnings(spark):
    """
    生成风险预警
    根据分析结果自动生成预警记录
    """
    print("\n" + "=" * 50)
    print("生成风险预警...")
    print("=" * 50)
    
    warnings = []
    
    # 检查农药不合规
    non_compliant_pesticide = spark.sql("""
        SELECT p.product_id, pr.pesticide_name, pr.apply_date
        FROM agri_trace.pesticide_record pr
        JOIN agri_trace.product_info p ON pr.product_id = p.product_id
        WHERE pr.compliant = false
    """)
    
    for row in non_compliant_pesticide.collect():
        warnings.append({
            "product_id": row.product_id,
            "level": "high",
            "type": "农药使用不合规",
            "stage": "种植环节",
            "description": f"使用农药 {row.pesticide_name} 不符合规定"
        })
    
    # 检查卫生评分不达标
    low_hygiene = spark.sql("""
        SELECT p.product_id, pr.factory_name, pr.hygiene_score
        FROM agri_trace.processing_data pr
        JOIN agri_trace.product_info p ON pr.product_id = p.product_id
        WHERE pr.hygiene_score < 90
    """)
    
    for row in low_hygiene.collect():
        warnings.append({
            "product_id": row.product_id,
            "level": "medium",
            "type": "加工卫生不达标",
            "stage": "加工环节",
            "description": f"工厂 {row.factory_name} 卫生评分 {row.hygiene_score} 低于90分"
        })
    
    # 检查运输温度异常
    temp_abnormal = spark.sql("""
        SELECT DISTINCT td.product_id, tt.temperature
        FROM agri_trace.transport_temperature tt
        JOIN agri_trace.transport_data td ON tt.transport_id = td.record_id
        WHERE tt.is_normal = false
    """)
    
    for row in temp_abnormal.collect():
        warnings.append({
            "product_id": row.product_id,
            "level": "medium",
            "type": "运输温度异常",
            "stage": "运输环节",
            "description": f"检测到异常温度 {row.temperature}℃"
        })
    
    print(f"生成预警数量: {len(warnings)}")
    for w in warnings[:5]:  # 只显示前5条
        print(f"  - [{w['level']}] {w['type']}: {w['description']}")
    
    return warnings

def trace_product(spark, trace_code):
    """
    追溯产品全流程信息
    """
    print("\n" + "=" * 50)
    print(f"追溯产品: {trace_code}")
    print("=" * 50)
    
    result = spark.sql(f"""
        SELECT *
        FROM agri_trace.v_product_trace
        WHERE trace_code = '{trace_code}'
    """)
    
    if result.count() > 0:
        result.show(truncate=False)
        return result.collect()[0].asDict()
    else:
        print("未找到该追溯码对应的产品")
        return None

def main():
    """主函数"""
    print("=" * 60)
    print("农产品质量安全追溯与分析系统 - Spark分析任务")
    print("=" * 60)
    
    # 创建Spark会话
    spark = create_spark_session()
    
    try:
        # 1. 种植用药合规性分析
        pesticide_result = analyze_pesticide_compliance(spark)
        
        # 2. 加工卫生达标率分析
        hygiene_result = analyze_processing_hygiene(spark)
        
        # 3. 运输温度异常检测
        temp_result = analyze_transport_temperature(spark)
        
        # 4. 各环节质量达标率统计
        stage_rates = calculate_stage_qualified_rates(spark)
        
        # 5. 生成风险预警
        warnings = generate_risk_warnings(spark)
        
        # 汇总结果
        summary = {
            "pesticide_compliance": pesticide_result,
            "processing_hygiene": hygiene_result,
            "transport_temperature": temp_result,
            "stage_qualified_rates": stage_rates,
            "warnings_count": len(warnings)
        }
        
        print("\n" + "=" * 60)
        print("分析完成！汇总结果:")
        print("=" * 60)
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        
    finally:
        spark.stop()

if __name__ == "__main__":
    main()
