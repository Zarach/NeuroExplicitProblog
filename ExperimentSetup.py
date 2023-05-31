# Test I: "2022-12-19 00:00:00", "2023-01-01 23:59:59"
# Test II: "2023-01-02 00:00:00", "2023-01-15 23:59:59"
# Test III: "2023-01-16 00:00:00", "2023-01-29 23:59:59"
# Test IV: "2023-01-30 00:00:00", "2023-02-12 23:59:59"
# Test V: "2023-02-13 00:00:00", "2023-02-26 23:59:59"
# Test VI: "2023-02-27 00:00:00", "2023-03-12 23:59:59"
# Test VII: "2023-03-13 00:00:00", "2023-03-26 23:59:59"
import argparse
import os

import roman
from clearml import Task, Dataset, InputModel, Model
from tensorflow.keras.models import Sequential

# dataset = Dataset.create(
#     dataset_project="NeSy", dataset_name="Results"
# )
#
# # add the example csv
# dataset.add_files(path="Results/")
#
# dataset.upload(chunk_size=100)
#
# # commit dataset changes
# dataset.finalize()


task = Task.init(project_name='NeSy', task_name='Experiment Test (Neurosymbolic)')
# cloned_task = Task.clone(source_task=task)
# Task.enqueue(task=cloned_task, queue_name='default')
task.execute_remotely(queue_name="default")

os.popen('cp ProblogAddons/bedu.py /root/.clearml/venvs-builds/3.10/lib/python3.10/site-packages/problog/library/bedu.py')

f = open("/root/.clearml/venvs-builds/3.10/lib/python3.10/site-packages/problog/library/bedu.py", "w")

import LogicalPlausibility
import TimeSeriesPatternRecognition

parser = argparse.ArgumentParser()

parser.add_argument('--experiment_number', type=str, default='2', metavar='N',
                        help='Experiment Number in roman numbers (default I)')
parser.add_argument('--period_start', type=str, default="2023-01-02 00:00:00", metavar='N',
                        help='Start Date')
parser.add_argument('--period_end', type=str, default="2023-01-15 23:59:59", metavar='N',
                        help='End Date')
parser.add_argument('--model_id', type=str, default="fea45e2128294960bc629ef78dbcd044", metavar='N',
                        help='ID of the model')

args = parser.parse_args()
roman_number = roman.toRoman(int(args.experiment_number)-1)
print(roman_number)
model = Model(args.model_id).get_weights()


dataset_databases = Dataset.get(dataset_project='NeSy', dataset_name='DataBases' )
dataset_path_databases = dataset_databases.get_mutable_local_copy("DataBases/", True)

dataset_results = Dataset.get(dataset_project='NeSy', dataset_name='Results' )
dataset_path_results = dataset_results.get_mutable_local_copy("Results/", True)

lp = LogicalPlausibility.LogicalPlausibility()
lp.check_plausibility(args.experiment_number, args.period_start, args.period_end, dataset_path_databases, dataset_path_results)

dataset = Dataset.create(
         dataset_project="NeSy", dataset_name="Results"
    )
dataset.add_files(path='Results/')
dataset.upload(chunk_size=100)
dataset.finalize()


tspr = TimeSeriesPatternRecognition.TimeSeriesPatternRecognition()
tspr.run(model, args.experiment_number, args.period_start, args.period_end, dataset_path_databases, dataset_path_results)

dataset = Dataset.create(
         dataset_project="NeSy", dataset_name="Results"
    )
dataset.add_files(path='Results/')
dataset.upload(chunk_size=100)
dataset.finalize()

# commit dataset changes
#dataset_results.finalize()