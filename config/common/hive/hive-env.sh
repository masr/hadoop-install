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

# Set Hive and Hadoop environment variables here. These variables can be used
# to control the execution of Hive. It should be used by admins to configure
# the Hive installation (so that users do not have to set environment variables
# or set command line parameters to get correct behavior).
#
# The hive service being invoked (CLI/HWI etc.) is available via the environment
# variable SERVICE


# Hive Client memory usage can be an issue if a large number of clients
# are running at the same time. The flags below have been useful in
# reducing memory usage:
#
# if [ "$SERVICE" = "cli" ]; then
#   if [ -z "$DEBUG" ]; then
#     export HADOOP_OPTS="$HADOOP_OPTS -XX:NewRatio=12 -Xms10m -XX:MaxHeapFreeRatio=40 -XX:MinHeapFreeRatio=15 -XX:+UseParNewGC -XX:-UseGCOverheadLimit"
#   else
#     export HADOOP_OPTS="$HADOOP_OPTS -XX:NewRatio=12 -Xms10m -XX:MaxHeapFreeRatio=40 -XX:MinHeapFreeRatio=15 -XX:-UseGCOverheadLimit"
#   fi
# fi

# The heap size of the jvm stared by hive shell script can be controlled via:
#
# export HADOOP_HEAPSIZE=1024
#
# Larger heap size may be required when running queries over large number of files or partitions.
# By default hive shell scripts use a heap size of 256 (MB).  Larger heap size would also be
# appropriate for hive server (hwi etc).


# Set HADOOP_HOME to point to a specific hadoop install directory
HADOOP_HOME={{ install_base_dir }}/hadoop

# Hive Configuration Directory can be controlled by:
export HIVE_CONF_DIR={{ hadoop_confs_dir }}/hive/conf

# Folder containing extra ibraries required for hive compilation/execution can be controlled by:
export HIVE_AUX_JARS_PATH={{ install_base_dir }}/share/hadoop/common/lib/aws-java-sdk-*.jar

{% if s3_supported == "true" %}
if [ -f ${HIVE_CONF_DIR}/AWS_ACCESS_KEY_ID ];then
  export AWS_ACCESS_KEY_ID=$(cat ${HIVE_CONF_DIR}/AWS_ACCESS_KEY_ID)
fi
if [ -f ${HIVE_CONF_DIR}/AWS_SECRET_ACCESS_KEY ];then
  export AWS_SECRET_ACCESS_KEY=$(cat ${HIVE_CONF_DIR}/AWS_SECRET_ACCESS_KEY)
fi
{% endif %}

HIVE_LOG_DIR={{ hadoop_log_dir }}/hive

export HIVE_METASTORE_HADOOP_OPTS="-Xms{{ hivemetastore_heap }} -Xmx{{ hivemetastore_heap }} -XX:MaxNewSize={{ hivemetastore_young_heap }} -XX:NewSize={{ hivemetastore_young_heap }} \
-XX:+UseConcMarkSweepGC -XX:+UseParNewGC -XX:CMSInitiatingOccupancyFraction=75 -XX:+UseCMSCompactAtFullCollection \
-verbose:gc -XX:+PrintGCDetails -XX:+PrintGCDateStamps -XX:+PrintGCApplicationStoppedTime \
-Xloggc:${HIVE_LOG_DIR}/hivemetastore.gc.log \
-XX:+UseGCLogFileRotation -XX:NumberOfGCLogFiles=10 -XX:GCLogFileSize=100M \
-XX:MaxMetaspaceSize=512M \
-Dhive.root.logger=${HIVE_ROOT_LOGGER:-INFO,console} \
-Dhive.log.dir=${HIVE_LOG_DIR} \
-Dhive.log.file=hive-hivemetastore-${HOSTNAME}.log"