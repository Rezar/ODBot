from StateGraph import *

graph = StateGraph()

# Define States
rootState = State('Root state')
helloState = State('State that says hello back')

# Define state actions
rootState.add_action(
    StateAction(
        Action(
            ActionType.VOICE_COMMAND,
            'hello'
        ),
        helloState
    )
)

helloState.add_response(
    Response(
        'Saying Hello Back with LED',
        ResponseType.LED,
        'Some Random LED Value'
    )
)

helloState.add_response(
    Response(
        'Sleeping for 5 seconds',
        ResponseType.SLEEP,
        5000
    )
)

helloState.add_response(
    Response(
        'Going back to Root State',
        ResponseType.GO_TO_STATE,
        rootState
    )
)

# Set roto state
graph.set_current_state(rootState)


# Check currnet state
print("Current State: {}".format(graph.get_current_state().name))

# Simulate an action
print("Simulating Action of VoiceCommand hello")
graph.apply_action(ActionType.VOICE_COMMAND, 'hello')

# Check currnet state
print("Current State: {}".format(graph.get_current_state().name))


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