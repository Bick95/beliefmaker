---
title: Logic Implementation
layout: default
filename: logic_implementation
--- 
# Logic Implementation

The system _beliefmaker_ takes as input a pointed $$KD45_{(m)}$$ Kripke model, a non-modal formula, and a type of belief.
It returns (one of) the smallest subset(s) of agents who have to be removed from the model in order to establish the requested formula as the requested type of belief.
The system's algorithm is strongly based on the system's logical background, as described [elsewhere](https://bick95.github.io/beliefmaker/logical_background).
The relevant Python code can be divided in three parts: a representation of models, a representation of formulas, and the algorithm itself (i.e. from input to output).
In this section, these three parts are discussed in order, and selected parts of the code are shown.


## Kripke Model

### Overview

The Kripke model is represented in our system as an object of class `Kripke`.
Like a Kripke model, this object has variables for the real world, the accessibility relations, the valuations, and the states.
Unlike a Kripke model, the object also has variables for the agents and the propositions that are in the language.
Only `real_world`, `R`, and `V` are provided by the user. The other variables are inferred:


```python
  def setup(self, real_world, R, V):
    # Assign model
    self.real_world = real_world
    self.R = R
    self.V = V
    self.S = self.states()
    self.agents = sorted(set(R.keys()))
    
    #Propositions
    self.P = sorted(set(V.keys()))
    
  
  def states(self):
    # Derive the states from R and V
    yss = [xs for xss in list(self.R.values()) for xs in xss]
    yss = [x for xss in [yss, list(self.V.values())] for xs in xss for x in xs]
    
    states = []
    [states.append(x) for x in yss if x not in states]
    
    return states
  
```

### Removing agents

The Kripke class contains functions which remove agents from the model.
Of these `remove_agent` is only used when trying to establish common belief, whereas `remove_non_believers` is always used.


```python
  
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
```    

### Legality check

The Kripke class supports any kind of epistemic Kripke model; however, _beliefmaker_ is based specifically on $$KD45_{(m)}$$.
Therefore, the class is equipped with a function which checks whether the model actually satisfies the requirements of this logic.
Recall that these requirements are seriality, transitivity, and euclideanness; these are checked in order, and if any one of them fails, a sensible error message is returned.

```python
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
```

## Formula

### Overview

Any non-modal well-formed formula can be represented in our system as an object of class `Formula`.
A formula has two variables: its main connective, and one or two subformulas, each of which is also a formula, or a string representing a proposition.
In this way, formulas are recursively defined.
The main connective can be either negation, conjunction, disjunction, implication, bi-implication, or nothing - in which case the formula is atomic, and so the subformula will be a string.
The recursive nature of the Formula class is especially clear in its `__str__` function:

```python

  def __str__(self):
    # Print current formula
    
    if self.mc == '':
      return self.subf[0]
      
    if self.mc == '~':
      return self.mc + str(self.subf[0])
      
    if self.mc in ['&', '|', '->', '<->']:
      return '(' + str(self.subf[0]) + ' ' + self.mc + ' ' + str(self.subf[1]) + ')'
```

### Parsing

When parsing a formula from a string, we keep track of and properly handle parentheses.
However, if the formula is ambiguous, pairs of parentheses are added to disambiguate it, starting from the right side.
For example, the string `p & q -> r | s` would be parsed as if it said `p & (q -> (r | s))`.

```python
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
```


### Propositions

The Formula class is equiped with a function `propositions`, which returns a list of all propositions occurring in the formula.
This list is useful for determining whether the formula is legal in the language implicitly defined by the input model.

```python
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

### Overview

The main algorithm on which _beliefmaker_ is based is encapsulated in the `analyse` function.
This function takes as input a model, a formula or a string to turn into a formula, and a type of belief.
It then follows the following algorithm:

1. Parse the input string into a formula if need be.
2. Check if the input model satisfies the requirements of $$KD45_{(m)}$$. If not, return an error; else, continue.
3. Check if the formula is legal in the language. If not, return an error; else, continue.
4. Remove all agents from the pointed model who do not believe the formula is true.
5. Check if there are any agents left. If not, return that there is no solution; else, continue.
6. At this point, all agents in the model believe that the formula is true; therefore, we have established general belief.
Thus, if the requested belief type is "general", we are done; else, continue.
7. Set the counter to $$i = 0$$.
8. Generate all models with $$i$$ agents removed.
9. Check if the formula is common belief in any of the resulting pointed models. If it is, return the solutions; else continue.
10. If $$i < m - 1$$, increase $$i$$ by 1 and return to step 8; else return that there is no solution.

This algorithm is guaranteed to find the least number of agents which need to be removed to establish the requested formula as general or common belief in the input model.


```python
def analyse(M, formula, belief_type = "common"):
  # Returns a list containing tuples.
  # Each tuple contains a model M and the agents that were removed from the original pointed model to obtain M.
  # The number of agents is the same for each tuple.
  # It corresponds to the minimal number of agents which need to be removed from the original model in order for
  #   the proposition to be common/general belief in that pointed model.
  
  # 1. If we're given a string, first make it a formula
  if isinstance(formula, str):
    formula = Formula(formula)

  # 2. Check if the model satisfies the requirements of KD45
  if M.is_legal_KD45()[0]:

    # 3. Check if all propositions in the formula are in the language
    for p in formula.propositions():
      if p not in M.P:
        raise PropositionError('The proposition %s is not in the language.' % p)
    
    # If this is all in order, generate (a) solution(s)
    # 4. Start by removing all non-believers; they will have to be removed anyhow
    agents_removed = M.remove_non_believers(formula)
    result = []
    
    # 5. If all agents are non-believers, there is no solution
    if len(M.agents) == 0:
      return result
      
    if belief_type == "general":
      # 6. There is always exactly 1 (or no) such solution to the general belief problem, so we can quit now
      result += [(M, agents_removed)]
      return result
    
    # 7, 10. Else: continue by removing 0 agents, then 1, then 2, etc, until we find a solution
    for i in range(len(M.agents)):
    
      # 8.
      for xs in sublists(M.agents, i):
        M2 = copy.deepcopy(M)
        
        for x in xs:
          M2.remove_agent(x)
        
        #9. Append every (model, agents) combination that constitutes a solution
        if common_belief(M2, formula):
          result.append((M2,agents_removed + xs))
      
      if result != []:
        # Return all solutions in which a minimum number of agents is removed
        return result
          
    return result
  else:
    raise ModelError(M.is_legal_KD45()[1])
```


### Truth Definition of Non-Modal Formulas

Thanks to the recursive character of the Formula class and the immediate accessibility of its main connective, a formula's truth value can be determined in a straightforward way,

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


### Belief and Common Belief

The `believes` function can be seen as a definition of the belief-operator $$B_i$$.
It is used by the Kripke class in the method `remove_non_believers`.
The `common_belief` function corresponds to the operator $$C$$.
It is used directly by the `analyse` function, and makes use of the `union` and `t_closure` helper functions.
Together, these helper functions can construct the transitive closure of the union of the accessibility relations, which is required for evaluating $$C$$.

```python
def believes(agent, formula, M):
  # Checks whether an agent believes a formula in a pointed model
  
  for [s, t] in M.R[agent]:
    if s == M.real_world:
      if not check_formula_local(formula, M, t):
          return False
          
  return True


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


def common_belief(M, formula):
  # Check whether a non-modal formula is a common belief in a pointed model
  
  for [s, t] in t_closure(M.R):
    if s == M.real_world:
      if not check_formula_local(formula, M, t):
        return False

  return True
```