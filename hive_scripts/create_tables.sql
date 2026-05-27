-- ============================================================
-- 农产品质量安全追溯与分析系统 - Hive数据仓库建表脚本
-- ============================================================

-- 创建数据库
CREATE DATABASE IF NOT EXISTS agri_trace;
USE agri_trace;

-- ============================================================
-- 1. 产品基础信息表
-- ============================================================
CREATE TABLE IF NOT EXISTS product_info (
    product_id STRING COMMENT '产品ID',
    trace_code STRING COMMENT '追溯码',
    product_name STRING COMMENT '产品名称',
    category STRING COMMENT '产品类别',
    batch_no STRING COMMENT '批次号',
    create_time TIMESTAMP COMMENT '创建时间',
    overall_qualified BOOLEAN COMMENT '整体是否合格'
)
COMMENT '产品基础信息表'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

-- ============================================================
-- 2. 种植环节数据表
-- ============================================================
CREATE TABLE IF NOT EXISTS planting_data (
    record_id STRING COMMENT '记录ID',
    product_id STRING COMMENT '产品ID',
    farm_name STRING COMMENT '种植基地名称',
    farm_location STRING COMMENT '基地位置',
    start_date DATE COMMENT '种植开始日期',
    end_date DATE COMMENT '种植结束日期',
    soil_ph DECIMAL(3,1) COMMENT '土壤pH值',
    temperature_range STRING COMMENT '温度范围',
    humidity_range STRING COMMENT '湿度范围',
    qualified BOOLEAN COMMENT '是否合格'
)
COMMENT '种植环节数据表'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

-- ============================================================
-- 3. 施肥记录表
-- ============================================================
CREATE TABLE IF NOT EXISTS fertilizer_record (
    record_id STRING COMMENT '记录ID',
    product_id STRING COMMENT '产品ID',
    fertilizer_name STRING COMMENT '肥料名称',
    fertilizer_type STRING COMMENT '肥料类型',
    amount STRING COMMENT '用量',
    apply_date DATE COMMENT '施肥日期',
    operator STRING COMMENT '操作人'
)
COMMENT '施肥记录表'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

-- ============================================================
-- 4. 用药记录表
-- ============================================================
CREATE TABLE IF NOT EXISTS pesticide_record (
    record_id STRING COMMENT '记录ID',
    product_id STRING COMMENT '产品ID',
    pesticide_name STRING COMMENT '农药名称',
    pesticide_type STRING COMMENT '农药类型',
    amount STRING COMMENT '用量',
    apply_date DATE COMMENT '用药日期',
    safety_interval INT COMMENT '安全间隔期(天)',
    compliant BOOLEAN COMMENT '是否合规'
)
COMMENT '用药记录表'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

-- ============================================================
-- 5. 加工环节数据表
-- ============================================================
CREATE TABLE IF NOT EXISTS processing_data (
    record_id STRING COMMENT '记录ID',
    product_id STRING COMMENT '产品ID',
    factory_name STRING COMMENT '加工厂名称',
    factory_location STRING COMMENT '工厂位置',
    process_date DATE COMMENT '加工日期',
    process_steps STRING COMMENT '加工工艺步骤',
    hygiene_score INT COMMENT '卫生评分',
    qualified BOOLEAN COMMENT '是否合格'
)
COMMENT '加工环节数据表'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

-- ============================================================
-- 6. 运输环节数据表
-- ============================================================
CREATE TABLE IF NOT EXISTS transport_data (
    record_id STRING COMMENT '记录ID',
    product_id STRING COMMENT '产品ID',
    company_name STRING COMMENT '物流公司',
    vehicle_no STRING COMMENT '车辆编号',
    start_date DATE COMMENT '运输开始日期',
    end_date DATE COMMENT '运输结束日期',
    required_temp_range STRING COMMENT '要求温度范围',
    qualified BOOLEAN COMMENT '是否合格'
)
COMMENT '运输环节数据表'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

-- ============================================================
-- 7. 运输温度监控表
-- ============================================================
CREATE TABLE IF NOT EXISTS transport_temperature (
    record_id STRING COMMENT '记录ID',
    transport_id STRING COMMENT '运输记录ID',
    record_time TIMESTAMP COMMENT '记录时间',
    temperature DECIMAL(4,1) COMMENT '温度值',
    is_normal BOOLEAN COMMENT '是否正常'
)
COMMENT '运输温度监控表'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

-- ============================================================
-- 8. 销售环节数据表
-- ============================================================
CREATE TABLE IF NOT EXISTS sales_data (
    record_id STRING COMMENT '记录ID',
    product_id STRING COMMENT '产品ID',
    channel STRING COMMENT '销售渠道',
    store_name STRING COMMENT '门店名称',
    store_location STRING COMMENT '门店位置',
    shelf_date DATE COMMENT '上架日期',
    price STRING COMMENT '售价',
    qualified BOOLEAN COMMENT '是否合格'
)
COMMENT '销售环节数据表'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

-- ============================================================
-- 9. 风险预警记录表
-- ============================================================
CREATE TABLE IF NOT EXISTS warning_record (
    warning_id STRING COMMENT '预警ID',
    product_id STRING COMMENT '产品ID',
    warning_level STRING COMMENT '预警级别(high/medium/low)',
    warning_type STRING COMMENT '预警类型',
    problem_stage STRING COMMENT '问题环节',
    description STRING COMMENT '问题描述',
    create_time TIMESTAMP COMMENT '创建时间',
    status STRING COMMENT '状态(pending/processing/resolved)'
)
COMMENT '风险预警记录表'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

-- ============================================================
-- 10. 企业信息表
-- ============================================================
CREATE TABLE IF NOT EXISTS enterprise_info (
    enterprise_id STRING COMMENT '企业ID',
    enterprise_name STRING COMMENT '企业名称',
    enterprise_type STRING COMMENT '企业类型',
    location STRING COMMENT '所在地',
    contact STRING COMMENT '联系方式',
    register_date DATE COMMENT '注册日期'
)
COMMENT '企业信息表'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

-- ============================================================
-- 创建视图：产品全流程追溯视图
-- ============================================================
CREATE VIEW IF NOT EXISTS v_product_trace AS
SELECT 
    p.product_id,
    p.trace_code,
    p.product_name,
    p.category,
    p.batch_no,
    pl.farm_name,
    pl.start_date as planting_start,
    pl.end_date as planting_end,
    pl.qualified as planting_qualified,
    pr.factory_name,
    pr.process_date,
    pr.hygiene_score,
    pr.qualified as processing_qualified,
    t.company_name as transport_company,
    t.start_date as transport_start,
    t.end_date as transport_end,
    t.qualified as transport_qualified,
    s.channel as sales_channel,
    s.store_name,
    s.shelf_date,
    s.qualified as sales_qualified,
    p.overall_qualified
FROM product_info p
LEFT JOIN planting_data pl ON p.product_id = pl.product_id
LEFT JOIN processing_data pr ON p.product_id = pr.product_id
LEFT JOIN transport_data t ON p.product_id = t.product_id
LEFT JOIN sales_data s ON p.product_id = s.product_id;

-- ============================================================
-- 打印完成信息
-- ============================================================
SELECT '数据仓库表创建完成！' as message;
