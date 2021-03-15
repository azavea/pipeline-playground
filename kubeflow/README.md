# K8S & Kubeflow local installation and run instructions

If you don't want to go through the entire README doc below:

## Short run instructions

```bash
# start local k8s cluster
$ minikube start

# install kubeflow
$ export PIPELINE_VERSION=1.4.1
$ kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"
$ kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io
$ kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/env/platform-agnostic-pns?ref=$PIPELINE_VERSION"
# expose UI to localhost:8080
$ kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80
# install Kubeflow DSL
$ pip3 install kfp
$ cd kubeflow/pipeline;
# set AWS credentials
$ kubectl create -f aws_secrets.yaml
# generate pipeline
$ python3 <path to pipeline python file>
```

Import the generated pipeline (press the `Upload the Pipeline` button):

<img width="1428" alt="image" src="https://user-images.githubusercontent.com/4929546/109371866-c913f580-7874-11eb-938b-286104d2ca78.png">

Execute it (press the `Create Run` button):

<img width="1164" alt="image" src="https://user-images.githubusercontent.com/4929546/109372019-56574a00-7875-11eb-824d-b3fc1c15a3dc.png">

## Extended Installation instructions

1. CLI to interact with K8S:
    * [Kubectl Installation](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
      * For instance via brew: `brew install kubectl`
      * [Autocompletion instructions and a Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)

2. [Minukube](https://minikube.sigs.k8s.io/docs/start/)
    * [Alternatives](https://kubernetes.io/docs/tasks/tools/):
        * [kind](https://kind.sigs.k8s.io/docs/user/quick-start/) - more to run several nodes on a single machine.
        * [k0s](https://github.com/k0sproject/k0s) - cool, but requires some extra research.
    * For instance via brew `brew install minikube`.

    ```bash
    $ minikube start
    $ kubectl get po -A # access the cluster
    ```

3. Use [Lens.app](https://github.com/lensapp/lens) to get access to the minikube cluster

    <img width="1433" alt="image" src="https://user-images.githubusercontent.com/4929546/109369004-e80c8a80-7868-11eb-857e-53f9756da872.png">

    * It allows to inspect K8S cluster running containers, secrets, etc.

4. (optional) Working with a bare K8S clusterrequires us to use Helm charts to deploy apps. However, for testing purposes, it is possible to convert exsiting docker-compose files via the [kompose](https://kubernetes.io/docs/tasks/configure-pod-container/translate-compose-kubernetes/) util into k8s comptaible docker-compose files.

5. K8S Local port forwarding instructions:
    * [https://kubernetes.io/docs/tasks/access-application-cluster/port-forward-access-application-cluster/#forward-a-local-port-to-a-port-on-the-pod](https://kubernetes.io/docs/tasks/access-application-cluster/port-forward-access-application-cluster/#forward-a-local-port-to-a-port-on-the-pod)

6. Kubeflow
    * [Local Cluster Deployment](https://www.kubeflow.org/docs/pipelines/installation/localcluster-deployment/)
        ```bash
        # env/platform-agnostic-pns hasn't been publically released, so you will install it from master
        export PIPELINE_VERSION=1.4.1
        kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"
        kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io
        kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/env/platform-agnostic-pns?ref=$PIPELINE_VERSION"
        ```
    * Kubeflow UI port forwarding: `kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80`

7. Images published locally are not accesible within the K8S cluster. [docker-env](https://minikube.sigs.k8s.io/docs/commands/docker-env/) is used to build images accesible to minikube: run `eval $(minikube docker-env)` and build images after running this command.

8. To start writing DSL you'd need to install [Kubeflow SDK](https://www.kubeflow.org/docs/pipelines/sdk/install-sdk/)
    * `pip3 install kfp`

9. KFP DSL allows to describe the Pipeline, which can be compiled into the yaml file [via the kfp.compiler.Compiler().compile](https://kubeflow-pipelines.readthedocs.io/en/stable/source/kfp.compiler.html). Such file can be imported through the UI. Alternatively this Pipeline can be launched without UI, directly [through the kfp.Client](https://kubeflow-pipelines.readthedocs.io/en/stable/source/kfp.client.html#kfp.Client.run_pipeline)

9. AWS Access:
    * Apps launched within the K8S cluster should have credentials set.
    * The idiomatic way is to set [K8S secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
    * For instance fill the [aws_secrets.yaml](./aws_secrets.yaml) file and run `kubectl create -f aws_secrets.yaml`
        * All secrets are Base64 encoded strings
    * You may need to run `kubectl -n kubeflow create -f aws_secrets.yaml`. Without specifying the `kubeflow` namespace you may get an error when running the pipeline: "CreateContainerConfigError: secret "aws-secrets" not found".
    * Kubeflow DSL has a special syntax to tell task to use credenitals `kubernetes.client.models.V1EnvFromSource`
