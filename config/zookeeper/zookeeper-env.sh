export JAVA_HOME={% install_base_dir %}/java
export ZOOKEEPER_HOME={% install_base_dir %}/zookeeper
export ZOO_LOG_DIR={% hadoop_log_dir %}/zookeeper
export ZOOPIDFILE={% hadoop_pid_dir %}/zookeeper_server.pid
export SERVER_JVMFLAGS=-Xmx{% zookeeper_heap %}
export JAVA=$JAVA_HOME/bin/java
