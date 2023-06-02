# Test I: "2022-12-19 00:00:00", "2023-01-01 23:59:59"
# Test II: "2023-01-02 00:00:00", "2023-01-15 23:59:59"
# Test III: "2023-01-16 00:00:00", "2023-01-29 23:59:59"
# Test IV: "2023-01-30 00:00:00", "2023-02-12 23:59:59"
# Test V: "2023-02-13 00:00:00", "2023-02-26 23:59:59"
# Test VI: "2023-02-27 00:00:00", "2023-03-12 23:59:59"
# Test VII: "2023-03-13 00:00:00", "2023-03-26 23:59:59"
import argparse
import os
import time
import datetime

import roman
from clearml import Task, Dataset, InputModel, Model
from tensorflow.keras.models import Sequential

# dataset = Dataset.create(
#     dataset_project="NeSy", dataset_name="DataBases"
# )

# add the example csv
#dataset.add_files(path="DataBases/")


# dataset = Dataset.get(dataset_project='NeSy', dataset_name='DataBases')
# dataset.sync_folder("DataBases")
# dataset.upload(chunk_size=100)
#
# # commit dataset changes
# dataset.finalize()

def start_task():
    global task
    task = Task.create(project_name='NeSy', task_name=f'Experiment Test (Neurosymbolic) {i}')
    # cloned_task = Task.clone(source_task=task)
    Task.enqueue(task=task, queue_name='default')
    # task.execute_remotely(queue_name='default', clone=True, exit_process=False)

    os.popen('cp ProblogAddons/bedu.py /root/.clearml/venvs-builds/3.10/lib/python3.10/site-packages/problog/library/bedu.py')

    f = open("/root/.clearml/venvs-builds/3.10/lib/python3.10/site-packages/problog/library/bedu.py", "w")

    import LogicalPlausibility
    import TimeSeriesPatternRecognition



    args = parser.parse_args()


    dataset_databases = Dataset.get(dataset_project='NeSy', dataset_name='DataBases')
    dataset_path_databases = dataset_databases.get_mutable_local_copy("DataBases/", True)

    dataset_results = Dataset.get(dataset_project='NeSy', dataset_name='Results')
    dataset_path_results = dataset_results.get_mutable_local_copy("Results/", True)

    models = Dataset.get(dataset_project='NeSy', dataset_name='Models')
    models_path = models.get_mutable_local_copy("Models/", True)

    lp = LogicalPlausibility.LogicalPlausibility()
    lp.check_plausibility(args.experiment_number, args.period_start, args.period_end, dataset_path_databases, dataset_path_results, models_path)

    dataset = Dataset.create(
             dataset_project="NeSy", dataset_name="Results"
        )
    dataset.add_files(path='Results/')
    dataset.upload(chunk_size=100)
    dataset.finalize()
    print("Logic results uploaded.")


    tspr = TimeSeriesPatternRecognition.TimeSeriesPatternRecognition()
    tspr.run(args.experiment_number, args.period_start, args.period_end, dataset_path_databases, dataset_path_results, models_path) #model_path)

    dataset = Dataset.create(
             dataset_project="NeSy", dataset_name="Results"
        )
    dataset.add_files(path='Results/')
    dataset.upload(chunk_size=100)
    dataset.finalize()
    print("Neuro results uploaded.")

    dataset = Dataset.create(
             dataset_project="NeSy", dataset_name="Models"
        )
    dataset.add_files(path='Models/')
    dataset.upload(chunk_size=100)
    dataset.finalize()
    print("Models uploaded.")

parser = argparse.ArgumentParser()
period_start = (datetime.datetime.strptime("2022-12-19 00:00:00", "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=14)).strftime("%Y-%m-%d %H:%M:%S")
period_end = (datetime.datetime.strptime("2023-01-01 23:59:59", "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=14)).strftime("%Y-%m-%d %H:%M:%S")

for i in range(2, 11):
    period_start = (datetime.datetime.strptime(period_start, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(
        days=14)).strftime("%Y-%m-%d %H:%M:%S")
    period_end = (datetime.datetime.strptime(period_end, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(
        days=14)).strftime("%Y-%m-%d %H:%M:%S")

    parser.add_argument('--experiment_number', type=int, default=i, metavar='N',
                            help='Experiment Number')
    parser.add_argument('--period_start', type=str, default=period_start, metavar='N',
                            help='Start Date')
    parser.add_argument('--period_end', type=str, default=period_end, metavar='N',
                            help='End Date')
    # parser.add_argument('--model_id', type=str, default="a18b1937a7f349ff859095f4902bd270", metavar='N',
    #                         help='ID of the model')

    start_task()

    while task.get_progress() != 100:
        time.sleep(30)
        print('wait for task to complete.')




    # commit dataset changes
    #dataset_results.finalize()