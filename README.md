# README: Automatic Multi-Instance GPT (AMIG)

## Overview

Automatic Multi-Instance GPT is designed to provide an interface for utilizing multiple GPT-based AI models for iteratively answering a given question. Specifically, it combines the input from the main model (default: GPT-4) and a child model (default: GPT-3.5-turbo) for solving complex AI problems.

The main components of this code snippet are:

1. GPT_API
2. delegator_parser
3. SemiRecursivePipeline class

The module imports GPT_API and delegator_parser, which are used in the SemiRecursivePipeline class to generate, delegate, parse, and combine tasks for multiple subAI instances.

## SemiRecursivePipeline Class

The SemiRecursivePipeline class is initialized with three parameters:

1. main_question (string): The main question to be answered by the pipeline.
2. main_model (string, optional): The primary GPT model to be used (default: "gpt-4").
3. child_model (string, optional): The secondary GPT model to be used (default: "gpt-3.5-turbo").

The class has only one method:

1. process(): This method generates a list of subtasks, delegates them to the main and child models, combines their respective outputs, and returns the final answer as a string.

## Usage

To use the SemiRecursivePipeline class, follow these steps:

1. Import the necessary classes.
2. Instantiate the SemiRecursivePipeline object with your main_question and your choice of main_model and child_model, if you wish to use different models.
3. Call the `process()` method on your instantiated object to get the final answer to the main_question provided.

### Example

```python
from GPT_API import Solver, Delegator, Combinator
import delegator_parser

# Create an instance of SemiRecursivePipeline
pipeline = SemiRecursivePipeline(main_question="What is the capital of France?")

# Get the answer to the question using the process method
answer = pipeline.process()

print(answer)
```

## Dependencies

- GPT_API (custom module)
- delegator_parser (custom module)
- OpenAI API (external)
