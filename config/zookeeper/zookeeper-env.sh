export JAVA_HOME={% install_base_dir %}/java
export ZOOKEEPER_HOME={% install_base_dir %}/zookeeper
export ZOO_LOG_DIR={% hadoop_log_dir %}/zookeeper
export ZOOPIDFILE={% hadoop_pid_dir %}/zookeeper.pid
export SERVER_JVMFLAGS="-Xms{% zookeeper_heap %} -Xmx{% zookeeper_heap %} -verbose:gc -XX:+PrintGCDetails -XX:+PrintGCDateStamps -Xloggc:${ZOO_LOG_DIR}/zookeeper.gc.`date +'%Y%m%d%H%M'`"
export ZOO_LOG4J_PROP=INFO,ROLLINGFILE
export ZOO_LOG_FILE=zookeeper-%H.log
export JAVA=$JAVA_HOME/bin/java
export JVMFLAGS="-Djute.maxbuffer=5242880"