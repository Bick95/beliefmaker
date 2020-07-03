---
title: Technical Report
layout: default
filename: technical_report
--- 
# Technical Report

## Overview

As described in the [introduction](https://bick95.github.io/beliefmaker/), an [online tool](http://bick95.pythonanywhere.com/) has been developed which checks how general or common belief of a queried formula in a given KD45 Kripke model can be established by removing the least number of agents from the model.
Implementation-wise, this project consists of a composition of multiple integrated parts. These are presented in the following subsections. 
All code has been developed using Python 3.5.

## Kripke Model & Logic Engine

First, a class for representing Kripke models has been created. Also a class for representing queried formulas has been developed. Also, an algorithm has been designed which determines how to establish general or common belief of a certain fact, as queried by the user, in the real world by removing the least number of agents from the provided model. For inference to be possible, both the provided model and a queried formula, consisting of a single atomic proposition or a more complex formula alternatively, must be valid. To ensure this, a mechanism has been implemented that checks the validity of a model and a queried formula before starting the inference. The implementation is described in more detail on a [separate page](https://bick95.github.io/beliefmaker/logic_implementation).

## Project Website - Solver

The project website has been created using the web framework [django](https://www.djangoproject.com/) (version 2.2.12). It is hosted on [pythonanywhere](https://www.pythonanywhere.com). 
On the front-end side, the website is characterized by a clear view on all the elements and functionality available to the user. Also, it is responsive and suitable for the use on mobile devices. 
The functionality of the website encompasses both a solver to the aforementioned problem at hand and a custom-made visualization software developed for showing medium-sized network structures (as explained in a separate section below), as which the Kripke models worked upon can be represented. On the back-end side, the website implements the [Kripke model and Logic engine](https://bick95.github.io/beliefmaker/logic_implementation) as presented above. 

In terms of input and output behavior, the solver can be described as follows. 
The user has to provide a Kripke model specification for a model he wishes to obtain a solution for. This structure must be provided in the format of a Python dictionary. An example of such a structural representation of a Kripke model looks as follows.

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

For more details on that, check out the [How To](https://bick95.github.io/beliefmaker/how_to) or the [Example](https://bick95.github.io/beliefmaker/example).

ince the above representation is not easy to read in the first place, a more intuitive explanation of the model can be obtained by clicking on the website's `Solve` button. When clicking on `Solve & Visualize`, a provided model can even be visualized by the aforementioned plotting software. States in the Kripke model are shown as light-blue dots, i.e. nodes of a graph, on top of which the respective state's id, commonly being an integer, and all propositions and formulas that hold at that state, are printed. Agents' accessibility relations between states are indicated as directed edges between the nodes. A label in the middle of an edge indicates which agent possesses a respective accessibility relation.

If the user does not only provide a model, but also a proposition or formula to be established as general or common belief in the real world, also a solution to the aforementioned problem is computed by the inference engine presented in the previous subsection. The solution is then shown right next to the provided input model. Also, by providing a proposition or formula and then clicking on `Solve & Visualize`, a graph of the Kripke model constituting the solution to the queried problem is shown in a position below the solution specification. 

To give a user of the online tool an intuitive understanding of what the input and output to the tool may look like, on startup of the [website](http://bick95.pythonanywhere.com/) an example model is inserted into the model input field and its explanation is shown already. 

Also, useful and suggestive error messages are shown when the user enters invalid or incomplete inputs. 

The source code to the repository containing the website is available on request. 

## Project Website - Documentation

The part of the website called _Documentation_ refers to the part of the website you are currently exploring. The documentation is deployed on [GitHub Pages](https://pages.github.com/) and uses an adapted version of the [Leap Day](https://github.com/pages-themes/leap-day) style template. The adaptions encompass the integration of the global navigation bar at the top of the page allowing for simple navigation and a more uniform look of all parts of the overall website encompassing both the solver and the documentation. 

## Plotting Software

For visualizing Kripke models, a custom plotting software has been developed.
Its working is as follows. First, the possible states of the Kripke model are placed equidistantly along an outer circle of dynamically adjusted size to maintain a comfortable distance between all visualized states. Then, text is placed on the node positions, where each node represents one possible state from the Kripke model. 
Afterwards, edges in between different nodes are drawn. A self-developed mathematical formalism ensures that edges, and their labels, going in opposite directions between the same nodes are not overlapping. 
Finally, reflexive connections are drawn for all states where applicable. For that, according to some mathematical formalism, a position near a respective state is determined, where a a label of a reflexive connection can safely be visualized without intersecting the corresponding state. Then, this point is connected to the state by a reflexive, directed edge. To make the software generally applicable to graph visualization problems, it has been implemented in a separate Graph class (using Python 3.5). The code can be found as a stand-alone implementation in the following [repository](https://github.com/Bick95/Small-Scale-Graph-Visualization/). 
