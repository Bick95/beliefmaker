---
title: Example
layout: default
filename: example
--- 
# Example

Consider four people: Anna, Ben, Clara, and David. Suppose that all four believe that the COVID-19 virus does exist. Ben and David also believe that it is being used by the government in order to make people sick, and that it is being caused by 5G towers. Clara holds it for possible that the government uses COVID-19 to make people sick, but not that 5G towers are causing it. Anna, on the other hand, believes that the government is using the COVID-19 to make people sick, and holds it for possible, that it might be caused by 5G towers. 

### First model

The situation can be represented by the following Kripke model:

Propositions: P =  {p, q, r} with:
* p: the government is using COVID-19 to make people sick
* q: COVID-19 is being caused by 5G towers
* r: COVID-19 exists 

Agents:    A = {a, b, c, d} with:
* a = Anna
* b = Ben
* c = Clara
* d = David

M = <S, R, v> with:

* States: S = {1, 2, 3}
* Relations:
R_a = {(1, 2), (1, 3), (2, 2), (3, 3), (2, 3), (3, 2)}
R_b = {(1, 3), (2, 3), (3, 3)}
R_c = {(1, 1), (2, 2), (3, 3), (1, 2), (2, 1)}
R_d = {(1, 3), (2, 2), (3, 3), (2, 3)}
* Valuation:
v(1) = {r}
v(2) = {p, r}
v(3) = {p, q, r}

Real world: 1

We can see that in the real world, it is common belief that COVID-19 exists, but it is neither common belief that the government uses COVID-19 to make people sick, nor that 5G towers cause COVID-19. 
We can see that it is not common belief that COVID-19 is being used by the government to make people sick, because Clara holds it for possible that this is not the case. Formally, agent c can access world 1 (the real world), where v(1)(p) = f. Since in world 1, also q does not hold, it is also not common belief that COVID-19 is caused by 5G.

### Second model

Now, imagine that Clara is being cut out of the group, possibly due to her not believing (although certainly holding for possible) that the government is behind the virus. This would result in a new Kripke model:

M = <S, R, v> with:
* States: S = {1, 2, 3}
* Relations:
R_a = {(1, 2), (1, 3), (2, 2), (3, 3), (2, 3), (3, 2)}
R_b = {(1, 3), (2, 3), (3, 3)}
R_d = {(1, 3), (2, 2), (3, 3), (2, 3)}
* Valuation:
v(1) = {r}
v(2) = {p, r}
v(3) = {p, q, r}

Real world: 1

Now, in this smaller social circle, not considering Clara’s perspective, it is common belief that the government is using COVID-19, because there is no one, who does holds the opposite for possible. Formally, none of the agents can access a world, in which p does not hold. However, it is still not common belief that 5G causes COVID-19, because Anna still holds it for possible that it does not. Formally, from world 1, agent a can access world 2, where v(2)(q) = f. 

### Third model

Imagine now, that Ben and David clash with Anna, and that they are excluding her (or at least her opinions) from their group. Now, only Ben and David remain, which leads us to yet another (smaller) Kripke model:

M = <S, R, v> with:
* States: S = {1, 2, 3}
* Relations:
R_b = {(1, 3), (2, 3), (3, 3)}
R_d = {(1, 3), (2, 2), (3, 3), (2, 3)}
* Valuation:
v(1) = {r}
v(2) = {p, r}
v(3) = {p, q, r}

Real world: 1

In this new, reduced model, we can see that neither of the two agents can access any world, in which q does not hold. This means that by now, in this even tighter social circle, it has become common belief that not only the government uses COVID-19 to make people sick, but also that 5G towers are causing COVID-19.