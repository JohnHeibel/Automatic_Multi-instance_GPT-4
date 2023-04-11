import GPT_Pipeline

def main():
    main_question = input("What is your question?\n")

    pipeline = GPT_Pipeline.AIMGPipeline(main_question)

    print(pipeline.process())


if __name__ == '__main__':
    main()



