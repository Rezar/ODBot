from StateGraph import *
from XMLParser import *

graph = XMLParser(graph_file="sample1a.xml", debug=False).parse()


def on_state_change():
    print("State was changed to {}".format(graph.get_current_state()))


graph.set_on_state_change(on_state_change)

# Check currnet state
print("Current State: {}".format(graph.get_current_state().name))

# Simulate an action
print("Simulating Action of VoiceCommand hello")
graph.apply_action(ActionType.VOICE_COMMAND, 'hello')

# Check currnet state
print("Current State: {}".format(graph.get_current_state().name))

"""
Output:

Parsing...
State:
	Name: Root state
	StateActions: 1 actions
		StateAction: (Type: voice_command, Value: hello, To: State that says hello back)
	Responses: 0 responses
State:
	Name: State that says hello back
	StateActions: 0 actions
	Responses: 3 responses
		Response: (Name: Saying Hello Back with LED, Type: led, Value: Some Random LED Value)
		Response: (Name: Sleeping for 5 seconds, Type: sleep, Value: 5000)
		Response: (Name: Going back to Root State, Type: go_to_state, Value: State: (Name: Root state, Actions: set([StateAction: (Type: voice_command, Value: hello, To: State that says hello back)])))
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
