#!/bin/bash

args=("$@")

spark_args=()

while [ "$1" != "" ]; do
        case $1 in
        --master) 	spark_args+=($1 $2)
			shift
                        master_url=$1
                        ;;
        --callback_url) shift
                        callback_url=$1
                        ;;
        --conf) 	spark_args+=($1 $2)
			shift
			if [[ "$1" =~ spark.kubernetes.driver.pod.name* ]]
			then
			driver_pod_name=$(echo $1 | awk -F "=" '{print($2)}')
			elif [[ "$1" =~ spark.kubernetes.namespace* ]]
			then
			k8s_namespace=$(echo $1 | awk -F "=" '{print($2)}')
			fi
                        ;;
        * ) spark_args+=($1)
                        ;;
        esac
        shift
done

spark_args_string=$(IFS=" " ; echo "${spark_args[*]}")
echo $spark_args_string
echo $k8s_namespace
echo $driver_pod_name
echo $master_url

header="Content-Type:application/json"

if [[ -z "$k8s_namespace" ]] ||  [[ -z "$driver_pod_name" ]]  || [[ -z "$master_url" ]]
then
	echo "Required parameters are not set, please check namespace, driver_pod_name or cluster URL settings"
	#curl --location --request POST $callback_url --header $header --data-raw '{"Output":{"Return Message":"Required parameters are not set, please check namespace, driver_pod_name or cluster URL settings"}, "StatusCode": 400}'
	exit 1
else
	echo "All set, moving forward"
fi

$SPARK_HOME/bin/spark-submit $spark_args_string

exit_code_res=$($SPARK_HOME/bin/spark-submit --status $k8s_namespace:$driver_pod_name --master $master_url 2>&1 | awk '/exit code/{print $3;exit}')

echo "Exit code is" $exit_code_res
if [[ $exit_code_res == "0" ]]
then
	#curl --location --request POST $callback_url --header $header --data-raw '{"Output":{"Return Message":"Job finished successfully, driver pod name: '$driver_pod_name'"}, "StatusCode": 200}'
	exit 0
else
	#curl --location --request POST $callback_url --header $header --data-raw '{"Output":{"Return Message":"Job failed, driver pod name: '$driver_pod_name'"}, "StatusCode": 200}'
	exit 1
fi
