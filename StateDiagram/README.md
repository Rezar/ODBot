# Files and what they do
StateGraph.py - The Graph class file

Test.py - Demonstrates graph and how to add nodes and edges programmatically

Test2.py - Demonstrates XMLParser and building the graph using it

XMLParser.py - Class file that parses sample1a.xml

# Sample file
We're using sample1a.xml for now and XMLParser is based on it
# Variable Explanation
- State - a Node of the graph
- StateAction - an edge of the graph (Action is the actual action requirement; StateAction holds action and destination node)
- Response - the action that robot takes once a certain state is reached
* More details can be found in the StateGraph.py in its comments
