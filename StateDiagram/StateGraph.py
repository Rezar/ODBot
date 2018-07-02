

class ActionType:
    """
    This Class defines the type of action the robot receives.
    It could be a voice command, environment detection, etc
     """
    UNDEFINED = 'undefined'
    VOICE_COMMAND = 'voice_command'

class Action:
    """
    This Class combines ActionType and action value
    For example, if the ActionType is voice command, value would be the words of the command
    """
    def __init__(self, type = ActionType.UNDEFINED, value = ''):
        self.type = type
        self.value = value

    def __repr__(self):
        return 'Action (Type: {}, Value: {})'.format(self.type, self.value)


class StateAction:
    """
    This Class combines Action and the To-State
    It acts as the node or path in a graph
    """
    def __init__(self, action, to):
        if not isinstance(action, Action):
            print('error: action is not Action object but {} : addAction of {} to {}'.format(type(action), action, to))
            return
        if not isinstance(to, State):
            print('error: state is not State object but {} : addAction of {} to {}'.format(type(to), action, to))
            return
        self.action = action
        self.to = to

    def __repr__(self):
        return 'StateAction: (Type: {}, Value: {}, To: {})'.format(self.action.type, self.action.value, self.to.name)


class ResponseType:
    """
    This Class defines the type of responses the robot can output
    """
    UNDEFINED = 'undefined'
    LED = 'led'
    VOICE_RESPONSE = 'voice_response'
    MOTOR_MOVE = 'motor_move'
    MOTOR_ROTATE = 'motor_rotate'
    GO_TO_STATE = 'go_to_state'
    SLEEP = 'sleep'

class Response:
    """
    This Class combines ResponseType and its values
    A Response should have a name tag, appropriate ResponseType and value for the appropriate ResponseType
    For example, a response to goto root state would have
        name of 'going to root state',
        type of ResponseType.GO_TO_STATE,
        value of the variable for root state
    """
    def __init__(self, name = 'unnamed response', type = ResponseType.UNDEFINED, value = ''):
        self.name = name
        self.type = type
        self.value = value

    def __repr__(self):
        return 'Response: (Name: {}, Type: {}, Value: {})'.format(self.name, self.type, self.value)

class State:
    """
    This Class represents the Node of a graph
    stateActions is a set of StateAction defined earlier that is equivalent to edges / paths of a graph state
    responses is a list of Responses defined earlier that executes when a state is reached
    """
    #actions = StateAction
    #responses = Responses
    def __init__(self, name = 'unnamed state'):
        self.name = name
        self.stateActions = set()
        self.responses = list()

    def __repr__(self):
        return 'State: (Name: {}, Actions: {})'.format(self.name, self.stateActions)

    def getResponses(self):
        return self.responses

    def addAction(self, stateAction):
        self.stateActions.add(stateAction)

    def addResponse(self, response):
        self.responses.append(response)

    def getStateActions(self):
        return self.stateActions


class StateGraph:
    """
    This Class defines the whole graph itself
    It only has one variable: state, which represents the current state
    But it has several methods that are required to drive the whole graph
    """
    def __init__(self):
        state = None

    def setCurrentState(self, state):
        if isinstance(state, State):
            self.state = state
            self.onStateChange()
        else:
            print('state is not State but {}. {}', type(state), state)

    def getCurrentState(self):
        return self.state

    def onAction(self, actiontype, value):
        print("onAction({}, {})".format(actiontype, value))
        # if not isinstance(actiontype, ActionType):
        #     print('\ttype is not ActionType but {}. {}'.format(type(actiontype), actiontype))
        #     return

        #Search for any registered response from action
        currentState = self.getCurrentState()
        nextState = None
        for stateAction in currentState.getStateActions():
            if stateAction.action.type == actiontype and stateAction.action.value == value:
                #Found matching action
                if nextState is None:
                    nextState = stateAction.to
                else:
                    print('\tError duplicate nextState found. ActionStates: {}'.format(currentState.getStateActions()))
                    exit(0)

        if nextState is None:
            print("\tNextState not found")
            return

        if not isinstance(nextState, State):
            print("\tNextState was found but isn't an instance of State. state: {}".format(nextState))
            return

        self.setCurrentState(nextState)

    def onStateChange(self):
        print("onStateChange()")
        #Runs through state responses
        print("\tNew Current State: {}".format(self.state))
        print("\tExecuting responses for nextState...")

        if len(self.state.getResponses()) > 0:
            for response in self.state.getResponses():
                print('\tRunning Response {}'.format(response))
                # do response action whether it has to do with moving motors, turning led, etc
                if response.type == ResponseType.GO_TO_STATE:
                    self.setCurrentState(response.value)
        else:
            print('\tResponding with nothing')

