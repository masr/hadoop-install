export JAVA_HOME={% install_base_dir %}/java
export ZOOKEEPER_HOME={% install_base_dir %}/zookeeper
export ZOO_LOG_DIR={% hadoop_log_dir %}/zookeeper
export ZOOPIDFILE={% hadoop_pid_dir %}/zookeeper.pid
export SERVER_JVMFLAGS="-Xms{% zookeeper_heap %} -Xmx{% zookeeper_heap %} -XX:MaxNewSize={%zookeeper_young_heap%} -XX:NewSize={%zookeeper_young_heap%} \
-XX:+UseConcMarkSweepGC -XX:+UseParNewGC -XX:CMSInitiatingOccupancyFraction=75 -XX:+UseCMSCompactAtFullCollection \
-verbose:gc -XX:+PrintGCDetails -XX:+PrintGCDateStamps -XX:+PrintGCApplicationStoppedTime \
-Xloggc:${ZOO_LOG_DIR}/zookeeper.gc.log \
-XX:+UseGCLogFileRotation -XX:NumberOfGCLogFiles=10 -XX:GCLogFileSize=100M \
-XX:MaxMetaspaceSize=512M \
-Dzookeeper.root.logger=${ZOO_LOG4J_PROP:-INFO,console} \
-Dzookeeper.log.dir={% hadoop_log_dir %}/zookeeper \
-Dzookeeper.log.file=zookeeper-$HOSTNAME.log"


export JAVA=$JAVA_HOME/bin/java
export JVMFLAGS="-Djute.maxbuffer=5242880"