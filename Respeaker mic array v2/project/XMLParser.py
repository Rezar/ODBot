import xml.etree.ElementTree as ElementTree
from StateGraph import *


class XMLParser:

    def printd(self, value):
        if self.debug:
            print(value)

    def __init__(self, graph_file="sample1a.xml", debug=False):
        self.file = graph_file
        self.debug = debug

    def parse(self):
        graph = StateGraph()
        self.printd("Parsing...")

        tree = ElementTree.parse(self.file)
        root = tree.getroot()

        """
        Sample parser based on sample1a.xml
        """

        # self.printd(ET.tostring(root, encoding='utf8').decode('utf8'))
        states = {}
        root_state = None
        for state in root:
            name = state.find("name").text
            states[name] = State(name)
            if root_state is None:
                root_state = states[name]

        for state in root:
            statename = state.find("name").text
            self.printd("State:")
            self.printd("\tName: {}".format(statename))
            self.printd("\tStateActions: {} actions".format(len(state.findall("stateaction"))))

            # State Actions
            for stateaction in state.findall("stateaction"):
                typ = stateaction.find("action").find("type").text
                value = stateaction.find("action").find("value").text
                to = states[stateaction.find("to").text]

                stateaction_obj = StateAction(
                    Action(
                        ActionType().get_type(typ),
                        value
                    ),
                    to
                )
                states[statename].add_action(stateaction_obj)
                self.printd("\t\t{}".format(stateaction_obj))

            self.printd("\tResponses: {} responses".format(len(state.findall("response"))))

            # Responses
            for response in state.findall("response"):
                name = response.find("name").text
                typ = ResponseType().get_type(response.find("type").text)
                value = response.find("value").text
                if value.isdigit():
                    value = int(value)
                elif value in states:
                    value = states[value]

                response_obj = Response(name, typ, value)
                states[statename].add_response(response_obj)
                self.printd("\t\t{}".format(response_obj))

        graph.set_current_state(root_state)
        return graph
