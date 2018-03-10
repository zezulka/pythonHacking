import importlib
from types import ModuleType
from graphviz import Digraph

moduleName="numpy"

'''
def nodeList(graph):
    # { '\ta1', ..., '\tan', ..., '\tai -> aj' }
    return map((lambda x: x[1:]), filter((lambda x: '->' not in x), graph.body))
'''

def walkModuleRecursive(module, level, graph, currentPath, visited):
    if (level > 4):
        return
    moduleName = module.__name__
    graph.node(moduleName, color="#AAFFAA", style="filled")
    visited.append(moduleName)
    for symbol in dir(module):
        submodule = module.__getattribute__(symbol)
        if(isinstance(submodule, ModuleType) and submodule.__name__ not in visited):
            graph.edge(moduleName, submodule.__name__)
            if currentPath in submodule.__name__:
                walkModuleRecursive(submodule, level+1, graph, \
                                submodule.__name__, visited)
            else:
                graph.node(submodule.__name__, color="#AAFFFF", style="filled")

def walkModule(moduleName):
    graph = Digraph(moduleName)
    graph.graph_attr['rankdir'] = 'LR'
    module = importlib.import_module(moduleName)
    walkModuleRecursive(module, 0, graph, moduleName, [])
    graph.render("img/graph")

if __name__ == "__main__":
    walkModule(moduleName)
