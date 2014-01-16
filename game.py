# Melanie Shafer
# Game engine
# Edited April 2011

import sys

import textwrap # edit made april 2011

class Node:

	def __init__(self, name):
                self.name = name
                self.description = None

class Edge:
        
        def __init__(self, node_in, command, node_to, constraint = None):
                self.node_in = node_in
                self.command = command
                self.node_to = node_to
                self.constraint = constraint

class Object:

        def __init__(self, start_node, object_name, short_description, long_description, weight):
                self.start_node = start_node
                self.object_name = object_name
                self.short_description = short_description
                self.long_description = long_description
                self.weight = weight

class Constraint:

        def __init__(self, constraint_name, object_name, state_name):
                self.constraint_name = constraint_name
                self.object_name = object_name
                self.state_name = state_name

class Game:
        
        def __init__(self, game_file):
                self.game_file = game_file
                self.current = "start"
                self.nodes = []
                self.edges = []
                self.objects = {}
                self.constraints = []
                self.constraint_dict = {}
                self.obj = {}
                self.read_game()

        def read_game(self):
                self.objects["backpack"] = []
                self.obj["backpack"] = []
                file = open(self.game_file, "r")
                for line in file:
                        line = line.strip()
                        if "::" in line:
                                type, rest = line.split("::", 1)
                                if type == "node":
                                        name, descript = rest.split("::", 1)
                                        node = Node(name)
                                        node.description = descript
                                        self.nodes.append(node)
                                        self.objects[name] = []

                                if type == "edge":
                                        node_in, command, node_to, constraint = rest.split("::", 3)
                                        edge = Edge(node_in, command, node_to, constraint)
                                        self.edges.append(edge)

                                if type == "object":
                                        start_node, object_name, short_description, long_description, weight = rest.split("::", 4)
                                        object = Object(start_node, object_name, short_description, long_description, weight)
                                        self.objects[start_node].append(object)

                                if type == "constraint":
                                        constraint_name, object_name, state_name = rest.split("::", 2)
                                        self.constraint_dict[constraint_name] = Constraint(constraint_name, object_name, state_name)
                                        self.constraints.append(constraint)


                                        

        def get_node(self, name, command = None):
                if command == None:
                        for node in self.nodes:
                                if node.name == name:
                                        return node

                else:
                        command = command.lower() # edit made april 2011

                        for edge in self.edges:
                                if edge.node_in == name and edge.command == command and edge.constraint == "None":
                                        return self.get_node(edge.node_to)

                                
                                if edge.node_in == name and edge.command == command and edge.constraint != "None":
                                        m = self.constraint_dict[edge.constraint]
                                        o = m.object_name

                                        if o in self.obj["backpack"]:
                                                print "Good, " + o + " is in your backpack. You can continue."
                                                return self.get_node(edge.node_to)
                                        else:
                                                print "You cannot continue without " + o
        
                return self.get_node(self.current)


        def start(self):
                command = None
                while True:
                        current_node = self.get_node(self.current, command)
                        self.current = current_node.name
                        if self.current == "end":
                                 print textwrap.fill(current_node.description, 20) # edit made april 2011
                                 break
                        print current_node.description
                        for object in self.objects[self.current]:
                                if object not in self.objects["backpack"]:
                                        print object.short_description
                        command = raw_input("Command> ")
        

                        
                        if "pickup" in command:
                                if object.object_name in command and object not in self.objects["backpack"] and self.objects[self.current] == [object]:
                                        self.objects["backpack"].append(object)
                                        self.objects[self.current].remove(object)
                                        self.obj["backpack"].append(object.object_name)
                                        print "You picked up " + object.object_name
                                else:
                                        print "That is not an object you can pick up."

                        if "drop" in command:
                                if object.object_name in command and object in self.objects["backpack"]:
                                        self.objects["backpack"].remove(object)
                                        self.objects[self.current].append(object)
                                        self.obj["backpack"].remove(object.object_name)
                                        print "You dropped " + object.object_name
                                else:
                                        print "You do not have that object to drop."
                        
                        if "backpack" in command:
                                for object in self.objects["backpack"]:
                                         print object.object_name
                                if self.objects["backpack"] == []:
                                        print "Your backpack is empty!"
                                else:
                                         item = raw_input("Pick the item> ")
                                         for object in self.objects["backpack"]:
                                                 if item == object.object_name:
                                                         print object.long_description

			
				



			if "help" in command:
                        	print """
         As a Terran, your goal is to survive in the Preserve.
         As a Tlic, your goal is to reproduce.
         All commands are in single quotations.
         Type 'restart' to go back to the beginning of the game.
          """

                        if "restart" in command:
                                 self.current = "start"
                                 self.nodes = []
                                 self.edges = []
                                 self.objects = {}
                                 self.constraints = []
                                 self.constraint_dict = {}
                                 self.obj = {}
                                 self.read_game()


		if self.current == "end":
                         print "~~~~~~Game Over! Congratulations!~~~~~~~"




	def simplify_command(self, command):
		self.command = command
		if command is not None:
			command = command.strip().lower()
		return command

                                

        def expand(self, node_name):
                retval = []
                for edge in self.edges:
                        if edge.node_in == node_name:
                                retval.append(self.get_node(edge.node_to))
                return retval

        def findPath(self, _from, _to):
                from_node = self.get_node(_from)
                to_node = self.get_node(_to)

                queue = Queue()
                queue.add(from_node)
                visited = {}

                while True:
                        current = queue.pop()
                        if current.name == to_node.name:
                                print "Found a path!"
                                break
                        if current.name not in visited:
                                for node in self.expand(current.name):
                                        queue.add(node)
                        visited[current.name] = current

class Queue:
        
        def __init__(self):
                self.queue = []

        def add(self, item):
                self.queue.append(item)

        def pop(self):
                return self.queue.pop(0)


game_file = sys.argv[1]
game = Game(game_file)
game.start()
