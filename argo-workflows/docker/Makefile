argo-run:
	argo submit -n argo workflow.yaml -p 'workflow-input={"msg": "workflow run"}' --watch

argo-run-par:
	argo submit -n argo workflow-minio-dag.yaml --watch

docker-build:
	./docker/build.sh
