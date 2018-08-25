basepath=$(cd `dirname $0`;cd ..; pwd)
source $basepath/.virtualenv/bin/active
export PYTHONPATH=$basepath:$PYTHONPATH
(cd $basepath; python $basepath/hadoop_install/generator.py $@)
deactivate