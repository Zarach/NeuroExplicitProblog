# Test I: "2022-12-19 00:00:00", "2023-01-01 23:59:59"
# Test II: "2023-01-02 00:00:00", "2023-01-15 23:59:59"
# Test III: "2023-01-16 00:00:00", "2023-01-29 23:59:59"
# Test IV: "2023-01-30 00:00:00", "2023-02-12 23:59:59"
# Test V: "2023-02-13 00:00:00", "2023-02-26 23:59:59"
# Test VI: "2023-02-27 00:00:00", "2023-03-12 23:59:59"
# Test VII: "2023-03-13 00:00:00", "2023-03-26 23:59:59"


import time
import datetime
import CML

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



for i in range(2, 11):
    period_start = (datetime.datetime.strptime(period_start, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(
        days=14)).strftime("%Y-%m-%d %H:%M:%S")
    period_end = (datetime.datetime.strptime(period_end, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(
        days=14)).strftime("%Y-%m-%d %H:%M:%S")

    CML.parser.add_argument('--experiment_number', type=int, default=i, metavar='N',
                            help='Experiment Number')
    CML.parser.add_argument('--period_start', type=str, default=period_start, metavar='N',
                            help='Start Date')
    CML.parser.add_argument('--period_end', type=str, default=period_end, metavar='N',
                            help='End Date')
    # parser.add_argument('--model_id', type=str, default="a18b1937a7f349ff859095f4902bd270", metavar='N',
    #                         help='ID of the model')

    CML.start_task(i)

    while CML.task.get_progress() != 100:
        time.sleep(30)
        print('wait for task to complete.')


    # commit dataset changes
    #dataset_results.finalize()