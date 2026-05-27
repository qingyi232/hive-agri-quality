-- ============================================================
-- 农产品质量安全追溯与分析系统 - 数据导入脚本
-- 将CSV数据导入Hive表
-- ============================================================

USE agri_trace;

-- 导入产品基础信息
LOAD DATA LOCAL INPATH '/data/sample_products.csv' 
OVERWRITE INTO TABLE product_info;

-- 导入种植环节数据
LOAD DATA LOCAL INPATH '/data/planting_data.csv' 
OVERWRITE INTO TABLE planting_data;

-- 导入施肥记录
LOAD DATA LOCAL INPATH '/data/fertilizer_record.csv' 
OVERWRITE INTO TABLE fertilizer_record;

-- 导入用药记录
LOAD DATA LOCAL INPATH '/data/pesticide_record.csv' 
OVERWRITE INTO TABLE pesticide_record;

-- 导入加工环节数据
LOAD DATA LOCAL INPATH '/data/processing_data.csv' 
OVERWRITE INTO TABLE processing_data;

-- 导入运输环节数据
LOAD DATA LOCAL INPATH '/data/transport_data.csv' 
OVERWRITE INTO TABLE transport_data;

-- 导入运输温度监控数据
LOAD DATA LOCAL INPATH '/data/transport_temperature.csv' 
OVERWRITE INTO TABLE transport_temperature;

-- 导入销售环节数据
LOAD DATA LOCAL INPATH '/data/sales_data.csv' 
OVERWRITE INTO TABLE sales_data;

-- 导入企业信息
LOAD DATA LOCAL INPATH '/data/enterprise_info.csv' 
OVERWRITE INTO TABLE enterprise_info;

-- 导入预警记录
LOAD DATA LOCAL INPATH '/data/warning_record.csv' 
OVERWRITE INTO TABLE warning_record;

-- 验证数据导入
SELECT '产品信息表' as table_name, COUNT(*) as row_count FROM product_info
UNION ALL
SELECT '种植数据表', COUNT(*) FROM planting_data
UNION ALL
SELECT '施肥记录表', COUNT(*) FROM fertilizer_record
UNION ALL
SELECT '用药记录表', COUNT(*) FROM pesticide_record
UNION ALL
SELECT '加工数据表', COUNT(*) FROM processing_data
UNION ALL
SELECT '运输数据表', COUNT(*) FROM transport_data
UNION ALL
SELECT '温度监控表', COUNT(*) FROM transport_temperature
UNION ALL
SELECT '销售数据表', COUNT(*) FROM sales_data
UNION ALL
SELECT '企业信息表', COUNT(*) FROM enterprise_info
UNION ALL
SELECT '预警记录表', COUNT(*) FROM warning_record;

SELECT '数据导入完成！' as message;
