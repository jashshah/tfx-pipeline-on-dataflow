import os
import pprint
import tempfile
import urllib
from typing import Optional, Dict, List, Text
import absl
import tensorflow as tf
import numpy as np
import tensorflow_model_analysis as tfma
tf.get_logger().propagate = False
pp = pprint.PrettyPrinter()

import tfx
# from tfx import v1 as tfx
from tfx.orchestration import pipeline
from tfx.orchestration.experimental.interactive.interactive_context import InteractiveContext

from tfx.components import CsvExampleGen
from tfx.components import StatisticsGen
from tfx.components import SchemaGen
from tfx.components import Transform
from tfx.components import Trainer
from tfx.components import Evaluator
from tfx.components import ResolverNode
from tfx.components import Pusher

from tfx.dsl.components.base import executor_spec
from tfx.components.trainer.executor import GenericExecutor

from tfx.dsl.experimental import latest_blessed_model_resolver
from tfx.types.standard_artifacts import Model
from tfx.types.standard_artifacts import ModelBlessing

from tfx.types import Channel


def create_pipeline(pipeline_name: Text,
                    pipeline_root: Text,
                    path_to_tfrecords: Text,
                    module_file: Text,
                    metric_module_file: Text,
                    train_steps: int,
                    eval_steps: int,
                    ai_platform_distributed_training: bool,
                    enable_tuning: bool,
                    ai_platform_training_args: Dict[Text, Text],
                    ai_platform_serving_args: Dict[Text, Text],
                    beam_pipeline_args: List[Text],
                    enable_cache: Optional[bool] = False) -> pipeline.Pipeline:
    # This is the path where your model will be pushed for serving.
    _serving_model_dir = os.path.join(
        tempfile.mkdtemp(), 'serving_model/taxi_simple')

    # Set up logging.
    absl.logging.set_verbosity(absl.logging.INFO)

    _data_root = 'gs://ml_test_micron/jash/taxi_test'

    example_gen = CsvExampleGen(input_base=_data_root)

    statistics_gen = StatisticsGen(
        examples=example_gen.outputs['examples'])

    schema_gen = SchemaGen(
        statistics=statistics_gen.outputs['statistics'],
        infer_feature_shape=False)

    # example_validator = ExampleValidator(
    #     statistics=statistics_gen.outputs['statistics'],
    #     schema=schema_gen.outputs['schema'])

    _taxi_transform_module_file = 'taxi_transform.py'
    transform = Transform(
        examples=example_gen.outputs['examples'],
        schema=schema_gen.outputs['schema'],
        module_file=_taxi_transform_module_file)

    _taxi_trainer_module_file = 'taxi_trainer.py'

    trainer = Trainer(
        module_file=_taxi_trainer_module_file,
        custom_executor_spec=executor_spec.ExecutorClassSpec(GenericExecutor),
        examples=transform.outputs['transformed_examples'],
        transform_graph=transform.outputs['transform_graph'],
        schema=schema_gen.outputs['schema'],
        train_args=tfx.proto.trainer_pb2.TrainArgs(num_steps=10000),
        eval_args=tfx.proto.trainer_pb2.EvalArgs(num_steps=5000))

    eval_config = tfma.EvalConfig(
        model_specs=[
            # This assumes a serving model with signature 'serving_default'. If
            # using estimator based EvalSavedModel, add signature_name: 'eval' and 
            # remove the label_key.
            tfma.ModelSpec(label_key='tips')
        ],
        metrics_specs=[
            tfma.MetricsSpec(
                # The metrics added here are in addition to those saved with the
                # model (assuming either a keras model or EvalSavedModel is used).
                # Any metrics added into the saved model (for example using
                # model.compile(..., metrics=[...]), etc) will be computed
                # automatically.
                # To add validation thresholds for metrics saved with the model,
                # add them keyed by metric name to the thresholds map.
                metrics=[
                    tfma.MetricConfig(class_name='ExampleCount'),
                    tfma.MetricConfig(class_name='BinaryAccuracy',
                      threshold=tfma.MetricThreshold(
                          value_threshold=tfma.GenericValueThreshold(
                              lower_bound={'value': 0.5}),
                          # Change threshold will be ignored if there is no
                          # baseline model resolved from MLMD (first run).
                          change_threshold=tfma.GenericChangeThreshold(
                              direction=tfma.MetricDirection.HIGHER_IS_BETTER,
                              absolute={'value': -1e-10})))
                ]
            )
        ],
        slicing_specs=[
            # An empty slice spec means the overall slice, i.e. the whole dataset.
            tfma.SlicingSpec(),
            # Data can be sliced along a feature column. In this case, data is
            # sliced along feature column trip_start_hour.
            tfma.SlicingSpec(feature_keys=['trip_start_hour'])
        ])

    # Use TFMA to compute a evaluation statistics over features of a model and
    # validate them against a baseline.

    # The model resolver is only required if performing model validation in addition
    # to evaluation. In this case we validate against the latest blessed model. If
    # no model has been blessed before (as in this case) the evaluator will make our
    # candidate the first blessed model.

    model_resolver = ResolverNode(
          instance_name='latest_blessed_model_resolver',
          resolver_class=latest_blessed_model_resolver.LatestBlessedModelResolver,
          model=Channel(type=Model),
          model_blessing=Channel(type=ModelBlessing))

    evaluator = tfx.components.Evaluator(
        examples=example_gen.outputs['examples'],
        model=trainer.outputs['model'],
        baseline_model=model_resolver.outputs['model'],
        eval_config=eval_config)
    
    components=[
            example_gen,
            statistics_gen,
            schema_gen,
            transform,
            trainer,
            model_resolver,
            evaluator
        ]

    
    return pipeline.Pipeline(
      pipeline_name=pipeline_name,
      pipeline_root=pipeline_root,
      components=components,
      enable_cache=enable_cache,
      beam_pipeline_args=beam_pipeline_args
    )