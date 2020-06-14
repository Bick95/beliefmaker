---
title: How To - Getting started
layout: default
filename: how_to
--- 
# How To - Getting started

This is a quick introduction into the usage of our [Solver](https://bick95.pythonanywhere.com/). 

## What is it about? 

Suppose you are with friends and having a discussion. You start wondering whom you would have to exclude from your discussion round in order to be left with only like minded people. For example with those that do not share the point of view that the Corona crisis was caused by radio waves emitted by 5G antennas. 

Suppose you have kept track of the circle of discussion members you commonly engage with, including their beliefs, and wanted to feed the data into a simple tool that allows you to commpute with ease which people you have to remove from your circle of discussion members to establish common belief in your group. Or at least to have everyone believing in the same world fact. 

Sounds eactly like what you need? Here you go! This [Solver](https://bick95.pythonanywhere.com/) implements the solution to vour problem at hand. 

## How to use it?

### Implicit possible world states

First, implicitly define which worlds you want to consider in your mini-universe and label them 1 through $n$, where $n$ stards for the maximal number of possible worlds, or world states, that are allowed in youe mini universe, i.e. the model you are going to construct. 

### Real world

From the set of $n$ worlds, choose a real world. For example:

```python
'real_world': 1
```

### Accessibility relations

Next, specify which person, or agent, considers which world states possible. Indicate, for each state and each state, which other world states a person considers consistent with its beliefs valid at a given state. 
Intuition: Imagine that person, or $agent$, $a$ is considered being at world 1 and considers it possible that world 2 is also possible, since facts valid at world 2 do not contradict with the agent's beliefs at world 1. 
In this case, establish a so-called accessibility relation for agent $a$ from world 1 to 2, which is done by specifying `'a': [[1, 2],...]`, where `...` stands for possibly more accessibility relations of the form $[world_i, world_j]$ for agent $a$. Given our running example, and doing this for all agents &a&, $b$, and $c$, for the worlds 1, 2, and 3, this may result in the following set of directed accessibility relations $R$ (depending on your constructed world model):

```python
'R': {'a': [[1, 2], [1, 3], [2, 2], [3, 3], [2, 3], [3, 2]], 
      'b': [[1, 3], [2, 3], [3, 3]], 
      'c': [[1, 1], [2, 2], [3, 3], [3, 1], [1, 3]]
      }
```

### Valuation functions

Finally, it must be specified which formulas hold at which state. For example let $p$ stand for $Corona is caused by 5G$. Then, in some possible world states, $p$ may be true, while in other's it isn't. Possible world states correspond to states of the world one could imagine being true. If $p$ is true at the possible worlds 2 and 3, then indicate this by writing `'p': [2, 3]`. The full set of such evaluation functions is the specified as set $V$. $V$ may look as follows:

```python
'V': {'q': [3], 
      'p': [2, 3], 
      'r': [1, 2, 3]
      }
```

### Putting it all together

Next, the individual parts developed above have to be compiled to a whole so-called Kripke Model. 

#### Constructing the full model specification

For constructing the Kripke model specification describing your usecase, you have to assemble the real world specification $real_world$, the set of accessibility realtions $R$, and the valuation function $V$ into a datastructure following the syntax of a dictionary implemented in the Python programming language. For that, put all parts specified above in curly braces `{...}` and separate the different parts by commas. Following our running example, this results in the following:

```python
{'real_world': 1, 'R': {'a': [[1, 2], [1, 3], [2, 2], [3, 3], [2, 3], [3, 2]], 'b': [[1, 3], [2, 3], [3, 3]], 'c': [[1, 1], [2, 2], [3, 3], [3, 1], [1, 3]]}, 'V': {'q': [3], 'p': [2, 3], 'r': [1, 2, 3]}}
```

This dictionary can then be passed into the text field labeled $Model$ on the start page of the solver. 

#### Mind $KD45_m$ constraints

When constructing model, please make sure the constructed model follows the constraints imposed on valid $KD45_m$ Kripke models, as described in section [Logical Background](https://bick95.github.io/beliefmaker/logical_background). If not, you will be pointed toward which constraints your model currently violates via error messages clearly indicated in red at the top of the page, when clicking on `Solve` or `Solve & Visualize`. 

### Querying the system

Still remember the task we aimed for achieving? The intention was to find out which agent to remove from your model to make sure only people sharing your beliefs (in the real world) are left in the circle of your close friends. Suppose you want to exclude peple from your system that do not believe $p$. That is, you want to restrict your system to a configuration where everyone who is present at the real world beliefs that $p$. 
Whatever formula it is ypu want your system to be true in the real world, type it into the text box labeled $Formula to be established$. Make sure that the formula is satisfiable. Otherwise, an error message will point you to the respective problem encountered when evaluating the formula. 

If it is only intended to establish that everyone in the computed solution model believes that the $Formula to be established$ holds imn the real world, choose the option "General belief". If you want to ensure that "Everyone knows that everyone knows that everyone knows ... that $Formula to be established$", choose the alternative option "Common belief". 

Afterwards, click on `Solve` or `Solve & Visualize`, depending on whether you only want a solution to be computed and explained or whether you wish to also obtain a visualization of the involved models. 

To account for the case that ambiguous formulas are provided to the system, the system will also print the disambiguated vriant of the formula that it has evaluated as a $Formula to be established$". 

### Connectives

The list of connectives available to extend the complexity of the queried $Formula to be established$" encompasses the following elements: 

* Negation: `~`; Example: `~p`
* Conjunction: `&`; Example: `a & b`
* Disjunction:  `|`; Example: `a | b` 
* Implication: `->`; Example: `a -> b`
* Bidirectional Implication: `<->`; Example: `a <-> b`

Formulas valid in propositional logic and constructed from this set of connectives can then be queried. 
