# User for YARN daemons
export HADOOP_YARN_USER=yarn

# resolve links - $0 may be a softlink
export YARN_CONF_DIR={%install_base_dir%}/confs/hadoop/conf

# some Java parameters
export JAVA_HOME={%install_base_dir%}/java

JAVA=$JAVA_HOME/bin/java

# so that filenames w/ spaces are handled correctly in loops below
IFS=

export YARN_PID_DIR={% hadoop_pid_dir %}
export YARN_LOG_DIR={% hadoop_log_dir %}/yarn

if [ "$YARN_LOGFILE" = "" ]; then
  YARN_LOGFILE='yarn.log'
fi

# default policy file for service-level authorization
if [ "$YARN_POLICYFILE" = "" ]; then
  YARN_POLICYFILE="hadoop-policy.xml"
fi

JAVA_HEAP_MAX=-Xmx1000m
if [ "$YARN_HEAPSIZE" != "" ]; then
  JAVA_HEAP_MAX="-Xmx""$YARN_HEAPSIZE""m"
fi

#export YARN_RESOURCEMANAGER_HEAPSIZE=1000
#export YARN_TIMELINESERVER_HEAPSIZE=1000
#export YARN_NODEMANAGER_HEAPSIZE=1000

# restore ordinary behaviour
unset IFS


YARN_OPTS="$YARN_OPTS -Dhadoop.log.dir=$YARN_LOG_DIR"
YARN_OPTS="$YARN_OPTS -Dyarn.log.dir=$YARN_LOG_DIR"
YARN_OPTS="$YARN_OPTS -Dhadoop.log.file=$YARN_LOGFILE"
YARN_OPTS="$YARN_OPTS -Dyarn.log.file=$YARN_LOGFILE"
YARN_OPTS="$YARN_OPTS -Dyarn.home.dir=$YARN_COMMON_HOME"
YARN_OPTS="$YARN_OPTS -Dyarn.id.str=$YARN_IDENT_STRING"
YARN_OPTS="$YARN_OPTS -Dhadoop.root.logger=${YARN_ROOT_LOGGER:-INFO,console}"
YARN_OPTS="$YARN_OPTS -Dyarn.root.logger=${YARN_ROOT_LOGGER:-INFO,console}"
if [ "x$JAVA_LIBRARY_PATH" != "x" ]; then
  YARN_OPTS="$YARN_OPTS -Djava.library.path=$JAVA_LIBRARY_PATH"
fi
YARN_OPTS="$YARN_OPTS -Dyarn.policy.file=$YARN_POLICYFILE"

#YARN_OPTS="$YARN_OPTS -Dzookeeper.sasl.client.username=zookeeper -Djava.security.auth.login.config={%install_base_dir%}/confs/hadoop/conf/yarn_jaas.conf -Dzookeeper.sasl.client=true -Dzookeeper.sasl.clientconfig=Client"

export YARN_NODEMANAGER_OPTS="${YARN_OPTS}  -Xms{%nodemanager_heap%} -Xmx{%nodemanager_heap%} -XX:MaxMetaspaceSize=512M"

export YARN_RESOURCEMANAGER_OPTS="${YARN_OPTS} -Xms{%resource_manager_heap%} -Xmx{%resource_manager_heap%} -XX:MaxNewSize={%resource_manager_young_heap%} -XX:NewSize={%resource_manager_young_heap%} -XX:MaxMetaspaceSize=512M \
-XX:+UseConcMarkSweepGC -XX:+UseParNewGC -XX:CMSInitiatingOccupancyFraction=75 -XX:+UseCMSCompactAtFullCollection \
-verbose:gc -XX:+PrintGCDetails -XX:+PrintGCDateStamps -XX:+PrintGCApplicationStoppedTime \
-Xloggc:$YARN_LOG_DIR/hadoop-gc-rm.log.`date +'%Y%m%d%H%M'` \
-XX:+UseGCLogFileRotation -XX:NumberOfGCLogFiles=10 -XX:GCLogFileSize=100M \
-XX:ErrorFile=${YARN_LOG_DIR}/hadoop-rm-hs_err_pid.log \
-Dyarn.rm.appsummary.logger=INFO,RMSUMMARY \
-Djute.maxbuffer=5242880"

