import GPT_Pipeline

def main():
    main_question = input("What is your question?")

    pipeline = GPT_Pipeline.SemiRecursivePipeline(main_question)

    print(pipeline.process())


if __name__ == '__main__':
    main()



