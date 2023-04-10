import GPT_Pipeline

def main():
    mainq = """What would you call an implementation of an AI that uses different specialized versions of itself to answer questions? Make the names simple, understadable, and unique.
"""

    pipeline = GPT_Pipeline.SemiRecursivePipeline(mainq)

    print(pipeline.process())


if __name__ == '__main__':
    main()



