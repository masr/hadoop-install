from enum import Enum, unique


@unique
class SERVICE(Enum):
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
    COMMON = "common"
    ZOOKEEPER_SERVER = "zookeeper_server"
    ZOOKEEPER_CLI = "zookeeper_cli"
    NAMENODE = "namenode"
    ZKFC = "zkfc"
    JOURNALNODE = "journalnode"
    DATANODE = "datanode"
    RESOURCE_MANAGER = "resource_manager"
    NODEMANAGER = "nodemanager"
    HADOOP_CLI = "hadoop_cli"
    SPARK_HISTORY_SERVER = "spark_history_server"
    SPARK_CLI = "spark_cli"
    HIVE_METASTORE = "hive_metastore"
    HIVE_CLI = "hive_cli"
    HBASE_MASTER = "hbase_master"
    REGIONSERVER = "regionserver"
    HBASE_CLI = "hbase_cli"


SERVICE_TO_ROLES = {
    SERVICE.JAVA: [ROLE.COMMON],
    SERVICE.HADOOP: [ROLE.NAMENODE, ROLE.DATANODE, ROLE.JOURNALNODE, ROLE.ZKFC, ROLE.RESOURCE_MANAGER, ROLE.NODEMANAGER,
                     ROLE.HADOOP_CLI],
    SERVICE.ZOOKEEPER: [ROLE.ZOOKEEPER_SERVER, ROLE.ZOOKEEPER_CLI],
    SERVICE.SPARK: [ROLE.SPARK_HISTORY_SERVER, ROLE.SPARK_CLI],
    SERVICE.HBASE: [ROLE.HBASE_MASTER, ROLE.REGIONSERVER, ROLE.HBASE_CLI],
    SERVICE.HIVE: [ROLE.HIVE_METASTORE, ROLE.HIVE_CLI]
}

ALL_ROLE_NAMES = [v for k, v in ROLE.__members__.items()]
