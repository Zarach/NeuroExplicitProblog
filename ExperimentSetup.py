# Test I: "2022-12-19 00:00:00", "2023-01-01 23:59:59"
# Test II: "2023-01-02 00:00:00", "2023-01-15 23:59:59"
# Test III: "2023-01-16 00:00:00", "2023-01-29 23:59:59"
# Test IV: "2023-01-30 00:00:00", "2023-02-12 23:59:59"
# Test V: "2023-02-13 00:00:00", "2023-02-26 23:59:59"
# Test VI: "2023-02-27 00:00:00", "2023-03-12 23:59:59"
# Test VII: "2023-03-13 00:00:00", "2023-03-26 23:59:59"
import argparse

from clearml import Task, Dataset

task = Task.init(project_name='NeSy', task_name='Experiment Test (Logical)')
# cloned_task = Task.clone(source_task=task)
# Task.enqueue(task=cloned_task, queue_name='default')
task.execute_remotely(queue_name="default")

import LogicalPlausibility

parser = argparse.ArgumentParser(
                    experiment_number=0,
                    period_start="2023-03-13 00:00:00",
                    period_end="2023-03-26 23:59:59")

args = parser.parse_args()

dataset_databases = Dataset.get(dataset_project='NeSy', dataset_name='DataBases' )
dataset_path_databases = dataset_databases.get_mutable_local_copy("DataBases/", True)

dataset_results = Dataset.get(dataset_project='NeSy', dataset_name='Results' )
dataset_path_results = dataset_results.get_mutable_local_copy("Results/", True)

lp = LogicalPlausibility.LogicalPlausibility()
lp.check_plausibility(args.experiment_number, args.period_start, args.period_end, dataset_path_databases, dataset_path_results)