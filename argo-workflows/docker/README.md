### Argo Workflows

```bash
$ argo submit -n argo workflow.yaml -p 'workflow-input={"msg": "workflow run"}' --watch
$ argo submit -n argo workflow-minio.yaml --watch
$ argo submit -n argo workflow-minio-dag.yaml --watch
```

