# README: Automatic Multi-Instance GPT (AMIG)

## Overview

Automatic Multi-Instance GPT is designed to provide an interface for utilizing multiple GPT-based AI models for iteratively answering a given question. It calls a main GPT instance that creates a list of related questions. This is then processed aby another GPT instance to convert it to JSON. This file is parsed to delegate a variable number of child instances. Each child instance can be assigned a tool to use. Current only internal knoledge and search is implemented. Search is a simple implementation that gets the top 3 search results and uses GPT to summarize the page. These summaries are passed to the child instance. After each child has processed, the results are passed into a single final summariszer GPT instance that tries to answer the main question. 


## Usage

1. Create file Keys.py
2. Add key values of the form
```python
GOOGLE_API_KEY = "[GOOGLE_API_KEY]"
GOOGLE_CSE_KEY = "[GOOGLE_CSE_KEY]"
OPEN_AI_KEY = "[OPEN_AI_KEY]"
```
3. Run GPT-Run.py 

### Example Usage

```python
from GPT_API import Solver, Delegator, Combinator
import delegator_parser

def main():
  question = input("What is your question?\n")
  # Create an instance of SemiRecursivePipeline
  pipeline = SemiRecursivePipeline(main_question=question)

  # Get the answer to the question using the process method
  answer = pipeline.process()

  print(answer)

if __name__ == '__main__':
  main()

```

## Dependencies

- OpenAI API 
- GoogleAPIClient
- BeautifulSoup
- Requests
- Logging
- Tiktoken
- Multiprocessing
