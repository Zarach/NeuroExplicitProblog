from clearml import PipelineController


def main():
    pipe = PipelineController(
        name="Pipeline Controller",
        project="examples",
        version="0.0.0",
        auto_version_bump=True,
    )

    pipe.add_function_step(
        name="increment_step_1",
        function=increment,
        function_return=["incremented_number"],
        cache_executed_step=True,
    )

    pipe.add_function_step(
        name="increment_step_2",
        parents=["increment_step_1"],
        function=increment,
        function_kwargs=dict(i="${increment_step_1.incremented_number}"),
        function_return=["incremented_number"],
        cache_executed_step=True,
    )

    pipe.start_locally(run_pipeline_steps_locally=True)


def increment(i: int = 0, limit: int = 2) -> int:
    if i < limit:
        print(f"incrementing from {i} of {i+1}")
        return i + 1
    else:
        print("limit reached")
        return i


if __name__ == "__main__":
    main()