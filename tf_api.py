import numpy as np

class Graph():
    def __init__(self):
        self.operations = []
        self.variables = []
        self.placeholders = []
        self.constants = []


    def as_default(self):
        global _default_graph
        _default_graph = self

def topology_sort(operation):
        ordering = []
        visited = set()

        def recursive_helper(node):
            if isinstance(node, Operation):
                for input_node in node.input_nodes:
                    if input_node not in visited:
                        recursive_helper(input_node)
            visited.add(node)
            ordering.append(node)

        recursive_helper(operation)

        return ordering

class Session():
    def run(self, operation, feed_dict={}):
        nodes_sorted = topology_sort(operation)

        for node in nodes_sorted:
            if type(node) == Placeholder:
                node.output = feed_dict[node]
            elif type(node) == Variable or type(node) == Constant:
                node.output = node.value
            else:
                inputs = [input_node.output for input_node in node.input_nodes]
                node.output = node.forward(*inputs)
        
        return operation.output

class Variable():
    def __init__(self, value=None):
        self.value = value
        _default_graph.variables.append(self)


class Placeholder():
    def __init__(self):
        self.value = None
        _default_graph.placeholders.append(self)

class Constant():
    def __init__(self, value=None):
        self.__value = value
        _default_graph.constants.append(self)

    @property
    def value(self):
        return self.__value

    @value.setter
    def set_value(self, value):
        raise ValueError("Cannot reassign value")

class Operation():
    def __init__(self, input_nodes=None):
        self.input_nodes = input_nodes
        self.output = None
    
        _default_graph.operations.append(self)

    def forward(self):
        pass

    def backward(self):
        pass

class BinaryOperation(Operation):
    def __init__(self, a,b):
        super().__init__(input_nodes=[a,b])

class add(BinaryOperation):
    def forward(self, a,b):
        return a+b

    def backward(self, upstream_grad):
        return NotImplementedError

class multiply(BinaryOperation):
    def forward(self,a,b):
        return a*b

    def backward(self,upstream_grad):
        return NotImplementedError
        
class divide(BinaryOperation):
    def forward(self,a,b):
        return np.true_divide(a,b)

    def backward(self, upstream_grad):
        return NotImplementedError

class matmul(BinaryOperation):
    def forward(self,a,b):
        return a.dot(b)

    def backward(self, upstream_grad):
        return NotImplementedError