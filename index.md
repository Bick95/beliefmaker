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

### Philosophical Background

In contemporary philosophy, „belief“ usually refers to an attitude, in which we regard a proposition as true (Schwitzgebel, 2019). In the English use of the term, a sense of uncertainty may be intended (i.e. „I believe this is the right address“ usually means „I am not completely sure, if this is the right address“), but there is no such uncertainty in the agent, when we consider belief in a philosophical sense. Here, „X believes that Y“ can be read as „X takes Y to be true“. Therefore, belief in the philosophical sense takes knowledge as its aim, and, while in logic we can formally distinguish between knowledge and belief, this distinction is usually hard to make in everyday life (Gettier, 1963). All humans constantly carry a set of beliefs, which mostly are implicit, and range in variety from mundane (e.g. the belief to possess hands), to impactful (e.g. the belief that I love my wife), to potentially dangerous (e.g. the belief in homophobic stereotypes).

### Belief and Conspiracy Theory in Reality

One type of belief that can bear great relevance or potential danger, is a *conspiracy theory*. There are many kinds of conspiracy theories: some are political and some are non-political (Räikkä, 2009), some constitute alternative explanations and others constitute a denial (Huneman & Vorms, 2018). However, recent events such the Christchurch massacre in New Zealand and the Hanau shooting in Germany show unambiguously, where the belief in conspiracy theories, at its worst, can lead to. Even more recently, conspiracy theories concerning the COVID-19 pandemic have led people to disobey social distancing guidelines or quarantine rules, thereby potentially putting the life of others at risk.

While there are many possible explanations for the viral spread of conspiracy theories concerning COVID-19 (e.g. scientific norms surrounding peer-reviews and retractions not being able to keep up with the spread of false information (O’Connor & Weatherall, 2020)), we propose that *shrinking social circles* can be another reason. By shrinking social circles, we describe a process, in which an individual who has a certain belief (i.e. in a conspiracy theory), may cut ties with contacts in their social network, who do not share their belief. By such a process, the individual’s social circle may eventually consist only of those who also believe in the theory. This could then lead that person to perceive a distorted form of reality, in which the (conspiracy) theory is *commonly believed*, meaning that there are no people within the social circle anymore who do not even hold it possible that the theory may in fact be false. We can imagine that such a situation could then further be seen as the perceived validation of the belief by each member of that group, and therefore further strengthen their commitment to the belief. Such a process could lead to those individuals living in echo chambers, where they are not confronted with opposing opinions anymore. Should such a process occur in multiple groups, it would lead to a polarization between different groups, where each group would only reinforce their own beliefs, and not take the opinion of out-group members into account. Ultimately, this could lead to a radicalization within the shrinking social group. Therefore, we argue that it is beneficial, to maintain social relationships with people who do not share one’s beliefs (or at least still hold the opposite of one’s belief to be possible), in order to prevent potentially distorted perceptions of reality.
    
### The Project

The goal of our project *beliefmaker* is to use the logic KD45 in order to show, via a visualization in Kripke models, how the removal of agents (meaning accessibility relations within the model), can lead a proposition to become *common belief*, in the logical sense. After providing some formal logical background concerning KD45 and common belief specifically, we introduce our model and online tool. Then, we will give a concrete example, related to the conspiracy theory that 5G internet towers cause coronavirus infection, in order to show how the model works in practice. Lastly, we will discuss limitations and possible philosophical implications of our model.
