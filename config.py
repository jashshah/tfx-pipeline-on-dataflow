# Copyright 2021 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# pylint: disable=line-too-long, invalid-envvar-default, too-few-public-methods
"""
The pipeline configurations.
"""

import os
from datetime import datetime


class Config:
    """Sets configuration vars."""
    # Lab user environment resource settings
    GCP_REGION=os.getenv("GCP_REGION", "us-west1")

    PROJECT_ID=os.getenv("PROJECT_ID", "xyz-dev-quantiphi-mlops")

    ARTIFACT_STORE_URI=os.getenv("ARTIFACT_STORE_URI","gs://xyz-dev-quantiphi-mlops-ml-default/ak/artifact_store")

    CUSTOM_SERVICE_ACCOUNT=os.getenv("CUSTOM_SERVICE_ACCOUNT","shared-service-account@xyz-dev-quantiphi-mlops.iam.gserviceaccount.com")
    # Lab user runtime environment settings

#     PIPELINE_NAME=os.getenv("PIPELINE_NAME", "tfx_witout_tuning_and_caip13")

    PIPELINE_NAME=os.getenv("PIPELINE_NAME","tfx-tuning-caip-training-"+datetime.now().strftime("%H-%M-%S"))

    MODEL_NAME=os.getenv("MODEL_NAME", "csam_obj_detection")

    DATA_ROOT_URI=os.getenv("DATA_ROOT_URI","gs://xyz-dev-quantiphi-mlops-ml-default/tfrecord_beam/csam-tf-records-training-20210312-115607/training")

    TFX_IMAGE=os.getenv("KUBEFLOW_TFX_IMAGE", "tensorflow/tfx:0.29.0")

    RUNTIME_VERSION=os.getenv("RUNTIME_VERSION", "2.3")

    PYTHON_VERSION=os.getenv("PYTHON_VERSION", "3.7")

    SERVING_DIR=os.getenv("SERVING_DIR","gs://xyz-dev-quantiphi-mlops-ml-default/ak/serving_model_dir")

    USE_KFP_SA=os.getenv("USE_KFP_SA", "False")

    ENABLE_TUNING=os.getenv("ENABLE_TUNING", "True")

    ENABLE_AIP_TRAINING=os.getenv("ENABLE_AIP_TRAINING", "False")

    IMAGE_KEY = os.getenv("IMAGE_KEY",'image/encoded')

    LABEL_KEY = os.getenv("LABEL_KEY",'labels')

    TRAIN_DATA_SIZE = os.getenv("TRAIN_DATA_SIZE",80)

    BATCH_SIZE = os.getenv("BATCH_SIZE",8)

    TABLE_SPEC=os.getenv("TABLE_SPEC","xyz-dev-quantiphi-mlops.default_dataset.csam_split_v1")

    ERROR_TABLE_SPEC=os.getenv("ERROR_TABLE_SPEC","error_logs.csam_error_cases_logs")

    CLASS_NAME_TABLE=os.getenv("CLASS_NAME_TABLE","xyz-dev-quantiphi-mlops.default_dataset.class_names")

    CLASS_NAME_PATH=os.getenv("CLASS_NAME_PATH","gs://xyz-dev-quantiphi-mlops-ml-default/csam_data/data/od_classes.txt")

    CLASS_NAME_STRING=os.getenv("CLASS_NAME_STRING",None)

    MODE=os.getenv("MODE","training")

    NUM_SHARDS=os.getenv("NUM_SHARDS",20)

    SETUP_FILE=os.getenv("SETUP_FILE","./setup.py")

#     RUNNER=os.getenv("RUNNER","DirectRunner")
    RUNNER=os.getenv("RUNNER","DataFlowRunner")

    STAGING_LOCATION=os.getenv("STAGING_LOCATION","gs://xyz-dev-quantiphi-mlops-default/staging")

    TEMP_LOCATION=os.getenv("TEMP_LOCATION","gs://xyz-dev-quantiphi-mlops-default/temp")

    now=os.getenv("now",datetime.now().strftime("%d%m%Y-%H-%M-%S"))

    JOB_NAME=os.getenv("JOB_NAME","csam_tf_records"+str(now))

    OUTPUT_PATH=os.getenv("OUTPUT_PATH","gs://xyz-dev-quantiphi-mlops-ml-default/tfrecord_beam/"+JOB_NAME)

    MACHINE_TYPE=os.getenv("MACHINE_TYPE","n1-standard-16")

    MAXIMUM_WORKERS=os.getenv("MAXIMUM_WORKERS","50")

    SERVICE_ACCOUNT_EMAIL=os.getenv("SERVICE_ACCOUNT_EMAIL","shared-service-account@xyz-dev-quantiphi-mlops.iam.gserviceaccount.com")

    ENDPOINT = os.getenv("ENDPOINT",'https://3ffb208ba15c72ab-dot-us-west1.pipelines.googleusercontent.com')

    SUBNETWORK=os.getenv("SUBNETWORK","https://www.googleapis.com/compute/v1/projects/shared-vpc-271916/regions/us-west1/subnetworks/sub-us-west1-xyz-dev-test")

    NO_USE_PUBLIC_IPS=os.getenv("NO_USE_PUBLIC_IPS",'True')

    MODULE_FILE=os.getenv("MODULE_FILE","taxi_tfx_utils.py")

#     MODULE_FILE=os.getenv("MODULE_FILE","gs://xyz-dev-quantiphi-mlops-default/ak/tfx_pipelines/tfx_utils.py") #necessary for caip training

    METRIC_MODULE_FILE = os.getenv("METRIC_MODULE_FILE","utilities.tfx_metrics.loss_metric")

    HP_EPOCHS = os.getenv("HP_EPOCHS", 2)

    TRAIN_STEPS=os.getenv("TRAIN_STEPS", 10)

    EVAL_STEPS=os.getenv("EVAL_STEPS",5)

    SCALE_TIER=os.getenv("SCALE_TIER", "CUSTOM")

    MASTER_TYPE=os.getenv("MASTER_TYPE", "n1-standard-4")

    WORKER_COUNT=os.getenv("Config.WORKER_COUNT", 1)

    WORKER_TYPE=os.getenv("WORKER_TYPE", "n1-standard-4")

    ACCELERATOR_COUNT=os.getenv("ACCELERATOR_COUNT", 1)

    WORKER_ACCELERATOR=os.getenv("WORKER_ACCLERATOR", "NVIDIA_TESLA_P100")

    MASTER_ACCELERATOR=os.getenv("MASTER_ACCLERATOR", "NVIDIA_TESLA_P100")

    IMG_FOR_CAIP=os.getenv("IMG_FOR_CAIP","gcr.io/xyz-dev-quantiphi-mlops/tfx_pipeline_caip:v6")

    UAIP_ENDPOINT = os.getenv("UAIP_ENDPOINT", '8025133060997513216')

    UAIP_ENDPOINT_LOCATION = os.getenv("UAIP_ENDPOINT_LOCATION", 'us-west1')

    UAIP_IMAGE_URI = os.getenv("UAIP_IMAGE_URI", 'gcr.io/xyz-dev-quantiphi-mlops/uaip_custom_container/prediction/artifacts/base-gpu:test_v3')

    GCS_MODEL_PATH = os.getenv("GCS_MODEL_PATH", "gs://model_artifacts_mlops/jash/csam_model/1/")

    UAIP_ARTIFACT_URI = os.getenv("UAIP_ARTIFACT_URI", "gs://model_artifacts_mlops/jash")

    MODEL_IDS_TABLE = os.getenv("MODEL_IDS_TABLE", "default_dataset.models_table_v1")

    MODEL_CONFIG_GCS_FILE = os.getenv("MODEL_CONFIG_GCS_FILE","gs://us-west2-xyz-dev-quantiphi--afbf3ddb-bucket/dags/composer_config_files/model_deployment_parameters.json")

    MODEL_DISPLAY_NAME = os.getenv("MODEL_DISPLAY_NAME","Tfx_Model"+str(datetime.now().strftime("%d_%m")))

    MAX_TRIALS = os.getenv("MAX_TRIALS",2)

    SPLIT_FACTOR = os.getenv("SPLIT_FACTOR",75)

    BQ_DATA_TABLE = os.getenv("BQ_DATA_TABLE","xyz-dev-quantiphi-mlops.default_dataset.csam_split_v1")

    TFRECORD_JOB_NAME=os.getenv("TFRECORD_JOB_NAME", "tfx-tfrecord"+datetime.now().strftime("%H-%M-%S"))

    BS_MIN_VAL=os.getenv("BS_MIN_VAL",4)

    BS_MAX_VAL=os.getenv("BS_MAX_VAL",12)

    DECAY_MIN_VAL=os.getenv("DECAY_MIN_VAL",0)

    DECAY_MAX_VAL=os.getenv("DECAY_MAX_VAL",0.9)

    LR_MIN_VAL=os.getenv("LR_MIN_VAL",0.001)

    LR_MAX_VAL=os.getenv("LR_MAX_VAL",0.1)
    