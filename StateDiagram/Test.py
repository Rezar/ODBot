from StateGraph import *

graph = StateGraph()

#Define States
rootState = State('Root state')
helloState = State('State that says hello back')

#Define state actions
rootState.addAction(
    StateAction(
        Action(
            ActionType.VOICE_COMMAND,
            'hello'
        ),
        helloState
    )
)

helloState.addResponse(
    Response(
        'Saying Hello Back with LED',
        ResponseType.LED,
        'Some Random LED Value'
    )
)

helloState.addResponse(
    Response(
        'Sleeping for 5 seconds',
        ResponseType.SLEEP,
        5000
    )
)

helloState.addResponse(
    Response(
        'Going back to Root State',
        ResponseType.GO_TO_STATE,
        rootState
    )
)

#Set roto state
graph.setCurrentState(rootState)


#Check currnet state
print("Current State: {}".format(graph.getCurrentState().name))

#Simulate an action
print("Simulating Action of VoiceCommand hello")
graph.onAction(ActionType.VOICE_COMMAND, 'hello')

#Check currnet state
print("Current State: {}".format(graph.getCurrentState().name))