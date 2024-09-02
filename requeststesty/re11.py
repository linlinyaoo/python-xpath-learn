from pyspark.sql import SparkSession

# 初始化 SparkSession
spark = SparkSession.builder.appName("DeduplicateByTtAcrossSources").getOrCreate()

# 读取第一个数据源并去重
df1 = spark.read.json("hdfs://path_to_first_file").dropDuplicates(["tt"])

# 读取第二个数据源并去重
df2 = spark.read.json("hdfs://path_to_second_file").dropDuplicates(["tt"])

# 展示每个数据源的去重结果
print("Data source 1 (after deduplication):")
df1.show(truncate=False)

print("Data source 2 (after deduplication):")
df2.show(truncate=False)

# 合并数据源并进行全局去重
merged_df = df1.union(df2)  # 合并数据源
global_dedup_df = merged_df.dropDuplicates(["tt"])  # 全局去重

# 展示全局去重后的结果
print("Global deduplication result:")
global_dedup_df.select("tt", "url").show(truncate=False)
