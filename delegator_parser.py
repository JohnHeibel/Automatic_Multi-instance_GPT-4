import json
import Bot_Modules
import logging
import multiprocessing


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

class DelegatorParser:
    def __init__(self, delegator_string, main_question: str, Model="gpt-3.5-turbo", Child_Model = "gpt-3.5-turbo"):
        self.del_json = json.loads(delegator_string)
        self.model = Model
        self.child_model = Child_Model
        self.main_question = main_question
        self.children = []
        self.generations = []


    def _child_parser(self, id: str, name: str, task: str, tool: str):
        if tool.lower() == "search":
            return Bot_Modules.GPTChild_Search(id,
                                           name,
                                           task,
                                           self.main_question,
                                           self.child_model)
        if tool.lower() == "calculator":
            return Bot_Modules.GPTChild_Search(id,
                                    name,
                                    task,
                                    self.main_question,
                                    self.child_model)
        else:
            return Bot_Modules.GPTChild(id,
                                    name,
                                    task,
                                    self.main_question,
                                    self.child_model)


    def _gen_children(self):
        for i in range(len(self.del_json['children'])):
            child = self._child_parser(
                                       self.del_json['children'][i]['id'],
                                       self.del_json['children'][i]['subAIName'],
                                       self.del_json['children'][i]['task'],
                                       self.del_json['children'][i]['tool']
                                       )
            log.debug(f"Child {child}")
            self.children.append(child)

    def _gen_messages(self):
        pool = multiprocessing.Pool(processes=self.del_json['children'][-1]['id'])
        self.generations = pool.map(self._gen_child_message, self.children)
        # for i in self.children:
        #     generation = i.create_chat_completion()
        #     log.debug(generation)
        #     self.generations.append(generation)

    def _gen_child_message(self, child) -> str:
        generation = child.create_chat_completion()
        log.debug(f"\nChild #{child.id} {child.name} \n {generation} \n")
        return (f"\n\[SubAI #{child.id} {child.name}: \n The task was {child.inst} The generation was {generation}]\n")

    def Delegate_Child_Pathway(self) -> str:
        self._gen_children()
        self._gen_messages()
        child_out = ""
        f = open("child_log.txt", "w")
        for i in self.generations:
            f.write(i)
            child_out += (i+"\n")
        f.close()
        return child_out

