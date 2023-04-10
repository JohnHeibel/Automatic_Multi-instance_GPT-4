import logging
import openai
import tiktoken
import time
import Keys
import multiprocessing
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv

load_dotenv()
openai.api_key = Keys.OPEN_AI_KEY
my_api_key = Keys.GOOGLE_API_KEY
my_cse_id = Keys.GOOGLE_CSE_KEY
enc = tiktoken.get_encoding("cl100k_base")




messages = []
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class GPT:
    def __init__(self, System, model="gpt-4"):
        self.Sys_Message = System
        self.model = model
        self.messages = []

    def _get_prompt(self, input):
        context = []
        context.append({"role": "system", "content": f"{self.Sys_Message}"})
        self.messages.append(input)
        for index, message in enumerate(self.messages):
            if index % 2 == 0:
                context.append({"role": "user", "content": message})
            else:
                context.append({"role": "assistant", "content": message})
        log.debug(f"Context is: {context}")
        return context

    def attempt_chat_completion(self, input):
        try:
            completion = openai.ChatCompletion.create(
                model=self.model,
                messages=self._get_prompt(input),
            )
            return completion
        except:
            log.info(f"Chat completion has been rate limited. Reattempting")
            time.sleep(5)
            return self.attempt_chat_completion(input)

    def create_chat_completion(self, input):
        completion = self.attempt_chat_completion(input)
        log.debug(completion.choices[0].message.content)
        self.messages.append(completion.choices[0].message.content)
        return completion.choices[0].message.content

    def memory_wipe(self):
        self.messages = []



class SearchBot:
    def __init__(self, search_input: "str"):
        self.input = search_input

    def google_search(self, search_term, api_key, cse_id, **kwargs) -> dict:
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
        return res['items']

    def _search_crop_process(self, link: dict) -> str:
        try:
            page = requests.get(link['link'])
            soup = BeautifulSoup(page.content, "html.parser")
            raw_text = soup.get_text().replace("\n", "")
            cropped = enc.decode(enc.encode(raw_text)[:4000])
        except:
            cropped = "The search has encountered an error, no page will be returned."
        print(len(cropped))
        search_test = GPT(
            "You are summarizeGPT. You will be given the raw text extracted from a website. You must create a summary of the core content on the page in a full and complete form. Results with no content or error messages should be ignored. Emphasize facts and statistics from the page.",
            model="gpt-3.5-turbo")
        summary = search_test.create_chat_completion(cropped)
        logging.debug(summary)
        return summary

    def search_pipeline(self) -> str:
        results = self.google_search(self.input, my_api_key, my_cse_id, num=3)
        summary_string = ""
        pool = multiprocessing.Pool(processes=3)
        website_summaries = pool.map(self._search_crop_process, results)
        for i in website_summaries:
            summary_string += (i+"\n")

        return summary_string

class GPTChild(GPT):
    def __init__(self, id: str, name: str, Child_Instruction: str, main_question, model="gpt-4"):
        CHILDPROMPT = f"""You are GPT-Child, a subinstance of a master problem solving AI. You will solve and iterate upon the task given to you by the master GPT instance. You have the authority to respond to any master tasks in clear and interpretable ways. The overall functioning of the system requires that you provide an answer. The overall question provided to the master AI is {main_question}"""
        super().__init__(CHILDPROMPT, model)
        self.inst = Child_Instruction
        prompt = f"Your individual task that you must answer is: {Child_Instruction}"
        self.messages = [prompt]
        self.ChildInst = prompt
        self.id = id
        self.name = name

    def __str__(self):
        return f"GPTChild {self.id} {self.name} with task: {self.ChildInst}"

    def _get_prompt(self):
        context = []
        context.append({"role": "system", "content": f"{self.Sys_Message}"})
        for index, message in enumerate(self.messages):
            if index % 2 == 0:
                context.append({"role": "user", "content": message})
            else:
                context.append({"role": "assistant", "content": message})
        log.debug(f"Context is: {context}")
        return context

    def attempt_chat_completion(self):
        try:
            completion = openai.ChatCompletion.create(
                model=self.model,
                messages=self._get_prompt(),
            )
            return completion
        except:
            log.info(f"Child chat completion has been rate limited. Reattempting")
            time.sleep(5)



    def create_chat_completion(self):
        completion = self.attempt_chat_completion()
        log.debug(completion.choices[0].message.content)
        self.messages.append(completion.choices[0].message.content)
        return completion.choices[0].message.content

class GPTChild_Search(GPT):
    def __init__(self, id: str, name: str, Child_Instruction: str, main_question, model="gpt-4"):
        CHILDPROMPT = f"""You are GPT-Child_Search, a subinstance of a master problem solving AI that searches the internet for information. You will solve and iterate upon the task given to you by the master GPT instance using the information returned from an internet search. You have the authority to respond to any master tasks in clear and interpretable ways. The overall functioning of the system requires that you provide an answer. The overall question provided to the master AI is {main_question}"""
        super().__init__(CHILDPROMPT, model)
        self.inst = Child_Instruction
        search_results = SearchBot(Child_Instruction).search_pipeline()
        prompt = f"The information from the internet search is: {search_results} \n Using this information, your individual task that you must answer is: {Child_Instruction}"
        self.messages = [prompt]
        self.ChildInst = prompt
        self.id = id
        self.name = name

    def __str__(self):
        return f"GPTChild {self.id} {self.name} with task: {self.ChildInst}"

    def _get_prompt(self):
        context = []
        context.append({"role": "system", "content": f"{self.Sys_Message}"})
        for index, message in enumerate(self.messages):
            if index % 2 == 0:
                context.append({"role": "user", "content": message})
            else:
                context.append({"role": "assistant", "content": message})
        log.debug(f"Context is: {context}")
        return context

    def attempt_chat_completion(self):
        try:
            completion = openai.ChatCompletion.create(
                model=self.model,
                messages=self._get_prompt(),
            )
            return completion
        except:
            log.info(f"Child chat completion has been rate limited. Reattempting")
            time.sleep(5)


    def create_chat_completion(self):
        completion = self.attempt_chat_completion()
        log.debug(completion.choices[0].message.content)
        self.messages.append(completion.choices[0].message.content)
        return completion.choices[0].message.content


class Delegator(GPT):
    def __init__(self, Model="gpt-4"):
        DELEGATORPROMPT = """You are DelegatorGPT, your task is to recieve a list of questions from the master AI and generate a json output of subAIs that need to be initialized for each step. You output a json file with the format {
        {
        	"children": [
        	{
        	"id": (id number of this subAI),
        	"subAIName": (A short descriptive name for this subAI instance),
        	"task": (the question this subAI instance is trying to solve),
        	"tool": (the appropriate tool for the AI. There are three options. 1. Internal: Use this tool for tasks not requiring facts or statistics, such as creative or interprative tasks, or definitions of words or concepts. 2. Search: Use this tool only if you need to know specific facts or statistics to answer the question 3. Calculator: Whenever mathematical operations are required, use this tool.),
        	}
        	(Add more entries to children according to the list given)
        	]
        }
        Fill in the the areas with parenthesis according to the contained instructions.
        """
        super().__init__(DELEGATORPROMPT, Model)


class Combinator(GPT):
    def __init__(self, main_question, Model="gpt-4"):
        COMBINATORPROMPT = f"""You are combinatorGPT, an extremely knowledgeable solving AI. Your task is to recive a list of responses to various sub-question given to the subAI instances by the master AI. You will take in this data, intepret the responses, and answer the final question to its full extent according to the subAI's answers. Unless the answers are straightforward, a long answer is preferred. Disregard any statements saying they were not able to answer the question. Remember that not all answers given may be correct. Use your own intuition and knowledge for each statement to fully answer the question or complete the request. If the SubAI's answers are in disagreement, choose a hard stance. The main question is {main_question}"""
        super().__init__(COMBINATORPROMPT, Model)


class Solver(GPT):
    def __init__(self, main_question, Model="gpt-4"):
        SOLVERPROMPT = f"You are SolverGPT. Your task is to approach a problem and break it down into separate and discrete questions that will be passed down to subAI instances. The problem you are tyring to break down into discrete steps to try and find the information needed to answer is: {main_question}"
        super().__init__(SOLVERPROMPT, Model)


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
