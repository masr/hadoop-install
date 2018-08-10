export JAVA_HOME={%install_base_dir%}/java

export HADOOP_LOG_DIR={%hadoop_log_dir%}/$USER

export HADOOP_CONF_DIR={%install_base_dir%}/confs/hadoop/conf

# Extra Java runtime options.  Empty by default.
export HADOOP_OPTS="$HADOOP_OPTS -Djava.net.preferIPv4Stack=true"

# Command specific options appended to HADOOP_OPTS when specified
export HADOOP_NAMENODE_OPTS="-Xms{%namenode_heap%} -Xmx{%namenode_heap%} -XX:MaxNewSize={%namenode_young_heap%} -XX:NewSize={%namenode_young_heap%} -XX:MaxMetaspaceSize=512M $HADOOP_NAMENODE_OPTS \
-XX:+UseConcMarkSweepGC -XX:+UseParNewGC -XX:CMSInitiatingOccupancyFraction=75 -XX:+UseCMSCompactAtFullCollection \
-verbose:gc -XX:+PrintGCDetails -XX:+PrintGCDateStamps -XX:+PrintGCApplicationStoppedTime \
-Xloggc:${HADOOP_LOG_DIR}/hadoop-gc-namenode.log.`date +'%Y%m%d%H%M'` \
-XX:+UseGCLogFileRotation -XX:NumberOfGCLogFiles=10 -XX:GCLogFileSize=100M \
-XX:ErrorFile=${HADOOP_LOG_DIR}/hadoop-namenode-hs_err_pid.log \
-Dhdfs.audit.logger=INFO,DRFAAUDIT -Dhadoop.hdfs.statechange.logger=WARN,SCA"

export HADOOP_DATANODE_OPTS="-Xms{%datanode_heap%} -Xmx{%datanode_heap%} -Dhadoop.security.logger=ERROR,RFAS $HADOOP_DATANODE_OPTS"

export HADOOP_SECONDARYNAMENODE_OPTS="-Dhadoop.security.logger=${HADOOP_SECURITY_LOGGER:-INFO,RFAS} -Dhdfs.audit.logger=${HDFS_AUDIT_LOGGER:-INFO,NullAppender} $HADOOP_SECONDARYNAMENODE_OPTS"

# The following applies to multiple commands (fs, dfs, fsck, distcp etc)
export HADOOP_CLIENT_OPTS="-Xmx2048m $HADOOP_CLIENT_OPTS"

# On secure datanodes, user to run the datanode as after dropping privileges.
# This **MUST** be uncommented to enable secure HDFS if using privileged ports
# to provide authentication of data transfer protocol.  This **MUST NOT** be
# defined if SASL is configured for authentication of data transfer protocol
# using non-privileged ports.
#export HADOOP_SECURE_DN_USER=${HADOOP_SECURE_DN_USER}

# Where log files are stored in the secure data environment.
export HADOOP_SECURE_DN_LOG_DIR=${HADOOP_LOG_DIR}/$USER

###
# HDFS Mover specific parameters
###
# Specify the JVM options to be used when starting the HDFS Mover.
# These options will be appended to the options specified as HADOOP_OPTS
# and therefore may override any similar flags set in HADOOP_OPTS
#
# export HADOOP_MOVER_OPTS=""

###
# Advanced Users Only!
###

# The directory where pid files are stored. /tmp by default.
# NOTE: this should be set to a directory that can only be written to by
#       the user that will run the hadoop daemons.  Otherwise there is the
#       potential for a symlink attack.
#export HADOOP_PID_DIR=${HADOOP_PID_DIR}
export HADOOP_PID_DIR={%hadoop_pid_dir%}

export HADOOP_SECURE_DN_PID_DIR=${HADOOP_PID_DIR}

# A string representing this instance of hadoop. $USER by default.
export HADOOP_IDENT_STRING=$USER
export JAVA_LIBRARY_PATH={%install_base_dir%}/hadoop/lib/native:{%install_base_dir%}/hadoop/lib/native/Linux-amd64-64:{%install_base_dir%}/hadoop/lib/native/Linux-amd64-64/lib