# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Set Hadoop-specific environment variables here.

# The only required environment variable is JAVA_HOME.  All others are
# optional.  When running a distributed configuration it is best to
# set JAVA_HOME in this file, so that it is correctly defined on
# remote nodes.

# The java implementation to use.
export JAVA_HOME={%install_base_dir%}/java

# The jsvc implementation to use. Jsvc is required to run secure datanodes
# that bind to privileged ports to provide authentication of data transfer
# protocol.  Jsvc is not required if SASL is configured for authentication of
# data transfer protocol using non-privileged ports.
#export JSVC_HOME=${JSVC_HOME}

export HADOOP_LOG_DIR={%hadoop_log_dir%}/$USER

export HADOOP_CONF_DIR={%install_base_dir%}/confs/hadoop/conf

# Extra Java CLASSPATH elements.  Automatically insert capacity-scheduler.
for f in $HADOOP_HOME/contrib/capacity-scheduler/*.jar; do
  if [ "$HADOOP_CLASSPATH" ]; then
    export HADOOP_CLASSPATH=$HADOOP_CLASSPATH:$f
  else
    export HADOOP_CLASSPATH=$f
  fi
done

# The maximum amount of heap to use, in MB. Default is 1000.
#export HADOOP_HEAPSIZE=
#export HADOOP_NAMENODE_INIT_HEAPSIZE=""

# Enable extra debugging of Hadoop's JAAS binding, used to set up
# Kerberos security.
# export HADOOP_JAAS_DEBUG=true

# Extra Java runtime options.  Empty by default.
# For Kerberos debugging, an extended option set logs more invormation
# export HADOOP_OPTS="-Djava.net.preferIPv4Stack=true -Dsun.security.krb5.debug=true -Dsun.security.spnego.debug"
export HADOOP_OPTS="$HADOOP_OPTS -Djava.net.preferIPv4Stack=true"

# Command specific options appended to HADOOP_OPTS when specified
COMMON_DAEMON_OPTS="-XX:+UseConcMarkSweepGC -XX:+UseParNewGC -XX:CMSInitiatingOccupancyFraction=75 -XX:+UseCMSCompactAtFullCollection \
-verbose:gc -XX:+PrintGCDetails -XX:+PrintGCDateStamps -XX:+PrintGCApplicationStoppedTime \
-XX:+UseGCLogFileRotation -XX:NumberOfGCLogFiles=10 -XX:GCLogFileSize=100M \
-XX:MaxMetaspaceSize=512M \
-Dhadoop.root.logger=${HADOOP_ROOT_LOGGER:-INFO,RFA}"

export HADOOP_NAMENODE_OPTS="-Xms{%namenode_heap%} -Xmx{%namenode_heap%} -XX:MaxNewSize={%namenode_young_heap%} -XX:NewSize={%namenode_young_heap%} \
-Dhadoop.log.file=hadoop-hdfs-namenode-$HOSTNAME.log \
-Dhadoop.security.logger=${HADOOP_SECURITY_LOGGER:-INFO,RFAS} \
-Dhdfs.audit.logger=${HDFS_AUDIT_LOGGER:-INFO,DRFAAUDIT} \
-Dhadoop.hdfs.statechange.logger=${HDFS_STATECHANGE_LOGGER:-WARN,SCA} \
-Xloggc:${HADOOP_LOG_DIR}/hadoop-gc-namenode.log.`date +'%Y%m%d%H%M'` \
-XX:ErrorFile=${HADOOP_LOG_DIR}/hadoop-namenode-hs_err_pid.log \
$COMMON_DAEMON_OPTS \
$HADOOP_NAMENODE_OPTS"

export HADOOP_DATANODE_OPTS="-Xms{%datanode_heap%} -Xmx{%datanode_heap%}  -XX:MaxNewSize={%datanode_young_heap%} -XX:NewSize={%datanode_young_heap%} \
-Dhadoop.log.file=hadoop-hdfs-datanode-$HOSTNAME.log \
-Dhadoop.security.logger=${HADOOP_SECURITY_LOGGER:-ERROR,RFAS} \
-Xloggc:${HADOOP_LOG_DIR}/hadoop-gc-datanode.log.`date +'%Y%m%d%H%M'` \
-XX:ErrorFile=${HADOOP_LOG_DIR}/hadoop-datanode-hs_err_pid.log \
$COMMON_DAEMON_OPTS \
$HADOOP_DATANODE_OPTS"

export HADOOP_ZKFC_OPTS="-Xms{%zkfc_heap%} -Xmx{%zkfc_heap%}  -XX:MaxNewSize={%zkfc_young_heap%} -XX:NewSize={%zkfc_young_heap%} \
-Dhadoop.log.file=hadoop-hdfs-zkfc-$HOSTNAME.log \
-Xloggc:${HADOOP_LOG_DIR}/hadoop-gc-zkfc.log.`date +'%Y%m%d%H%M'` \
-XX:ErrorFile=${HADOOP_LOG_DIR}/hadoop-zkfc-hs_err_pid.log \
$COMMON_DAEMON_OPTS \
$HADOOP_ZKFC_OPTS"

export HADOOP_JOURNALNODE_OPTS="-Xms{%journalnode_heap%} -Xmx{%journalnode_heap%}  -XX:MaxNewSize={%journalnode_young_heap%} -XX:NewSize={%journalnode_young_heap%} \
-Dhadoop.log.file=hadoop-hdfs-journalnode-$HOSTNAME.log \
-Xloggc:${HADOOP_LOG_DIR}/hadoop-journalnode.log.`date +'%Y%m%d%H%M'` \
-XX:ErrorFile=${HADOOP_LOG_DIR}/hadoop-journalnode-hs_err_pid.log \
$COMMON_DAEMON_OPTS \
$HADOOP_JOURNALNODE_OPTS"

export HADOOP_SECONDARYNAMENODE_OPTS="-Dhadoop.security.logger=${HADOOP_SECURITY_LOGGER:-INFO,RFAS} -Dhdfs.audit.logger=${HDFS_AUDIT_LOGGER:-INFO,NullAppender} $HADOOP_SECONDARYNAMENODE_OPTS"

export HADOOP_NFS3_OPTS="$HADOOP_NFS3_OPTS"
export HADOOP_PORTMAP_OPTS="-Xmx512m $HADOOP_PORTMAP_OPTS"

# The following applies to multiple commands (fs, dfs, fsck, distcp etc)
export HADOOP_CLIENT_OPTS="-Xmx512m $HADOOP_CLIENT_OPTS"
#HADOOP_JAVA_PLATFORM_OPTS="-XX:-UsePerfData $HADOOP_JAVA_PLATFORM_OPTS"

# On secure datanodes, user to run the datanode as after dropping privileges.
# This **MUST** be uncommented to enable secure HDFS if using privileged ports
# to provide authentication of data transfer protocol.  This **MUST NOT** be
# defined if SASL is configured for authentication of data transfer protocol
# using non-privileged ports.
export HADOOP_SECURE_DN_USER=${HADOOP_SECURE_DN_USER}

# Where log files are stored.  $HADOOP_HOME/logs by default.
#export HADOOP_LOG_DIR=${HADOOP_LOG_DIR}/$USER

# Where log files are stored in the secure data environment.
export HADOOP_SECURE_DN_LOG_DIR=${HADOOP_LOG_DIR}/${HADOOP_HDFS_USER}

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
export HADOOP_PID_DIR={%hadoop_pid_dir%}
export HADOOP_SECURE_DN_PID_DIR=${HADOOP_PID_DIR}

# A string representing this instance of hadoop. $USER by default.
export HADOOP_IDENT_STRING=$USER