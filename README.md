# tfx-pipeline-on-dataflow

Step 1. Run the following command to download skaffold:

```
curl -Lo skaffold https://storage.googleapis.com/skaffold/releases/latest/skaffold-linux-amd64 && \
sudo install skaffold /usr/local/bin/

```

Step 2. Install the required packages:

```
pip install -r requirements.txt

```

Step 3. Create and run the Kubeflow Pipeline

```
bash tfx_pipeline.sh

```
