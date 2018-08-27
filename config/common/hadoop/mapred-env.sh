# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

export JAVA_HOME={% install_base_dir %}/java

#export HADOOP_JOB_HISTORYSERVER_HEAPSIZE=1000

export HADOOP_MAPRED_LOG_DIR="{% hadoop_log_dir %}/mapred" # Where log files are stored.  $HADOOP_MAPRED_HOME/logs by default.

export HADOOP_MAPRED_LOGFILE=hadoop-mapred-jobhistoryserver-${HOSTNAME}.log

export HADOOP_MAPRED_ROOT_LOGGER=${HADOOP_MAPRED_ROOT_LOGGER:-INFO,console}
export HADOOP_JHS_LOGGER=${HADOOP_JHS_LOGGER:-INFO,console} # Hadoop JobSummary logger.

export HADOOP_JOB_HISTORYSERVER_OPTS="-Xms{% jobhistoryserver_heap %} -Xmx{% jobhistoryserver_heap %} -XX:MaxNewSize={% jobhistoryserver_young_heap %} -XX:NewSize={% jobhistoryserver_young_heap %} \
-XX:+UseConcMarkSweepGC -XX:+UseParNewGC -XX:CMSInitiatingOccupancyFraction=75 -XX:+UseCMSCompactAtFullCollection \
-verbose:gc -XX:+PrintGCDetails -XX:+PrintGCDateStamps -XX:+PrintGCApplicationStoppedTime \
-XX:+UseGCLogFileRotation -XX:NumberOfGCLogFiles=10 -XX:GCLogFileSize=100M \
-XX:MaxMetaspaceSize=512M \
-Xloggc:${HADOOP_MAPRED_LOG_DIR}/hadoop-gc-jobhistoryserver.log \
-XX:ErrorFile=${HADOOP_MAPRED_LOG_DIR}/hadoop-jobhistoryserver-hs_err_pid.log"

export HADOOP_MAPRED_PID_DIR={% hadoop_pid_dir %} The pid files are stored. /tmp by default.
#export HADOOP_MAPRED_IDENT_STRING= #A string representing this instance of hadoop. $USER by default
#export HADOOP_MAPRED_NICENESS= #The scheduling priority for daemons. Defaults to 0.
