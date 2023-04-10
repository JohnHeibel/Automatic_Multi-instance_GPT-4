import GPT_Pipeline

def main():
    file = open(r"C:\Users\jhcat\OneDrive\Documents\College\Automatic Multi-Instance GPT-4\GPT_Pipeline.py", "r")
    data = file.read()
    file.close()
    mainq = f"""Given a snippet of code, write a README file describing it. The code is: {data}"""

    pipeline = GPT_Pipeline.SemiRecursivePipeline(mainq)

    print(pipeline.process())


if __name__ == '__main__':
    main()



