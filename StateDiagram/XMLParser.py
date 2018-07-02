import xml.etree.ElementTree as ET
from StateGraph import *


class XMLParser:

    def __init__(self, file = "sample1a.xml"):
        self.file = file

    def parse(self):
        graph = StateGraph()
        print("Parsing...")

        tree = ET.parse('sample1a.xml')
        root = tree.getroot()


        """
        Sample parser based on sample1a.xml
        """

        # print(ET.tostring(root, encoding='utf8').decode('utf8'))
        states = {}
        rootState = None
        for state in root:
            name = state.find("name").text
            states[name] = State(name)
            if rootState is None:
                rootState = states[name]


        for state in root:
            statename = state.find("name").text
            print("State:")
            print("\tName: {}".format(statename))
            print("\tStateActions: {} actions".format(len(state.findall("stateaction"))))

            #State Actions
            for stateaction in state.findall("stateaction"):
                type = stateaction.find("action").find("type").text
                value = stateaction.find("action").find("value").text
                to = states[stateaction.find("to").text]

                stateactionObj = StateAction(
                    Action(
                        ActionType().getType(type),
                        value
                    ),
                    to
                )
                states[statename].addAction(stateactionObj)
                print("\t\t{}".format(stateactionObj))


            print("\tResponses: {} responses".format(len(state.findall("response"))))
            #Responses
            for response in state.findall("response"):
                name = response.find("name").text
                type = ResponseType().getType(response.find("type").text)
                value = response.find("value").text
                if value.isdigit():
                    value = int(value)
                elif value in states:
                    value = states[value]

                responseObj = Response(name, type, value)
                states[statename].addResponse(responseObj)
                print("\t\t{}".format(responseObj))

        graph.setCurrentState(rootState)
        return graph