import time
import datetime
from clearml import Task, Dataset, InputModel, Model
import os

def start_task(i, local=False):
    global task
    global parser
    task = Task.create(project_name='NeSy', task_name=f'Experiment Test (Neurosymbolic) {i}')
    # cloned_task = Task.clone(source_task=task)
    Task.enqueue(task=task, queue_name='default')
    # task.execute_remotely(queue_name='default', clone=True, exit_process=True)

    if not local:
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

