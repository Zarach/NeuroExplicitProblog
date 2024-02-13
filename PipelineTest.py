from clearml import PipelineController


def test1():
    print("test 1")
    return 'test1'

#@PipelineDecorator.component(execution_queue="default")
def test2():
    print("test 2")
    return 'test2'

if __name__ ==  '__main__':
    pipeline_controller = PipelineController(name='NeSy Pipeline', project='NeSy', abort_on_failure=True, repo='https://github.com/Zarach/NeuroExplicitProblog.git')
    pipeline_controller.add_function_step(
        name='step_one',
        function=test1,
        function_return=['test1_ret'],
        cache_executed_step=True
    )
    pipeline_controller.add_function_step(
        name='step_two',
        function=test2,
        function_return=['test2_ret'],
        cache_executed_step=True
    )
    pipeline_controller.start(queue='default')
    #pipeline_controller.start_locally()