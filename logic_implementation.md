---
title: Logic Implementation
layout: default
filename: logic_implementation
--- 
# Logic Implementation

```python
# Path declaration
path_to_shared = ''
```


```python
# List of connectives implemented in the system
known_connectives = ['', '~', '&', '|', '->', '<->']
```


```python
# Imports
import os
import re
import json
import copy
import math
import itertools
import numpy as np
# Plotting
from matplotlib import patches
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
```

**Error types**


```python
class ParsingError(ValueError):
  __module__ = 'builtins'

class ModelError(ValueError):
  __module__ = 'builtins'

class PropositionError(ValueError):
  __module__ = 'builtins'

class ModelParsingError(ValueError):
  __module__ = 'builtins'
```

# **Plotting**


```python
import math

def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    # Thanks to: https://stackoverflow.com/a/34374437/11478452
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy
```


```python
import operator

def vector_arithmetics(vec, modifier, val=None):
  # Define math operators
  ops = { "+": operator.add, 
          "-": operator.sub,
          "mod": operator.mod,
          "%": operator.mod,
          "/": operator.truediv,
          "*": operator.mul,
          "pow": operator.pow,
          "norm": "norm"
         }

  #print('Vec operation -->', vec, modifier, val)

  # Prepare vector operation
  assert(isinstance(modifier, str))
  vec = np.asarray(vec)

  if modifier == "norm":
    return vec / np.sum(np.abs(vec))

  # val can only be none for normalization
  if val is not None:

    # Retrieve math operator
    op = ops[modifier]

    if not (isinstance(val, tuple) or isinstance(val, list)):
      # Modifier is a scalar
      return op(vec, val)
    
    # Modifier is itself vector
    val = np.asarray(val)
    return op(vec, val)

    raise ValueError('val cannot be none, except when normalizing vec!')
```


```python
class Graph():
  def __init__(self):
    self.nodes = {}   # {node_id: sattelite_data}
    self.edges = {}   # {edge_id: sattelite_data}

  def add_nodes(self, nodes, attributes=None):
    # Assign self.nodes, where self.nodes is a dict of form: {node_id: sattelite_data}
    if attributes:
      assert(isinstance(nodes, list))
      assert(len(nodes) == len(attributes))
      self.nodes = {nodes[i]: attributes[i] for i in range(len(nodes))}
    elif isinstance(nodes, list):
      self.nodes = {node: None for node in nodes}
    else:
      assert(isinstance(nodes, dict))
      self.nodes = nodes

  def add_edges(self, edges, attributes=None):
    # Assign self.edges, where self.edges is a dict of form: {edge_id: sattelite_data}
    if attributes:
      assert(isinstance(edges, list))
      assert(len(edges) == len(attributes))
      self.edges = {edges[i]: attributes[i] for i in range(len(edges))}
    elif isinstance(edges, list):
      self.edges = {node: None for node in edges}
    else:
      assert(isinstance(edges, dict))
      self.edges = edges

  def add_node(self, node, attribute=None):
    # May overwrite existing node
    self.nodes[node] = attribute

  def add_edge(self, edge, attribute=None):
    # May overwrite existing edge
    self.edges[edge] = attribute
  
  def delete_node(self, node):
    # TODO: haven't tested/checked yet. Focus was primarily on visualizing so far
    raise Warning('Untested function delete_node.')
    del self.nodes[node]
    for edge in self.edges:
      if node in edge:
        del edge
  
  def delete_edge(self, edge):
    # TODO: haven't tested/checked yet. Focus was primarily on visualizing so far
    raise Warning('Untested function delete_edge.')
    for e in self.edges:
      if e == edge:
        del e
        break
  
  def visualize(self, html=False):
    enumerated_nodes = {i: n for i, n in enumerate(sorted(self.nodes))}
    enumerated_edges = {i: e for i, e in enumerate(sorted(self.edges))}
    rev_enumerated_nodes = {n: i for i, n in enumerate(sorted(self.nodes))}
    rev_enumerated_edges = {e: i for i, e in enumerate(sorted(self.edges))}

    # Plot nodes
    colors = (0,0,0)
    nodes = len(self.nodes)
    step_size = 360/nodes
    thetas = np.arange(0,360,step_size)
    r_min = 5
    d = 4*r_min
    if len(thetas) <= 2:
      r_maj = d
    else:
      d_s = math.pow(d,2)
      d_1 = math.pow(math.cos(np.deg2rad(thetas[1]))-1, 2)
      d_2 = math.pow(math.sin(np.deg2rad(thetas[1])), 2)
      r_maj = math.sqrt(d_s / (d_1 + d_2))

    x = [math.cos(np.deg2rad(t))*r_maj for t in thetas]
    y = [math.sin(np.deg2rad(t))*r_maj for t in thetas]

    fig = plt.figure()
    plt.scatter(x, y, c='lightblue', alpha=0.8, s=r_maj*20)
    plt.margins(0.2)

    # Print nodes' satellite data to plot
    for i in range(len(self.nodes)):
      string = str(enumerated_nodes[i]) + '\n' + str(self.nodes[enumerated_nodes[i]])
      plt.text(x[i]*1., y[i]*1., string, horizontalalignment='center', verticalalignment='center', weight="bold")

    # Edge visualization
    
    style="wedge"
    kw_lin = dict(arrowstyle=style, shrinkA = 0, shrinkB = 0, color="#808080", label='', connectionstyle="arc3,rad=.15")
    style="simple,head_width=5,head_length=8"
    kw_arw = dict(arrowstyle=style, shrinkA = 0, shrinkB = 0, color="#808080", label='', connectionstyle="arc3,rad=.15")

    # Visualize non-reflexive edges
    for i in range(len(self.edges)):
      edge = enumerated_edges[i]
      if edge[0] != edge[1]:
        ptA = (x[rev_enumerated_nodes[edge[0]]], y[rev_enumerated_nodes[edge[0]]])
        ptB = (x[rev_enumerated_nodes[edge[1]]], y[rev_enumerated_nodes[edge[1]]])

        mid = vector_arithmetics(ptA, '+', ptB)
        mid = vector_arithmetics(mid, '/', 2)
        #plt.plot(mid[0], mid[1], 'ro')
        
        dirA = vector_arithmetics(ptA, '-', mid)
        norm_dirA = vector_arithmetics(dirA, 'norm')
        #norm_dirA = vector_arithmetics(norm_dirA, '*', 0.5) # Only shlight move towards A
        mid_close = vector_arithmetics(mid, '+', norm_dirA)
        #plt.plot(mid_close[0], mid_close[1], 'bo')

        mid_rotated = rotate(mid_close, mid, math.radians(-90))
        #plt.plot(mid_rotated[0], mid_rotated[1], 'yo')

        displacement_dir = vector_arithmetics(mid_rotated, '-', mid_close)
        displacement_dir = vector_arithmetics(displacement_dir, 'norm')  # wrt origin

        scaled_displacement = vector_arithmetics(displacement_dir, '*', 4.)

        new_mid = vector_arithmetics(mid_close, '+', scaled_displacement)

        mid = new_mid

        a = patches.FancyArrowPatch(ptA, mid, **kw_lin)
        b = patches.FancyArrowPatch(mid, ptB, **kw_arw)

        plt.gca().add_patch(a)
        plt.gca().add_patch(b)

        #plt.text(mid[0], mid[1], self.edges[edge], 
        #         horizontalalignment='center', 
        #         verticalalignment='center')

        bbox_props = dict(boxstyle="round,pad=0.3", fc="lightgray")#, ec="b", lw=2)
        plt.plot(mid[0], mid[1])  # Set fake point to make sure text is not going to end up outside plotted region 
        plt.text(mid[0], mid[1], self.edges[edge], ha="center", va="center", bbox=bbox_props)
        
    # Visualize reflexive edges
    for i in range(len(self.edges)):
      edge = enumerated_edges[i]

      if edge[0] == edge[1]:
        pt = (x[rev_enumerated_nodes[edge[0]]], y[rev_enumerated_nodes[edge[0]]])

        pt_dir = vector_arithmetics(pt, 'norm')
        scaled_pt_dir = vector_arithmetics(pt_dir, '*', 20)

        text_pos = vector_arithmetics(pt, '+', scaled_pt_dir)

        a = patches.FancyArrowPatch(pt, text_pos, **kw_lin)
        b = patches.FancyArrowPatch(text_pos, pt, **kw_arw)

        plt.gca().add_patch(a)
        plt.gca().add_patch(b)

        plt.plot(text_pos[0], text_pos[1]) # Set fake point to make sure text is not going to end up outside plotted region 
        bbox_props = dict(boxstyle="round,pad=0.3", fc="lightgray")#, ec="b", lw=2)
        plt.text(text_pos[0], text_pos[1], self.edges[edge], ha="center", va="center", 
                 #rotation=45, size=15,
            bbox=bbox_props)

    plt.axis('off')

    if html:
      return fig
    plt.show()

```

# **Definition of Knowledge Structure**

**Kripke Model**


```python
class Kripke():

  def __init__(self, path=None):
    if path == None:
      # Example mode
      self.parse_model()
    else:
      self.parse_model(path)


  def parse_model(self, path=(path_to_shared + 'model_5.txt'), to_print = False):
    # Load model from file
    model = {}
    try:
      with open(path) as json_file:
        model = json.load(json_file)
    except Exception as e:
      print('Exception occurred! Updating current model aborted! Exception:', e)

    # Check whether dictionary is empty 
    if to_print:
      print('MODEL', model)
    if not bool(model):
      raise Warning('Empty model provided. Updating current model aborted!')

    # Assign model
    self.real_world = model['real_world']
    self.R = model['R']
    self.V = model['V']

    # Print loaded model
    if to_print:
      print(self)


  def assign_model(self, model):

    try:
      model = eval(model.strip())
    except:
      raise ModelParsingError('Model\'s syntax invalid!')

    # Assign model
    self.real_world = model['real_world']
    self.R = model['R']
    self.V = model['V']

    # Print loaded model
    print(self)


  def save(self, name='model_1.txt', path=path_to_shared, overwrite=False):
    self.save_model(name, path, overwrite)


  def save_model(self, name='model_1.txt', path=path_to_shared, overwrite=False):
    # Choose model name
    file_name = path + name

    # Check if file name is acceptable or needs refinement
    if '.' in file_name:
      # File extension does not need to be added, but divided for further processing
      parts = file_name.split('.')
      non_extsn = '.'.join(parts[0:-1])
      extension = '.' + parts[-1]
    else:
      # No file extension provided, so add it to file name structure
      non_extsn = file_name
      extension = '.txt'

    if not overwrite and os.path.exists(file_name):
      # Provided file name exists already: Adapt name to avoid overwriting if wished
      print('File name exists already! Going to change name.\n' + 
            '\t To overwrite existing files, save with \'overwrite=True\'.\n')

      pattern = '[\d]+' # Integer search pattern
      nums = []
      if re.search(pattern, non_extsn) is not None:
        # There is an integer in file name. If int==last position, increment & save
        
        for catch in re.finditer(pattern, non_extsn):
          # Retrieve all integer parts from provided file name
          nums.append(catch) 
        
        # Select last detected integer
        last_num_str = nums[-1].group(0)
        last_occ_idx = non_extsn.rfind(last_num_str)

        if last_occ_idx+len(last_num_str) < len(non_extsn):
          # Integer is not in last position of file name, so simply append '_1'
          file_name = former + '_1' + extension
        else:
          # Integer detected in last position of provided file name
          former = non_extsn[:last_occ_idx]  # Non-integer-part
          num = int(non_extsn[last_occ_idx : last_occ_idx+len(last_num_str)]) # Integer

          # Construct a candidate file name containing int in last position and 
          # keep incrementing int until a new file name has been determined
          file_name = former + str(num) + extension
          while os.path.exists(file_name):
            num += 1
            file_name = former + str(num) + extension
      else:
        # Integer is no integer in the file name, so simply append '_1'
        file_name = former + '_1' + extension
    else:
      # If overwrite or file name didn't exist yet, keep provided file name
      file_name = non_extsn + extension

    # If folder-path doesn't exist yet, create it
    if not os.path.exists(path):
      os.mkdirs(path)

    # Define model to be saved
    model = { 'real_world': self.real_world, 'R': self.R, 'V': self.V }

    # Save model
    with open(file_name, 'w') as outfile:
      json.dump(model, outfile)

    print('Saved to:\n', file_name)


  def update(self, path):
    self.parse_model(path)

    
  def states(self):
    # Derive the states from R and V
    yss = [xs for xss in list(self.R.values()) for xs in xss]
    yss = [x for xss in [yss, list(self.V.values())] for xs in xss for x in xs]
    
    states = []
    [states.append(x) for x in yss if x not in states]
    
    return states
    

  def is_legal_KD45(self):
    # Check whether the model satisfies seriality, transitivity, and euclideanness
    #   (and so is legal in KD45).
    # Returns a tuple of a boolean and an error message indicating the violation if necessary.
    
    error_msg = 'The model you have provided is not a legal model in KD45(m), since '
    
    # First, seriality (associated with axiom D).
    # According to this requirement, every state should have at least one outgoing accessibility
    #   relation for every agent.
    for state in self.states():
      
      serial_check = False
      
      for agent in self.R.keys():
        
        for relation in self.R[agent]:
          if relation[0] == state:
            # There is a relation from this state for this agent; i.e. "so far, so good"
            serial_check = True
            break
        
        if serial_check:
          serial_check = False
        else:
          # If we ever end up here, there is some state from which not all agents have a relation.
          # This means there is a violation of seriality.
          error_msg += 'seriality was violated.\n'
          error_msg += 'Problem: no relation from state ' + str(state) + ' for agent ' + agent + '.'
          return (False, error_msg)
    
    # Now, transitivity (associated with axiom A4).
    # According to this requirement, for every x, y, z and every agent: if xRy and yRz, then xRz.
    
    for agent in self.R.keys():
      
      relations = self.R[agent]
      for [x,y],[z,w] in itertools.product(relations, relations):
        if y==z and [x,w] not in relations:
          # There is a violation of transitivity.
          error_msg += 'transitivity was violated.\n'
          error_msg += 'Problem: ' + str([x,w]) + ' not in R_' + agent + '.'
          return (False, error_msg)
          
    # Last, euclideanness (associated with axiom A5).
    # According to this requirement, for every x, y, z and every agent: if xRy and xRz, then yRz.
    
    for agent in self.R.keys():
      
      relations = self.R[agent]
      for [x,y],[z,w] in itertools.product(relations, relations):
        if x==z and [y,w] not in relations:
          # There is a violation of euclideanness.
          # Note that in this implementation, we don't have to explicitly check for [w,y], since
          #   ([z,w],[x,y]) will also be an element of the cartesian product.
          error_msg += 'euclideanness was violated.\n'
          error_msg += 'Problem: ' + str([y,w]) + ' not in R_' + agent + '.'
          return (False, error_msg)
    
    # If we reach this point, no violation was detected, so the model is legal.
    
    return (True, '')
    

  def is_legal_proposition(self, proposition):
    _, _, propositions, _, _ = self.summarize_model()
    for p in proposition:
      if p not in propositions:
        return False
    return True

  def dict_str_representation(self):
    model = {"real_world": self.real_world, 
             "R": self.R, 
             "V": self.V}
    return str(model)

  def summarize_model(self):
    # Get list of agents
    agents = [a for a in self.R]
    agents = sorted(set(agents))

    # Get list of states
    states = []
    for agent in self.R:
      agent_relations = self.R[agent]
      for relation in agent_relations:
        for state in relation:
          states.append(state)
    states = sorted(set(states))

    # Get list of propositions
    propositions = [p for p in self.V]
    propositions = sorted(set(propositions))

    # Get list of agents per accessibility
    global_accessibilities = {}

    for agent in agents:
      for agent_acc in self.R[agent]:
        acc = (agent_acc[0], agent_acc[1])
        if acc in global_accessibilities:
          # There esist a record for a given connection already
          global_accessibilities[acc].append(agent)
        else:
          # The first time that an agent maintains the current relation in quest.
          global_accessibilities[acc] = [agent]

    global_valuations = {s: [] for s in states}
    for p in propositions:
      for state in self.V[p]:
          global_valuations[state].append(p)

    return agents, states, propositions, global_accessibilities, global_valuations

  def __str__(self):
    # Print current model
    
    summary_entities = ''
    agents, states, propositions, _, valuations = self.summarize_model()
    
    # First, print the set of propositions in the language
    propositions_str = 'Propositions:\tP = {'
    for i in range(len(propositions)):
      if i != 0:
        propositions_str += ', '
      propositions_str += str(propositions[i])
    propositions_str += '}\n'
    summary_entities += propositions_str

    # Second, the set of agents we are concerned with   
    agents_str = 'Agents:\t\tA = {'
    for i in range(len(agents)):
      if i != 0:
        agents_str += ', '
      agents_str += str(agents[i])
    agents_str += '}\n'
    summary_entities += agents_str
    
    summary_entities += '\nM = <S, R, v> with:\n'
    
    # Third, the set of states in the model
    states_str = 'States:\t\tS = {'
    for i in range(len(states)):
      if i != 0:
        states_str += ', '
      states_str += str(states[i])
    states_str += '}\n'
    summary_entities += states_str

    # Fourth, the various accessibility relations
    relations_str = 'Relations:\t'
    for i in range(len(agents)):
      if i != 0:
        relations_str += '\t\t\t'
      relations_str += 'R_' + str(agents[i]) + ' = {'
      for j in range(len(self.R[agents[i]])):
        if j != 0:
          relations_str += ', '
        relations_str += '(' + str(self.R[agents[i]][j][0]) + ', ' +\
                         str(self.R[agents[i]][j][1]) + ')'
      relations_str += '}\n'
    summary_entities += relations_str

    # Fifth, the valuations (as sets of true propositions per state)
    valuations_str = 'Valuation:\t'
    for i in range(len(states)):
      if i != 0:
        valuations_str += '\t\t\t'
      valuations_str += 'v(' + str(states[i]) + ') = {'
      for j in range(len(valuations[states[i]])):
        if j != 0:
          valuations_str += ', '
        valuations_str += str(valuations[states[i]][j])
      valuations_str += '}\n'
    summary_entities += valuations_str
    
    summary_entities += '\nReal world:\t' + str(self.real_world) + '\n'
    
    return summary_entities


  def __deepcopy__(self, memo):
    # Create deep copy of the model
    new_model = Kripke()
    new_model.real_world = self.real_world
    new_model.R = copy.deepcopy(self.R, memo)
    new_model.V = copy.deepcopy(self.V, memo)
    return new_model


  def visualize(self, html=False):
    # Visualize the model

    agents, states, propositions, accessibilities, valuations = K.summarize_model()

    print('agents', agents)
    print('states', states)
    print('propositions', propositions)
    print('accessibilities', accessibilities)
    print('valuations', valuations)

    g = Graph()
    g.add_nodes(valuations)
    g.add_edges(accessibilities)
    if html:
      return g.visualize()
    g.visualize()
```

# **Definition of Formula**

**Class**


```python
class Formula:

  def __init__(self, formula_str):
    
    try:
      self.parse_formula(formula_str)
    except ParsingError:
      # Give it a second try with outer parentheses
      self.parse_formula('('+ formula_str + ')')
    
    # If the main connective is unknown, throw an error
    if not (self.mc in known_connectives):
      raise ParsingError('The symbol \'%s\' is unknown to me.' % self.mc)
      
          
  def __eq__(self, other):
    # For comparing two formulas regardless of whether they're the same object
    return self.mc == other.mc and self.subf == other.subf


  def __str__(self):
    # Print current formula
    
    if self.mc == '':
      return self.subf[0]
      
    if self.mc == '~':
      return self.mc + str(self.subf[0])
      
    if self.mc in ['&', '|', '->', '<->']:
      return '(' + str(self.subf[0]) + ' ' + self.mc + ' ' + str(self.subf[1]) + ')'
    

  def parse_formula(self, formula_str):
    # Parse a string into a main connective (self.mc) and subformulas (self.subf)
    # The function is rather forgiving of user errors, ignoring and ``fixing''
    #   many mistakes regarding parentheses. It is therefore good practice to 
    #   print the result, since that may be different from the intended formula
    #   if the original formula was not legal.

    depth = 0
    record_lefthand = False
    record_righthand = False
    record_symbol = False
    
    for char,i in zip(formula_str, range(len(formula_str))):
      
      # Ignore whitespace
      if char in [' ', '\t', '\n']:
        continue
      
      # Opening parentheses indicate we're dealing with a binary connective
      if char == '(':
        depth += 1
        # The left side of the binary connective starts after the first '('
        if depth == 1:
          record_lefthand = True
          lefthand = ''
          continue

      # In case of a negation sign    
      if char == '~':
        # Only take special action if it's outside of parentheses
        if depth == 0:
          self.mc = '~'
          self.subf = [Formula(formula_str[1:])]
          return
      
      # In case of a binary connective, one or more characters in length
      if char in ['&', '|', '-', '<', '>']:
        # If it's the main connective, (start) read(ing) it as the mc
        if record_lefthand and depth == 1:
          record_lefthand = False
          record_symbol = True
          symbol = ''
        if record_symbol:
          symbol += char
          continue
      
      # If we're done reading the mc, switch to the righthand side
      if char not in ['&', '|', '-', '<', '>']:
        if record_symbol:
          record_symbol = False
          record_righthand = True
          righthand=''
      
      # Closing parentheses indicate we're done dealing with a binary connective
      if char == ')':
        depth -= 1
        # After the final closing parentheses
        if depth == 0:
          # If we have characters left
          if len(formula_str[i:]) > 1:
            # Raise an error unless it's just superfluous closing parentheses
            for char2 in formula_str[(i+1):]:
              if char != ')':
                raise ParsingError('The following characters were ignored: %s\nMaybe check the parentheses?'\
                                % formula_str[(i+1):])
          
          # If we were not recording the lefthand side, set mc and figure out the subformulas
          if not record_lefthand:
            self.mc = symbol
            self.subf = [Formula(lefthand), Formula(righthand)]
            return

          # Else, last resort: maybe there are superfluous opening parentheses (see if-statement outside loop)
          if formula_str[:2] == '((':
            break
          
          # Else, we don't know what to do
          raise ParsingError('Formula %s not recognized. Maybe check the parentheses?' % formula_str)
      
      # Recording the lefthand side (or righthand in case of negation)
      if record_lefthand:
        lefthand += char
        continue
      
      # Recording the righthand side
      if record_righthand:
        righthand += char
        continue
      
      # An alphanumeric character outside of parentheses suggests the formula is propositional
      if depth == 0 and char.isalnum():
        # If it's not, we don't know what to do
        if not formula_str.isalnum():
          raise ParsingError('I expected the formula \'%s\' to be propositional' % formula_str +\
                                ', but it is not alphanumeric.\nMaybe check the parentheses?' )
        # If it is, we're done (base case)
        self.mc = ''
        self.subf = [formula_str]
        return
    
    # If the entire string has been processed but we're not done yet, perhaps there were
    #   superfluous opening parentheses. Let's try removing one and see what happens
    if formula_str[0] == '(':
      self.parse_formula(formula_str[1:])


  def propositions(self):
    # Return a sorted list of the propositions that occur in the formula
    
    propositions = []

    # Recursively determine all propositions
    for A in self.subf:
      if isinstance(A, str):
        if A not in propositions:
          propositions += [A]
      else:
        propositions += A.propositions()
       
    return sorted(propositions)
```

# **Main Algorithm**

**Follow the truth definition**


```python
def check_formula_local(formula, M, state):
  # Checks whether a non-modal formula is true in a state
  
  # Basis: for propositions, check directly in the model
  if formula.mc == '':
    return state in M.V[formula.subf[0]]
    
  # Semantics of negation
  if formula.mc == '~':
    return not check_formula_local(formula.subf[0], M, state)
    
  # Semantics of disjunction
  if formula.mc == '|':
    if check_formula_local(formula.subf[0], M, state):
      return True
    return check_formula_local(formula.subf[1], M, state)
    
  # Semantics of conjunction
  if formula.mc == '&':
    if not check_formula_local(formula.subf[0], M, state):
      return False
    return check_formula_local(formula.subf[1], M, state)
    
  # Semantics of implication
  if formula.mc == '->':
    if not check_formula_local(formula.subf[0], M, state):
      return True
    return check_formula_local(formula.subf[1], M, state)
  
  # Semantics of bi-implication
  if formula.mc == '<->':
    if check_formula_local(formula.subf[0], M, state) == check_formula_local(formula.subf[1], M, state):
      return True
    return False
```

**Transitive closure**


```python
def t_closure(R):
  # Return transitive closure of the union of a number of accessibility relations
  
  # First combine all elements of the accessibility relations in one list
  total = []
  
  for ls in R.values():
    total += ls
    
  # Remove duplicate elements to obtain the union
  union = []
  [union.append(x) for x in total if x not in union]
  
  # Then iteratively add new relations to obtain the transitive closure
  closure = union
  
  while True:  
    element_added = False
    for [x,w],[v,y] in itertools.product(closure,closure):
      if w==v and [x,y] not in closure:
        closure.append([x,y])
        element_added = True
    
    # If an iteration does not lead to new relations, we're done
    if not element_added:
      break
  
  return closure

```

**Common belief**


```python
def common_belief(M, formula):
  # Check whether a non-modal formula is a common belief in a pointed model
  for [s, t] in t_closure(M.R):
    if s == M.real_world:
      if not check_formula_local(formula, M, t):
        return False

  return True
```

**Sublists (for use in the analyse function)**


```python
def sublists(ls, n):
  # Returns all sublists of length n (order does not matter)
  
  def sublists_rec(ls, selected, n):
    # Recursively finds and returns a list of requested sublists
    
    if n == 0:
      return [selected]
    
    result = []
    xs = copy.deepcopy(ls)
    
    # Popping the elements means we only further consider the part of the list after the selected element
    for i in range(len(xs)):
      x = xs.pop(0)
      result += sublists_rec(xs, selected + [x], n-1)
    
    return result

  if n > len(ls):
    raise ValueError('Requested sublist length exceeds list length (' + str(n) + ' > ' + str(len(ls)) + ')')
    
  return sublists_rec(ls, [], n)
```

**Main function**


```python
def analyse(M, formula):
  # Returns a list containing tuples.
  # Each tuple contains a model M and the agents that were removed from the original pointed model to obtain M.
  # The number of agents is the same for each tuple.
  # It corresponds to the minimal number of agents which need to be removed from the original model in order for
  #   the proposition to be common belief in that pointed model.
  
  # If we're given a string, first make it a formula
  if isinstance(formula, str):
    formula = Formula(formula)

  # Check if the model satisfies the requirements of KD45
  if M.is_legal_KD45()[0]:

    # Check if all propositions in the formula are in the language
    _, _, language, _, _ = M.summarize_model()
    for p in formula.propositions():
      if p not in language:
        raise PropositionError('The proposition %s is not in the language.' % p)
    
    # If this is all in order, generate (a) solution(s)
    agents = list(M.R.keys())
    result = []
    
    # First remove 0 agents, than 1, than 2, etc, until we find a solution
    for i in range(len(agents)):
    
      for xs in sublists(agents, i):
        M2 = copy.deepcopy(M)
        
        for x in xs:
          del M2.R[x]
        
        # Append every model - agents combination that constitutes a solution
        if common_belief(M2, formula):
          result.append((M2,xs))
      
      if result != []:
        return result
          
    return result
  else:
    raise ModelError(M.is_legal_KD45()[1])
```

**Wrapper**


```python
def solve(formula, number=5, to_print = True):
  # A sort of wrapper for ease of implementation and testing
  
  path=(path_to_shared + 'model_' + str(number) + '.txt')
  M = Kripke(path)
  
  print('To check: how to establish ' + str(formula) + ' as common belief in the following model:\n\n'\
    + str(M) + '\nSolution:')
  
  results = analyse(M, formula)
  
  if to_print and results:
    print(results[0][0])
  
  return results
 
```

**For testing**


```python
def query_formula():
  # Ask for a formula and turn it into a Formula

  ans = input('\nPlease enter a formula to be parsed: ')
  return Formula(ans)
```


```python
solve(query_formula())
print('-----')
analyse(Kripke(), Formula('p'))
```

    
    Please enter a formula to be parsed: ~p
    To check: how to establish ~p as common belief in the following model:
    
    Propositions:	P = {p, q, r}
    Agents:		A = {a, b, c}
    
    M = <S, R, v> with:
    States:		S = {1, 2, 3}
    Relations:	R_a = {(1, 2), (1, 3), (2, 2), (3, 3), (2, 3), (3, 2)}
    			R_b = {(1, 3), (2, 3), (3, 3)}
    			R_c = {(1, 1), (2, 2), (3, 3), (3, 1), (1, 3)}
    Valuation:	v(1) = {r}
    			v(2) = {p, r}
    			v(3) = {p, q, r}
    
    Real world:	1
    
    Solution:
    -----





    [(<__main__.Kripke at 0x7f62bf3dd898>, ['c'])]


