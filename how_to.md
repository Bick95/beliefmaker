---
title: How To - Getting started
layout: default
filename: how_to
--- 
# How to use

This is a quick introduction into the usage of our [Solver](https://bick95.pythonanywhere.com/). 

## What is it about? 

One way to establish shared belief in a group is to exclude (potential) dissidents.
The project [_beliefmaker_](https://bick95.pythonanywhere.com/) uses epistemic logic to illustrate how general or common belief in a group can change as a function of removing group members.
In particular, the question it answers is: how can we, by removing a minimal number of agents, establish a formula as general or common belief, in a given world, in a given model?

## How to use it?

The input to the system consists of three parts: a pointed Kripke model, a formula, and a requested type of belief.

### Kripke model

The input model consists of the essential parts of a pointed $$KD45_{(m)}$$ Kripke model (see the [Logical Background](https://bick95.github.io/beliefmaker/logical_background) section for more information on such models).
These are the model's point (i.e. the "real world"), the accessibility relations, and the valuation.
The agents and the propositions are deduced from these parts of the model.
There are few restrictions on the naming conventions: any string can be used as an agent's name, and any alphanumeric string can be used as a proposition.
However, states have to be integers, reflecting the convention of naming them $s_1$, $s_2$, etc.

#### Real world

The real world is the first part of the input. It can be defined as follows:

```python
'real_world': 1
```

#### Accessibility relations

Next, specify the model's accessibility relations. These are implemented as dictionaries, where the keys are the names of the agents, and the values are lists of lists of length 2.
For example, in a model with $$A = \{a,b,c\}$$ and $$S$$ = $$\{s_1,s_2,s_3\}$$, this may result in the following set of directed accessibility relations $$R$$ (depending on the constructed world model):

```python
'R': {'a': [[1, 2], [1, 3], [2, 2], [3, 3], [2, 3], [3, 2]], 
      'b': [[1, 3], [2, 3], [3, 3]], 
      'c': [[1, 1], [2, 2], [3, 3], [3, 1], [1, 3]]
      }
```

#### Valuation functions

Finally, it must be specified which formulas hold at which state. For example, let the set of propositions be $$P = \{p,q,r\}$$.
Now, if $$p$$ is true in states $$s_2$$ and $$s_3$$, but false in all other states, this can be indicated by writing `'p': [2, 3]`. The full set of such valuation functions is the specified as set $$V$$, as follows:

```python
'V': {'q': [3], 
      'p': [2, 3], 
      'r': [1, 2, 3]
      }
```

#### Putting it all together

In order to construct the Kripke model specification, assemble the real world specification, the set of accessibility realtions, and the valuation function into a datastructure following the syntax of a dictionary implemented in the Python programming language. For that, put all the different parts specified above in curly braces `{...}` and separate them by commas. Following our running example, this results in the following input:

```python
{'real_world': 1, 
 'R': {'a': [[1, 2], [1, 3], [2, 2], [3, 3], [2, 3], [3, 2]], 
       'b': [[1, 3], [2, 3], [3, 3]], 
       'c': [[1, 1], [2, 2], [3, 3], [3, 1], [1, 3]]
       }, 
 'V': {'q': [3], 
       'p': [2, 3], 
       'r': [1, 2, 3]
       }
}
```

This dictionary can then be written in the text field labeled **_Model_** on the start page of the solver. 

#### Note: Mind $$KD45_{(m)}$$ constraints

When constructing a model, please make sure it follows the constraints imposed on valid $$KD45_{(m)}$$ Kripke models, as described in the [Logical Background](https://bick95.github.io/beliefmaker/logical_background) section. Otherwise, if you click on `Solve` or `Solve & Visualize`, you will be pointed toward which constraints your model currently violates via error messages clearly indicated in red at the top of the page. 

### Query formula

The formula to be established as shared belief can be typed into the indicated textbox. Make sure that the formula's syntax is in order and that all propositions occurring in it also occur in the model. Otherwise, an error message will point you to the respective problem encountered when evaluating the formula. 
Simple and complex formulas are both accpeted, but modal operators are not. For example, $$p \rightarrow (q \wedge r)$$ is allowed, but $B_i p$ is not.

#### Connectives

The full list of connectives available to extend the complexity of the queried **_Formula to be established_** is as follows: 

* Negation: `~`; Example: `~a`
* Conjunction: `&`; Example: `a & b`
* Disjunction:  `|`; Example: `a | b` 
* Implication: `->`; Example: `a -> b`
* Bidirectional Implication: `<->`; Example: `a <-> b`

Please do not forget to write parentheses in order to disambiguate your formula.
In case the formula does end up ambiguous, the system will also print the disambiguated variant of the formula that it has evaluated as a **_Formula to be established_**". 

### Type of belief

If it is only intended to establish that everyone in the computed solution model believes that the **_Formula to be established_** holds in the real world, choose the option "General belief". If you want to ensure that this formula is commonly believed, choose the alternative option "Common belief". 

Afterwards, click on `Solve` or `Solve & Visualize`, depending on whether you only want a solution to be computed and explained or whether you wish to also obtain a visualization of the involved models.

The resulting model, as well as the agents to be removed, will then be printed on the right.