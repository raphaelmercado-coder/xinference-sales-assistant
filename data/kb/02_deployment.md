# Xinference: Deployment

You can install Xinference with pip and start a local instance with a single command,
which launches a supervisor and worker and serves an endpoint (default port 9997).

For GPU users, Xinference provides a Docker image. The image relies on NVIDIA GPUs and
CUDA, so the host must have a working GPU with a compatible CUDA version and driver.
The image does not bundle model files; it downloads models into the container, so you
typically mount a host directory to cache and reuse downloaded weights.

For larger setups, Xinference supports cluster deployment, including a Helm chart for
Kubernetes when the cluster has GPU support.

Distributed deployment lets model inference run across multiple workers and machines.
This is how a single logical service can span more hardware than one box provides.

The lightest way to try Xinference without local hardware is a Jupyter notebook on
Google Colab using a free GPU runtime. The model runs on Colab's GPU while a client
elsewhere calls the API, which keeps load off the developer's own machine.
