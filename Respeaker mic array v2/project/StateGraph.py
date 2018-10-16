class ActionType:
    """
    This Class defines the type of action the robot receives.
    It could be a voice command, environment detection, etc
     """

    def __init__(self):
        pass

    UNDEFINED = 'undefined'
    VOICE_COMMAND = 'voice_command'

    # def getType(self, actiontype):
    #     for var, val in ActionType.__dict__.items():
    #         if actiontype == val:
    #             return var
    #     return None
    def get_type(self, typ):
        if typ == self.UNDEFINED:
            return self.UNDEFINED
        elif typ == self.VOICE_COMMAND:
            return self.VOICE_COMMAND


class Action:
    """
    This Class combines ActionType and action value
    For example, if the ActionType is voice command, value would be the words of the command
    """

    def __init__(self, typ=ActionType.UNDEFINED, value=''):
        self.typ = typ
        self.value = value

    def __repr__(self):
        return 'Action (Type: {}, Value: {})'.format(self.typ, self.value)


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
        return 'StateAction: (Type: {}, Value: {}, To: {})'.format(self.action.typ, self.action.value, self.to.name)


class ResponseType:
    """
    This Class defines the type of responses the robot can output
    """

    def __init__(self):
        pass

    UNDEFINED = 'undefined'
    LED = 'led'
    VOICE_RESPONSE = 'voice_response'
    MOTOR_MOVE = 'motor_move'
    MOTOR_ROTATE = 'motor_rotate'
    GO_TO_STATE = 'go_to_state'
    SLEEP = 'sleep'
    CAMERA_MOVE = 'camera_move'

    type_dict = {
        'undefined': UNDEFINED,
        'led': LED,
        'voice_response': VOICE_RESPONSE,
        'motor_move': MOTOR_MOVE,
        'motor_rotate': MOTOR_ROTATE,
        'go_to_state': GO_TO_STATE,
        'sleep': SLEEP,
        'camera_move': CAMERA_MOVE
    }

    # def getType(self, type):
    #     for var, val in ResponseType.__dict__.iteritems():
    #         if type == val:
    #             return var
    #     return None

    # def getType(self, type):
    #     if type == self.UNDEFINED:
    #         return self.UNDEFINED
    #     elif type == self.LED:
    #         return self.LED
    #     elif type == self.VOICE_RESPONSE:
    #         return self.VOICE_RESPONSE
    #     elif type == self.MOTOR_MOVE:
    #         return self.MOTOR_MOVE
    #     elif type == self.MOTOR_ROTATE:
    #         return self.MOTOR_ROTATE
    #     elif type == self.GO_TO_STATE:
    #         return self.GO_TO_STATE
    #     elif type == self.SLEEP:
    #         return self.SLEEP
    #     return self.UNDEFINED

    def get_type(self, arg):
        return self.type_dict.get(arg, self.UNDEFINED)


class Response:
    """
    This Class combines ResponseType and its values
    A Response should have a name tag, appropriate ResponseType and value for the appropriate ResponseType
    For example, a response to goto root state would have
        name of 'going to root state',
        type of ResponseType.GO_TO_STATE,
        value of the variable for root state
    """

    def __init__(self, name='unnamed response', typ=ResponseType.UNDEFINED, value=''):
        self.name = name
        self.typ = typ
        self.value = value

    def __repr__(self):
        return 'Response: (Name: {}, Type: {}, Value: {})'.format(self.name, self.typ, self.value)


class State:
    """
    This Class represents the Node of a graph
    stateActions is a set of StateAction defined earlier that is equivalent to edges / paths of a graph state
    responses is a list of Responses defined earlier that executes when a state is reached
    """

    # actions = StateAction
    # responses = Responses
    def __init__(self, name='unnamed state'):
        self.name = name
        self.stateActions = set()
        self.responses = list()

    def __repr__(self):
        return 'State: (Name: {}, Actions: {})'.format(self.name, self.stateActions)

    def get_responses(self):
        return self.responses

    def add_action(self, state_action):
        self.stateActions.add(state_action)

    def remove_action(self, state_action):
        self.stateActions.remove(state_action)

    def add_response(self, response):
        self.responses.append(response)

    def remove_response(self, response):
        self.responses.remove(response)

    def get_state_actions(self):
        return self.stateActions


class StateGraph:
    """
    This Class defines the whole graph itself
    It only has one variable: state, which represents the current state
    But it has several methods that are required to drive the whole graph
    """

    def __init__(self):
        self.state = None
        self.on_state_change = self.default_on_state_change

    def set_on_state_change(self, method = None):
        if method is not None:
            self.on_state_change = method

    def set_current_state(self, state):
        if isinstance(state, State):
            self.state = state
            self.on_state_change()
        else:
            print('state is not State but {}. {}'.format(type(state), state))

    def get_current_state(self):
        return self.state

    def apply_action(self, actiontype, value):
        print("onAction({}, {})".format(actiontype, value))
        # if not isinstance(actiontype, ActionType):
        #     print('\ttype is not ActionType but {}. {}'.format(type(actiontype), actiontype))
        #     return

        # Search for any registered response from action
        current_state = self.get_current_state()
        next_state = None
        for stateAction in current_state.get_state_actions():
            if stateAction.action.typ == actiontype and stateAction.action.value == value:
                # Found matching action
                if next_state is None:
                    next_state = stateAction.to
                else:
                    print('\tError duplicate nextState found. ActionStates: {}'.format(current_state.get_state_actions()))
                    # exit(0)

        if next_state is None:
            print("\tNextState not found")
            return

        if not isinstance(next_state, State):
            print("\tNextState was found but isn't an instance of State. state: {}".format(next_state))
            return

        self.set_current_state(next_state)

    def default_on_state_change(self):
        print("onStateChange()")
        # Runs through state responses
        print("\tNew Current State: {}".format(self.state))
        print("\tExecuting responses for nextState...")

        if len(self.state.get_responses()) > 0:
            for response in self.state.get_responses():
                print('\tRunning Response {}'.format(response))
                # do response action whether it has to do with moving motors, turning led, etc
                if response.typ == ResponseType.GO_TO_STATE:
                    self.set_current_state(response.value)
        else:
            print('\tResponding with nothing')
