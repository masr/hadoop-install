from enum import Enum, unique


@unique
class SERVICE(Enum):
    JAVA = 0
    HADOOP = 1
    SPARK = 2
    ZOOKEEPER = 3
    HBASE = 4
    HIVE = 5
