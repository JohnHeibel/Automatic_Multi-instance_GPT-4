import Bot_Modules
import delegator_parser

class AIMGPipeline:
    def __init__(self, main_question, main_model="gpt-4", child_model="gpt-3.5-turbo"):
        self.main_question = main_question
        self.main_model = main_model
        self.child_model = child_model

    def process(self) -> str:
        solver = Bot_Modules.Solver(self.main_question)

        task_list = solver.create_chat_completion(self.main_question)

        delegator = Bot_Modules.Delegator()

        delegate_json = delegator.create_chat_completion(task_list)

        delegator_parse = delegator_parser.DelegatorParser(delegate_json, self.main_question, self.main_model, self.child_model)

        child_out = delegator_parse.Delegate_Child_Pathway()

        combinator = Bot_Modules.Combinator(self.main_question)

        final_answer = combinator.create_chat_completion(f"{child_out} \n\n\n Using the information given from the subAI instances, fully answer this question: {self.main_question}")

        return final_answer
