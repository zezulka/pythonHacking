#!/usr/bin/python

import importlib
from inspect import *
from graphviz import Digraph

moduleName="numpy"
symVerifiers=[isclass, isfunction]

def checkForSymbolConflictsRec(module, level, currentPath, visited, symbsSoFar):
    """
    Checks whether there are any conflicting symbols throughout the module.
    In the context of this function, conflicting symbol is a symbol (var, fun)
    which appears at least twice throughout the module.
    Context: consider module arithmetics:
    arithmetics
        real
            (fun def) sum(a,b)
        integer
            (fun def) sum(a,b)
    The function definition for sum is then a conflicting symbol, as in any
    other Python module which would import these two submodules in the manner
        
        from arithmetics.real import *
        from arithmetics.integer import *

    could cause unexpected behaviour.
    """
    moduleName = module.__name__
    visited.append(moduleName)
    #visited.append(moduleName)
    for symbol in dir(module):
        attr = module.__getattribute__(symbol)
        if(reduce((lambda prev, now: prev or now(attr)), \
           symVerifiers, False)):
            if symbsSoFar.has_key(attr):
                symbsSoFar[attr].append(moduleName)
            else:
                symbsSoFar[attr]=[moduleName]
        elif(ismodule(attr) and attr.__name__ not in visited):
            checkForSymbolConflictsRec(attr, level+1, attr.__name__, \
                                       visited, symbsSoFar)
    return symbsSoFar
            
def genModuleGraphRec(module, level, graph, currentPath, visited):
    """
    Generates graph whose nodes are (sub)modules and edges depict the
    relation 'module -> submodule'. Results are stored in the input parameter
    graph.
    """
    moduleName = module.__name__
    graph.node(moduleName, color="#AAFFAA", style="filled")
    visited.append(moduleName)
    for symbol in dir(module):
        submodule = module.__getattribute__(symbol)
        if(ismodule(submodule) \
           and submodule.__name__ not in visited):
            graph.edge(moduleName, submodule.__name__)
            if currentPath in submodule.__name__:
                genModuleGraphRec(submodule, level+1, graph, \
                                submodule.__name__, visited)
            else:
                graph.node(submodule.__name__, color="#AAFFFF", style="filled")

def createBlankGraph(moduleName):
    """
    Returns an initialized blank graphviz digraph.
    """
    result = Digraph(name=moduleName)
    # We want the graph to be generated vertically
    result.graph_attr['rankdir'] = 'LR'

def checkForSymbolConflicts(moduleName):
    module = importlib.import_module(moduleName)
    return checkForSymbolConflictsRec(module, 0, moduleName, [], dict()) 

def genModuleGraph(moduleName):
    graph = createBlankGraph(moduleName)
    module = importlib.import_module(moduleName)
    walkModuleRecursive(module, 0, graph, moduleName, [])
    graph.render("img/graph")

if __name__ == "__main__":
