import logging
import openai
import tiktoken
import Keys

openai.api_key = Keys.OPEN_AI_KEY
enc = tiktoken.get_encoding("cl100k_base")




logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class GPT:
    def __init__(self, System, model="gpt-4"):
        self.Sys_Message = System
        self.model = model
        self.messages = []
    def __str__(self):
        return f"{self.__class__} instance"
    def _get_prompt(self, input=None):
        context = []
        context.append({"role": "system", "content": f"{self.Sys_Message}"})
        if not input is None:
            self.messages.append(input)
        for index, message in enumerate(self.messages):
            if index % 2 == 0:
                context.append({"role": "user", "content": message})
            else:
                context.append({"role": "assistant", "content": message})
        log.debug(f"Context is: {context}")
        return context
    def set_initial_message(self, message: str):
        self.messages = [message]
    def _attempt_chat_completion(self, input=None):
        try:
            completion = openai.ChatCompletion.create(
                model=self.model,
                messages=self._get_prompt(input),
            )
            return completion
        except Exception as e:
            log.info(f"Chat completion has failed {e}")

    def create_chat_completion(self, input = None):
        completion = self._attempt_chat_completion(input)
        log.debug(completion.choices[0].message.content)
        self.messages.append(completion.choices[0].message.content)
        return completion.choices[0].message.content

    def memory_wipe(self):
        self.messages = []






# class SemiRecursivePipeline:
#     def __init__(self, main_question, main_model="gpt-4", child_model="gpt-3.5-turbo"):
#         self.main_question = main_question
#         self.main_model = main_model
#         self.child_model = child_model
#
#     def process(self) -> str:
#         solver = Solver(self.main_question)
#
#         task_list = solver.create_chat_completion(self.main_question)
#
#         delegator = Delegator()
#
#         delegate_json = delegator.create_chat_completion(task_list)
#
#         delegator_parse = delegator_parser.DelegatorParser(delegate_json, self.main_question, self.main_model, self.child_model)
#
#         # child_out = delegator_parse.Delegate_Child_Pathway()
#         #
#         # combinator = Combinator(self.main_question)
#         #
#         # final_answer = combinator.create_chat_completion(f"{child_out} \n\n\n Using the information given from the subAI instances, fully answer this question: {self.main_question}")
#
#         # return final_answer
