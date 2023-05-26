# Test I: "2022-12-19 00:00:00", "2023-01-01 23:59:59"
# Test II: "2023-01-02 00:00:00", "2023-01-15 23:59:59"
# Test III: "2023-01-16 00:00:00", "2023-01-29 23:59:59"
# Test IV: "2023-01-30 00:00:00", "2023-02-12 23:59:59"
# Test V: "2023-02-13 00:00:00", "2023-02-26 23:59:59"
# Test VI: "2023-02-27 00:00:00", "2023-03-12 23:59:59"
# Test VII: "2023-03-13 00:00:00", "2023-03-26 23:59:59"
import argparse
import os

from clearml import Task, Dataset

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

task = Task.init(project_name='NeSy', task_name='Experiment Test (Logical)')
# cloned_task = Task.clone(source_task=task)
# Task.enqueue(task=cloned_task, queue_name='default')
task.execute_remotely(queue_name="default")

os.popen('cp ProblogAddons/bedu.py /root/.clearml/venvs-builds/3.10/lib/python3.10/site-packages/problog/library/bedu.py')

f = open("/root/.clearml/venvs-builds/3.10/lib/python3.10/site-packages/problog/library/bedu.py", "w")

import LogicalPlausibility

parser = argparse.ArgumentParser()

parser.add_argument('--experiment_number', type=str, default='I', metavar='N',
                        help='input batch size for training (default: 64)')
parser.add_argument('--period_start', type=str, default="2023-01-02 00:00:00", metavar='N',
                        help='input batch size for training (default: 64)')
parser.add_argument('--period_end', type=str, default="2023-01-15 23:59:59", metavar='N',
                        help='input batch size for training (default: 64)')

args = parser.parse_args()

dataset_databases = Dataset.get(dataset_project='NeSy', dataset_name='DataBases' )
dataset_path_databases = dataset_databases.get_mutable_local_copy("DataBases/", True)

dataset_results = Dataset.get(dataset_project='NeSy', dataset_name='Results' )
dataset_path_results = dataset_results.get_mutable_local_copy("Results/", True)

lp = LogicalPlausibility.LogicalPlausibility()
lp.check_plausibility(args.experiment_number, args.period_start, args.period_end, dataset_path_databases, dataset_path_results)

dataset_results.sync_folder(dataset_path_results)

# commit dataset changes
#dataset_results.finalize()