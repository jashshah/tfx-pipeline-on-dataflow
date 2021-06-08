now=$(date +"%H-%M-%S")
PROJECT_ID=project-id
export PIPELINE_NAME=tfx-tuning-caip-training-$now
ENDPOINT=https://endpoint-id-dot-us-west1.pipelines.googleusercontent.com
export CUSTOM_TFX_IMAGE=gcr.io/$PROJECT_ID/$PIPELINE_NAME

tfx pipeline compile --engine kubeflow --pipeline_path runner.py

tfx pipeline create  \
--engine kubeflow \
--pipeline_path=runner.py \
--endpoint=$ENDPOINT \
--build_target_image=$CUSTOM_TFX_IMAGE

tfx run create --engine kubeflow --pipeline_name=$PIPELINE_NAME --endpoint=$ENDPOINT

tfx run list --engine kubeflow --pipeline_name=$PIPELINE_NAME --endpoint=$ENDPOINT

