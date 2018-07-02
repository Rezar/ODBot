from StateGraph import *
from XMLParser import *

graph = XMLParser(file = "sample1a.xml").parse()



#Check currnet state
print("Current State: {}".format(graph.getCurrentState().name))

#Simulate an action
print("Simulating Action of VoiceCommand hello")
graph.onAction(ActionType.VOICE_COMMAND, 'hello')

#Check currnet state
print("Current State: {}".format(graph.getCurrentState().name))


"""
Output:

onStateChange()
	New Current State: State: (Name: Root state, Actions: set([StateAction: (Type: voice_command, Value: hello, To: State that says hello back)]))
	Executing responses for nextState...
	Responding with nothing
Current State: Root state
Simulating Action of VoiceCommand hello
onAction(voice_command, hello)
onStateChange()
	New Current State: State: (Name: State that says hello back, Actions: set([]))
	Executing responses for nextState...
	Running Response Response: (Name: Saying Hello Back with LED, Type: led, Value: Some Random LED Value)
	Running Response Response: (Name: Sleeping for 5 seconds, Type: sleep, Value: 5000)
	Running Response Response: (Name: Going back to Root State, Type: go_to_state, Value: State: (Name: Root state, Actions: set([StateAction: (Type: voice_command, Value: hello, To: State that says hello back)])))
onStateChange()
	New Current State: State: (Name: Root state, Actions: set([StateAction: (Type: voice_command, Value: hello, To: State that says hello back)]))
	Executing responses for nextState...
	Responding with nothing
Current State: Root state


"""