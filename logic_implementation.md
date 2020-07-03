---
title: Logic Implementation
layout: default
filename: logic_implementation
--- 
# Logic Implementation

The system _beliefmaker_ takes as input a pointed $$KD45_{(m)}$$ Kripke model, a non-modal formula, and a type of belief.
It returns (one of) the smallest set(s) of agents who have to be removed from the model in order to establish the requested formula as the requested type of belief.
The system's algorithm is strongly based on the system's logical background, as described [elsewhere](https://bick95.github.io/beliefmaker/logical_background).
The relevant Python code can be divided in three parts: a representation of models, a representation of formulas, and the algorithm itself (i.e. from input to output).
In this section, these three parts are discussed in order.


## Kripke Model

The Kripke model is represented in our system as an object of class `Kripke`. 


```python
class Kripke():

  def __init__(self, path=None):
    if path == None:
      # Example mode
      pass
    else:
      self.parse_model(path)
              
        
  def setup(self, real_world, R, V):
    # Assign model
    self.real_world = real_world
    self.R = R
    self.V = V
    self.S = self.states()
    self.agents = sorted(set(R.keys()))
    self.P = sorted(set(V.keys()))


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
    self.setup(model['real_world'], model['R'], model['V'])

    # Print loaded model
    if to_print:
      print(self)


  def assign_model(self, model):

    try:
      model = eval(model.strip())
    except:
      print('Error???')
      raise ModelParsingError('Model\'s syntax invalid!')

    # Assign model
    self.setup(model['real_world'], model['R'], model['V'])

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


  def __deepcopy__(self, memo):
    # Create deep copy of the model
    new_model = Kripke()
    new_model.setup(self.real_world, copy.deepcopy(self.R, memo), copy.deepcopy(self.V, memo))
    return new_model

    
  def states(self):
    # Derive the states from R and V
    yss = [xs for xss in list(self.R.values()) for xs in xss]
    yss = [x for xss in [yss, list(self.V.values())] for xs in xss for x in xs]
    
    states = []
    [states.append(x) for x in yss if x not in states]
    
    return states
    
    
  def remove_agent(self, agent):
    # Remove a single agent from the model
    
    del self.R[agent]
    self.agents.remove(agent)

  
  def remove_non_believers(self, formula):
    non_believers = []
    
    for agent in self.agents:
      if not believes(agent, formula, self):
        non_believers += agent

    for agent in non_believers:
      self.remove_agent(agent)
      
    return non_believers
    

  def is_legal_KD45(self):
    # Check whether the model satisfies seriality, transitivity, and euclideanness
    #   (and so is legal in KD45).
    # Returns a tuple of a boolean and an error message indicating the violation if necessary.
    
    error_msg = 'The model you have provided is not a legal model in KD45(m), since '
    
    # First, seriality (associated with axiom D).
    # According to this requirement, every state should have at least one outgoing accessibility
    #   relation for every agent.
    for state in self.S:
      
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


  def summarize_model(self):
    # Return two alternative descriptions of the model's properties: the agents per state-pair in the
    #   accessibility relations, and the true propositions at each state.

    # Get list of agents per accessibility
    global_accessibilities = {}

    for agent in self.agents:
      for agent_acc in self.R[agent]:
        acc = (agent_acc[0], agent_acc[1])
        if acc in global_accessibilities:
          # There esist a record for a given connection already
          global_accessibilities[acc].append(agent)
        else:
          # The first time that an agent maintains the current relation in quest.
          global_accessibilities[acc] = [agent]

    # Get list of true propositions per state
    global_valuations = {s: [] for s in self.S}
    for p in self.P:
      for state in self.V[p]:
          global_valuations[state].append(p)

    return global_accessibilities, global_valuations
  

  def dict_str_representation(self):
    model = {"real_world": self.real_world, 
             "R": self.R, 
             "V": self.V}
    return str(model)


  def __str__(self):
    # Print current model
    
    summary_entities = ''
    _, valuations = self.summarize_model()
    
    # First, print the set of propositions in the language
    propositions_str = 'Propositions:\tP = {'
    for i in range(len(self.P)):
      if i != 0:
        propositions_str += ', '
      propositions_str += str(self.P[i])
    propositions_str += '}\n'
    summary_entities += propositions_str

    # Second, the set of agents we are concerned with   
    agents_str = 'Agents:\t\tA = {'
    for i in range(len(self.agents)):
      if i != 0:
        agents_str += ', '
      agents_str += str(self.agents[i])
    agents_str += '}\n'
    summary_entities += agents_str
    
    summary_entities += '\nM = <S, R, v> with:\n'
    
    # Third, the set of states in the model
    states_str = 'States:\t\tS = {'
    for i in range(len(self.S)):
      if i != 0:
        states_str += ', '
      states_str += str(self.S[i])
    states_str += '}\n'
    summary_entities += states_str

    # Fourth, the various accessibility relations
    relations_str = 'Relations:\t'
    for i in range(len(self.agents)):
      if i != 0:
        relations_str += '\t\t\t'
      relations_str += 'R_' + str(self.agents[i]) + ' = {'
      for j in range(len(self.R[self.agents[i]])):
        if j != 0:
          relations_str += ', '
        relations_str += '(' + str(self.R[self.agents[i]][j][0]) + ', ' +\
                         str(self.R[self.agents[i]][j][1]) + ')'
      relations_str += '}\n'
    summary_entities += relations_str

    # Fifth, the valuations (as sets of true propositions per state)
    valuations_str = 'Valuation:\t'
    for i in range(len(self.S)):
      if i != 0:
        valuations_str += '\t\t\t'
      valuations_str += 'v(' + str(self.S[i]) + ') = {'
      for j in range(len(valuations[self.S[i]])):
        if j != 0:
          valuations_str += ', '
        valuations_str += str(valuations[self.S[i]][j])
      valuations_str += '}\n'
    summary_entities += valuations_str
    
    summary_entities += '\nReal world:\t' + str(self.real_world) + '\n'
    
    return summary_entities


  def visualize(self, html=False):
    # Visualize the model

    accessibilities, valuations = K.summarize_model()

    print('agents', self.agents)
    print('states', self.S)
    print('propositions', self.P)
    print('accessibilities', accessibilities)
    print('valuations', valuations)

    g = Graph()
    g.add_nodes(valuations)
    g.add_edges(accessibilities)
    if html:
      return g.visualize()
    g.visualize()
```

## Formula

```python
class Formula:

  def __init__(self, formula_str):
    
    self.parse_formula(formula_str)
    
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
    # Parse a string into a formula
    
    def remove_whitespace(formula_str):
      # Remove all whitespace in the string
      result = ''
      for char in formula_str:
        if char not in [' ', '\t', '\n']:
          result += char
      return result
    
    
    def remove_outer_parentheses(formula_str):
      # Remove the outer parentheses to facilitate parsing
    
      # This is only useful if the formula starts and ends with a parenthesis
      if formula_str[0] == '(' and formula_str[len(formula_str)-1] == ')':
        depth = 0
        outer_parentheses = True
        
        # Check if we reach depth 0 before the end; then, there are no outer parentheses
        for char in formula_str:
          if not outer_parentheses:
            return formula_str
          if char == '(':
            depth += 1
          elif char == ')':
            depth -=1
            if depth == 0:
              outer_parentheses = False
        
        if depth != 0:
          raise ParsingError('The numbers of opening and closing parentheses do not match.')
        
        # If we reach this point, depth 0 was only reached at the end
        return remove_outer_parentheses(formula_str[1:len(formula_str)-1])
          
      return formula_str
    
    
    formula_str = remove_whitespace(formula_str)
    
    # These three exceptional cases are problematic because they lead to IndexErrors
    if formula_str == '()':
      raise ParsingError('Two parentheses do not a formula make.')
    if formula_str == '~':
      raise ParsingError('One negation does not a formula make.')
    if formula_str == '':
      raise ParsingError('The empty formula cannot be parsed.')
    
    formula_str = remove_outer_parentheses(formula_str)

    record_lefthand = True
    lefthand = ''
    depth = 0

    for char,i in zip(formula_str, range(len(formula_str))):
     
      # Recording the lefthand side; keep track of parentheses
      if record_lefthand:
        if char == '(':
          depth += 1
        if char == ')':
          depth -= 1
        # Record connectives
        if char in ['&', '|', '-', '<', '>'] and depth == 0:
          # The first connective at depth 0 is considered the main connective
          record_lefthand = False
          symbol = ''
        else:
          lefthand += char
      
      # If we are not recording the lefthand side, there's 2 options:
      if not record_lefthand:
        # 1. We are recording the main connective
        if char in ['&', '|', '-', '<', '>']:
            symbol += char
            continue
        # 2. We are done recording the main connective;
        #    the rest is considered the righthand side
        self.mc = symbol
        self.subf = [Formula(lefthand), Formula(formula_str[i:])]
        return
     
    # If we have recorded the entire formula as the lefthand side, 3 options:
    if record_lefthand:
      # 1. The main connective is negation
      if lefthand[0] == '~':
        if len(lefthand) == 1:
          raise ParsingError('One negation does not a formula make.')
        self.mc = '~'
        self.subf = [Formula(lefthand[1:])]
        return
      # 2. The formula is propositional
      if lefthand.isalnum():
        self.mc = ''
        self.subf = [lefthand]
        return
      # 3. The user made a mistake
      else:
        raise ParsingError('I expected the formula \'%s\' to be propositional' % formula_str +\
                                ', but it is not alphanumeric.' )
    else:
      raise ParsingError('Formula ended with symbol: ' + symbol)


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

## Main Algorithm

### Truth Definition of Non-Modal Formulas

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

### Transitive Closure


```python
def t_closure(R):
  # Return transitive closure of the union of a number of accessibility relations
  
  # Obtain union, then iteratively add new relations to obtain the transitive closure
  closure = union(R)
  
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
  

def union(R):
  # Return the union of a number of accessibility relations

  # First combine all elements of the accessibility relations in one list
  total = []
  
  for ls in R.values():
    total += ls
    
  # Remove duplicate elements to obtain the union
  union = []
  [union.append(x) for x in total if x not in union]
  
  return union
```

### Belief and Common Belief


```python
def believes(agent, formula, M):
  # Checks whether an agent believes a formula in a pointed model
  
  for [s, t] in M.R[agent]:
    if s == M.real_world:
      if not check_formula_local(formula, M, t):
          return False
          
  return True


def common_belief(M, formula):
  # Check whether a non-modal formula is a common belief in a pointed model
  
  for [s, t] in t_closure(M.R):
    if s == M.real_world:
      if not check_formula_local(formula, M, t):
        return False

  return True
```

### Main Algorithm


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


def analyse(M, formula, belief_type = "common"):
  # Returns a list containing tuples.
  # Each tuple contains a model M and the agents that were removed from the original pointed model to obtain M.
  # The number of agents is the same for each tuple.
  # It corresponds to the minimal number of agents which need to be removed from the original model in order for
  #   the proposition to be common/general belief in that pointed model.
  
  # If we're given a string, first make it a formula
  if isinstance(formula, str):
    formula = Formula(formula)

  # Check if the model satisfies the requirements of KD45
  if M.is_legal_KD45()[0]:

    # Check if all propositions in the formula are in the language
    for p in formula.propositions():
      if p not in M.P:
        raise PropositionError('The proposition %s is not in the language.' % p)
    
    # If this is all in order, generate (a) solution(s)
    # Start by removing all non-believers; they will have to be removed anyhow
    agents_removed = M.remove_non_believers(formula)
    result = []
    
    # If all agents are non-believers, there is no solution
    if len(M.agents) == 0:
      return result
      
    if belief_type == "general":
      # There is always exactly 1 (or no) such solution to the general belief problem, so we can quit now
      result += [(M, agents_removed)]
      return result
    
    # Else: continue by removing 0 agents, then 1, then 2, etc, until we find a solution
    for i in range(len(M.agents)):
    
      for xs in sublists(M.agents, i):
        M2 = copy.deepcopy(M)
        
        for x in xs:
          M2.remove_agent(x)
        
        # Append every (model, agents) combination that constitutes a solution
        if common_belief(M2, formula):
          result.append((M2,agents_removed + xs))
      
      if result != []:
        # Return all solutions in which a minimum number of agents is removed
        return result
          
    return result
  else:
    raise ModelError(M.is_legal_KD45()[1])
```