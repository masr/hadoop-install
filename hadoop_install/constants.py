from enum import Enum, unique


@unique
class SERVICE(Enum):
    NIL = "nil"
    JAVA = "java"
    HADOOP = "hadoop"
    SPARK = "spark"
    ZOOKEEPER = "zookeeper"
    HBASE = "hbase"
    HIVE = "hive"

    def to_name(self):
        return str(self.name).lower()


@unique
class ROLE(Enum):
    ZOOKEEPER = "zookeeper"
    ZOOKEEPER_CLI = "zookeeper_cli"
    NAMENODE = "namenode"
    ZKFC = "zkfc"
    JOURNALNODE = "journalnode"
    DATANODE = "datanode"
    RESOURCEMANAGER = "resourcemanager"
    NODEMANAGER = "nodemanager"
    HADOOP_CLI = "hadoop_cli"
    SPARKHISTORYSERVER = "sparkhistoryserver"
    SPARK_CLI = "spark_cli"
    HIVEMETASTORE = "hivemetastore"
    HIVE_CLI = "hive_cli"
    HBASEMASTER = "hbasemaster"
    REGIONSERVER = "regionserver"
    HBASE_CLI = "hbase_cli"


SERVICE_TO_ROLES = {
    SERVICE.NIL: [],
    SERVICE.JAVA: [],
    SERVICE.HADOOP: [ROLE.NAMENODE, ROLE.DATANODE, ROLE.JOURNALNODE, ROLE.ZKFC, ROLE.RESOURCEMANAGER, ROLE.NODEMANAGER,
                     ROLE.HADOOP_CLI],
    SERVICE.ZOOKEEPER: [ROLE.ZOOKEEPER, ROLE.ZOOKEEPER_CLI],
    SERVICE.SPARK: [ROLE.SPARKHISTORYSERVER, ROLE.SPARK_CLI],
    SERVICE.HBASE: [ROLE.HBASEMASTER, ROLE.REGIONSERVER, ROLE.HBASE_CLI],
    SERVICE.HIVE: [ROLE.HIVEMETASTORE, ROLE.HIVE_CLI]
}

ALL_ROLE_NAMES = [v for k, v in ROLE.__members__.items()]
