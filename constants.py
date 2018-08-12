from enum import Enum, unique


@unique
class SERVICE(Enum):
    JAVA = 0
    HADOOP = 1
    SPARK = 2
    ZOOKEEPER = 3
    HBASE = 4
    HIVE = 5


SERVICE_TO_ROLES = {
    SERVICE.JAVA: ['common'],
    SERVICE.HADOOP: ['namenode', 'datanode', 'journal_node', 'zkfc', 'resource_manager', 'nodemanager', 'hadoop_cli'],
    SERVICE.ZOOKEEPER: ['zookeeper_server', 'zookeeper_cli']
}

ALL_ROLES = SERVICE_TO_ROLES[SERVICE.ZOOKEEPER] + SERVICE_TO_ROLES[SERVICE.HADOOP]
