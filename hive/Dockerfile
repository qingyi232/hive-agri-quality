FROM apache/hive:4.0.0

USER root

# 下载 MySQL JDBC 驱动
RUN apt-get update && apt-get install -y wget && \
    wget -O /opt/hive/lib/mysql-connector-j-8.0.33.jar https://repo1.maven.org/maven2/com/mysql/mysql-connector-j/8.0.33/mysql-connector-j-8.0.33.jar && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

USER hive
