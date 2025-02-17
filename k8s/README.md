# Running your own Elastic Stack with Kubernetes

If you'd like to start Elastic with Kubernetes, you can use the provided
[manifest-elastic.yml](manifest-elastic.yml) file. This starts
Elasticsearch, Kibana, and APM Server and only requires Docker installed.

First, configure the Elastic stack:
```bash
kubectl apply -f manifest-elastic.yml
```

**Note**: For simplicity, this adds an Elastic Stack to the default namespace.
Commands after here are simpler due to this. If you want to choose a different
one, use `kubectl`'s `--namespace` flag!

Next, block until the whole stack is available. First install or changing the
Elastic Stack version can take a long time due to image pulling.
```bash
kubectl wait --for=condition=available --timeout=10m \
  deployment/elasticsearch \
  deployment/kibana \
  deployment/apm-server
```

Next, forward the kibana port:
```bash
kubectl port-forward service/kibana 5601:5601 &
```

Finally, you can view Kibana at http://localhost:5601/app/home#/

If asked for a username and password, use username: elastic and password: elastic.

Clean up when finished, like this:

```bash
kubectl delete -f manifest-elastic.yml
```
