from enum import Enum, unique


@unique
class SERVICE(Enum):
    HADOOP = 0
    SPARK = 1
    ZOOKEEPER = 2
    HBASE = 3
    HIVE = 4

