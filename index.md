---
title: Welcome to beliefmaker!
layout: default
filename: index
--- 
## Welcome to beliefmaker!

### Foreword

**This is the website for the final project for the course Logical Aspects of Multi-Agent Systems (LAMAS@[UG](https://www.rug.nl/){:target="_blank"}) in 2019/2020.**

It contains the documentation accompanying the [online tool](http://bick95.pythonanywhere.com/) developed as the final project for the LAMAS course.

## Introduction 

Did you know that 5G towers are causing Covid-19?
This conspiracy theory, which might initially sound like a joke, has recently led to the incineration of several 5G internet towers in the United Kingdom (The Verge, 2020).
While we may have the initial desire to view these cases as rare instances of pathology, they rather seem to be symptoms of people’s growing affinity with a variety of (new) conspiracy theories.
Bale (2007) defines conspiracy theories as explanatory beliefs, involving multiple actors who join together in secret agreement to achieve a hidden goal, which is perceived to be unlawful or malevolent.
It was shown that people are more likely to be open to conspiracy theories when they feel anxious (Grzesiak-Feldman, 2013), powerless (van Prooijen & Acker, 2015) and uncertain (van Prooijen & Jostmann, 2013), all of which seem highly applicable in a time marked by lockdowns, social-distancing, and the spread of false information.
Even worse, the belief in conspiracy theories has been linked to increased hostility, interpersonal distrust (Abalakina-Paap et al., 1999), and withdrawal from politics (Jolley & Douglas, 2014), all of which may have detrimental consequences in a time where cooperation and rule obedience are of grave importance.
Furthermore, belief in one conspiracy theory was found to be correlated with the belief in other unrelated (and sometimes even contradictory; Wood, Douglas & Sutton, 2012) conspiracy theories (Swami et al., 2013), indicating the danger of falling down into a rabbit hole of false beliefs.
Therefore, even bizarre theories, such as the 5G tower example, warrant our attention, and understanding how such crude beliefs may spread and manifest is essential in order to prevent potentially great harm.

One way in which conspiracy theories can manifest within a group is group polarization.
Group polarization describes a social phenomenon, by which members of a deliberating group tend to end up in a more extreme position in line with the tendencies they had before deliberation (Brown, 1986).
This means that beliefs already somewhat prevalent within the group will be continually reinforced.
While there are important inter-group characteristics (e.g. stereotyping, out-group hostility), one intra-group characteristic of group polarization is the removal of doubters from the group (Sunstein & Vermeule, 2009).
In the 5G case, this could mean that a group member who does not share the belief that 5G towers cause Covid-19, might be excluded from the group.
As doubters are being removed, the situation of both the group and its remaining members may change as a consequence.
In the long run, removing members with opposing beliefs may lead the group to develop increasingly maladaptive biases, such as a sinister attribution error (Kramer, 1994), by which out-group members are suspected to be plotting against the in-group (similar to conspiracy theories).
More generally, group polarization is associated with the danger of the group socially and informally isolating itself (Sunstein & Vermeule, 2009). 

Using concepts from epistemic logic, our project _beliefmaker_ aims at providing a formal and visual representation of how within a group of agents, the selective exclusion of members can lead to shared belief.
This process is what we call a _doxastic shift_.
More specifically, using the epistemic logic $$KD45_{(m)}$$, we will show how, through the exclusion of agents, a proposition (i.e. a belief in a conspiracy theory) can attain the status of being both generally and/or commonly believed within a group.
Belief, in the epistemic logical sense, describes a situation, in which an agent does _not_ hold a world for possible in which a certain state of affairs does _not_ hold, while the assumed state of affairs may actually not hold in the real world (Hintakka, 1962).
For example, a believer of the 5G conspiracy theory would not hold it for possible that (there is a possible world in which) 5G internet towers do not cause Covid-19.
Furthermore, while _general belief_ describes a situation in which all group members share a belief, _common belief_ describes one in which everybody in the group believes that the proposition holds, and everybody believes that everybody believes that the proposition holds, and so forth, ad infinitum (Meyer & van der Hoek, 2004). 

In the context of group polarization, the doxastic shift to both general belief and common belief within a group can be expected to both accelerate the process of group polarization as such, as well as to lead to an informational and social isolation of the remaining group members over time.
Common belief is here suspected to have an even stronger impact than general belief, since the fact that not just everybody believes in the proposition, but that also everybody is aware that everybody believes in the proposition (and so forth), introduces new social reasons for the remaining group members to push the belief even further.
For example, motivations such as reputation gain within the group may lead the members to engage in positional jockeying, a competition for who has the strongest belief (Sunstein & Vermeule, 2009).
The doxastic shift towards general and common belief can therefore be expected to play an important role in the process of group polarization.

### The Project

Our online tool _beliefmaker_ requires you to first define a Kripke model, covering a set of possible worlds, accessibility relations, and valuations of propositions.
Then, you can choose a formula that you want to be either generally or commonly believed within the group.
The [program](https://bick95.pythonanywhere.com/) will then exclude zero or more of the agents from the model, in such a way that your desired proposition holds as general/common belief within the restricted new model.
Moving forward, we will first introduce the [logical background](https://bick95.github.io/beliefmaker/logical_background) of our system, after which we will give a [concrete example](https://bick95.github.io/beliefmaker/example), related to the aforementioned conspiracy theory that 5G internet towers cause Covid-19, in order to show how it works in practice.
From there, we will discuss the technical aspect of the [program](https://bick95.github.io/beliefmaker/technical_report) itself, and in particular, the [algorithm](https://bick95.github.io/beliefmaker/logic_implementation) on which _beliefmaker_ is based.
Lastly, we will discuss the [limitations and (philosophical) implications](https://bick95.github.io/beliefmaker/limitations_considerations) of our system.
By showing how a doxastic shift can be brought on by the selective exclusion of specific members from a group, we aim to show how phenomena such as group polarization may occur, and argue for the benefits of an doxastically diverse group.