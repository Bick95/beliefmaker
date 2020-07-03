---
title: How To - Getting started
layout: default
filename: how_to
--- 
# How to use

This is a quick introduction into the usage of our [Solver](https://bick95.pythonanywhere.com/). 

## What is it about? 

Consider a group of three people.
Two of them, Alec and Beth, believe that 5G towers cause Covid-19, while the third, Chris, disagrees.
Then, we can establish shared belief in this group by excluding Chris.
That is, one way to establish shared belief in a group is to exclude (potential) non-believers.
 
The project [_beliefmaker_](https://bick95.pythonanywhere.com/) uses epistemic logic to illustrate how shared belief in a group can change as a function of removing group members.
In particular, the question it answers is: how can we, by removing a minimal number of agents, establish a statement as general or common belief in a given world, in a given model?

## How to use it?

The input to the system consists of three parts:
* A description of the situation, in the form of a pointed Kripke model,
* A statement, in the form of a well-formed formula, and
* A requested type of belief (see the [introduction](https://bick95.github.io/beliefmaker/index) for a brief distinction between the types).

### Kripke model

The Kripke model describes the situation of interest, against the backdrop of a set of agents (here: 'Alec', 'Beth', and 'Chris') and a set of propositions (here: 'p': '5G causes Covid-19').
The actual model contains of a set of possible states - for example, one (state 1) in which 5G does not cause Covid-19, and one (state 2) in which it does.
It also contains a set of accessibility relations, one describing each agent's beliefs, and a set of valuations, describing in which states each proposition holds true.
Finally, a pointed model also specifies which state represents the real world.

All in all, the input model consists of the essential parts of a pointed $$KD45_{(m)}$$ Kripke model (see the [Logical Background](https://bick95.github.io/beliefmaker/logical_background) section for more information on such models).
These are the model's point (i.e. the "real world"), the accessibility relations, and the valuation.
There are few restrictions on the naming conventions: any string can be used as an agent's name, and any alphanumeric string can be used as a proposition.
However, states have to be integers, reflecting the convention of naming them $s_1$, $s_2$, etc.

#### Real world

The real world is the first part of the input. It can be defined as follows:

```python
'real_world': 1
```

That is, we define state 1, i.e. the state in which 5G does not cause Covid-19, as the real world.


#### Accessibility relations

Next, specify the model's accessibility relations.
In programming terms, these are implemented as dictionaries, where the keys are the names of the agents, and the values are lists of lists of length 2.
In our example, Alec and Beth believe, in state 1, that state 2 is actually the correct description of the world.
Thus, we add `[1,2]` to both their accessibility relations. This means both hold state 2 for possible from state 1.
We also add `[2,2]` to their relations, but nothing else, meaning that both _only_ hold state 2 for possible from state 1.
Further, Chris does not believe that Covid-19 is caused by 5G. One way to model this is by including all possible relations for him, meaning he always holds both states for possible.

This results in the following accessibility relations:

```python
'R': {'Alec': [[1, 2], [2, 2]], 
      'Beth': [[1, 2], [2, 2]], 
      'Chris': [[1, 1], [1,2], [2,1], [2, 2]]
      }
```

#### Valuation functions

Finally, it must be specified which formulas hold at which state. In our case, we want 'p' to hold only at state 2.
The full set of such valuation functions is then specified as follows:

```python
'V': {'p': [2]
      }
```

This set can be extended in a similar way to the set of accessibility relations.

#### Putting it all together

In order to construct the Kripke model specification, assemble the real world specification, the set of accessibility realtions, and the valuation function into a datastructure following the syntax of a dictionary implemented in the Python programming language. For that, put all the different parts specified above in curly braces `{...}` and separate them by commas. Following our running example, this results in the following input:

```python
{'real_world': 1, 
'R': {'Alec': [[1, 2], [2, 2]], 
      'Beth': [[1, 2], [2, 2]], 
      'Chris': [[1, 1], [1,2], [2,1], [2, 2]]
       }, 
'V': {'p': [2]
      }
}
```

This dictionary can then be written in the text field labeled **_Model_** on the start page of the solver.

#### Note: Mind $$KD45_{(m)}$$ constraints

When constructing a model, please make sure it follows the constraints imposed on valid $$KD45_{(m)}$$ Kripke models, as described in the [Logical Background](https://bick95.github.io/beliefmaker/logical_background) section. Otherwise, if you click on `Solve` or `Solve & Visualize`, you will be pointed toward which constraints your model currently violates via error messages clearly indicated in red at the top of the page. 

### Query formula

The formula to be established as shared belief can be typed into the indicated textbox.
In our case, we want to established 'p', so this step is rather straightforward.
In general, make sure that the formula's syntax is in order and that all propositions occurring in it also occur in the model.
Otherwise, an error message will point you to the respective problem encountered when evaluating the formula.
Simple and complex formulas are both accpeted, but modal operators are not. For example, $$p \rightarrow (q \wedge r)$$ is allowed, but $B_i p$ is not.

#### Connectives

The full list of connectives available to extend the complexity of the queried **_Formula to be established_** is as follows: 

* Negation: `~`; Example: `~p`
* Conjunction: `&`; Example: `p & q`
* Disjunction:  `|`; Example: `p | q` 
* Implication: `->`; Example: `p -> q`
* Bidirectional Implication: `<->`; Example: `p <-> q`

Please do not forget to write parentheses in order to disambiguate your formula.
In case the formula does end up ambiguous, the system will also print the disambiguated variant of the formula that it has evaluated as a **_Formula to be established_**. 

### Type of belief

If it is only intended to establish that everyone in the computed solution model believes that the **_Formula to be established_** holds in the real world, choose the option "General belief".
If you want to ensure that this formula is commonly believed, choose the alternative option "Common belief".
In our case, the choice of belief does not impact the result; in both cases, it is necessary and sufficient to remove Chris from the model. 


### Results

Afterwards, click on `Solve` or `Solve & Visualize`, depending on whether you only want a solution to be computed and explained or whether you wish to also obtain a visualization of the involved models.

The resulting model, as well as the agents to be removed, will then be printed on the right:

```python
Propositions: P = {p}
Agents:       A = {Alec, Beth}

M = <S, R, v> with:
States:       S = {1, 2}
Relations:    R_Alec = {(1, 2), (2, 2)}
              R_Beth = {(1, 2), (2, 2)}
Valuation:    v(1) = {}
              v(2) = {p}

Real world:   1
Agent(s) removed: ['Chris']
```

Thus, by removing Chris, we obtain a pointed model in which it is both generally and commonly believed that 5G causes Covid-19.

As a final note, the example in this illustration was very simple to keep it accessible for those with a limited background in logic.
The example in the dedicated [example](https://bick95.github.io/beliefmaker/example) section is more complex, and allows for a distinction between general and common belief.