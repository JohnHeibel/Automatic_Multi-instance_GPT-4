import GPT_API
import logging
import Search_Tool

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)



class GPTChild(GPT_API.GPT):
    def __init__(self, id: str, name: str, Child_Instruction: str, main_question, model="gpt-4"):
        CHILDPROMPT = f"""You are GPT-Child, a subinstance of a master problem solving AI. You will solve and iterate upon the task given to you by the master GPT instance. You have the authority to respond to any master tasks in clear and interpretable ways. The overall functioning of the system requires that you provide an answer. The overall question provided to the master AI is {main_question}"""
        super().__init__(CHILDPROMPT, model)
        self.set_initial_message(f"Your individual task that you must answer is: {Child_Instruction}")
        self.inst = Child_Instruction
        self.id = id
        self.name = name

    def __str__(self):
        return f"GPTChild {self.id} {self.name}"

class GPTChild_Search(GPT_API.GPT):
    def __init__(self, id: str, name: str, Child_Instruction: str, main_question, model="gpt-4"):
        CHILDPROMPT = f"""You are GPT-Child_Search, a subinstance of a master problem solving AI that searches the internet for information. You will solve and iterate upon the task given to you by the master GPT instance using the information returned from an internet search. You have the authority to respond to any master tasks in clear and interpretable ways. The overall functioning of the system requires that you provide an answer. The overall question provided to the master AI is {main_question}"""
        super().__init__(CHILDPROMPT, model)
        search_results = Search_Tool.SearchBot(Child_Instruction).search_pipeline()
        self.set_initial_message(f"The information from the internet search is: {search_results} \n Using this information, your individual task that you must answer is: {Child_Instruction}")
        self.inst = Child_Instruction
        self.id = id
        self.name = name

    def __str__(self):
        return f"GPTChild_Search {self.id} {self.name}"


class Delegator(GPT_API.GPT):
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


class Combinator(GPT_API.GPT):
    def __init__(self, main_question, Model="gpt-4"):
        COMBINATORPROMPT = f"""You are combinatorGPT, an extremely knowledgeable solving AI. Your task is to recive a list of responses to various sub-question given to the subAI instances by the master AI. You will take in this data, intepret the responses, and answer the final question to its full extent according to the subAI's answers. Unless the answers are straightforward, a long answer is preferred. Disregard any statements saying they were not able to answer the question. Remember that not all answers given may be correct. Use your own intuition and knowledge for each statement to fully answer the question or complete the request. If the SubAI's answers are in disagreement, choose a hard stance. The main question is {main_question}"""
        super().__init__(COMBINATORPROMPT, Model)


class Solver(GPT_API.GPT):
    def __init__(self, main_question, Model="gpt-4"):
        SOLVERPROMPT = f"You are SolverGPT. Your task is to approach a problem and break it down into separate and discrete questions that will be passed down to subAI instances. The problem you are tyring to break down into discrete steps to try and find the information needed to answer is: {main_question}"
        super().__init__(SOLVERPROMPT, Model)
