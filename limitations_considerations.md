---
title: Limitations & Considerations
layout: default
filename: limitations_considerations
--- 
## Limitations & Considerations

### Logical Omniscience

Naturally, since we have chosen the system $$KD45_{(m)}$$ as the basis for our logical implementation, our project runs into the same problems that this system on its own does.
A major problem with $$KD45_{(m)}$$ is that it does not seem representative of actual human logical intuition, because it assumes that all agents believe all logical truths.
This problem is more generally known as the problem of _Logical Omniscience_.
Under the assumption of Logical Omniscience, it would be assumed that humans possess belief in all valid, as well as equivalent formulas, at all times, which seems to be an unrealistic expectation.
For example, it could be the case that one formula is logically equivalent to another, but that an agent believes in one but not the other, because they are unaware of the equivalence.
Therefore, since $$KD45_{(m)}$$ suffers from the problem of Logical Omniscience, this might reduce the representative strength of our models when it comes to agents in the real world.

### Belief Change

While _beliefmaker_ is able to show how the selective removal of members from a group can lead to changes in shared belief, it is not able to show belief change regarding the proposition as such, by the individual group members.
This means that it is not possible that an agent believes in a proposition in one model, and then does not believe in the proposition anymore in in _beliefmaker_'s new restricted model, and vice versa.
For example, it would not be possible for a remaining group member to believe that 5G towers are causing Covid-19 after the removal of any number of group members, if that group member has not already believed it before the removal.
This means that our system cannot represent many interpersonal social psychological mechanisms that play a role in group polarization.
One example of such a phenomenon would be conspiracy cascades (Sunstein & Vermeule, 2009), by which group members who previously did not believe in a conspiracy theory may adopt the belief upon hearing that other group members believe in it.
This could then potentially lead a whole group to adopt said belief, without the need to exclude any members, since doubters are simply being converted by other in-group members.
While this is not possible in our system, it can certainly be argued that an intensification (albeit not a reversal) of the individual member’s belief is implicit in their gaining the awareness that a certain proposition has become commonly believed within their group, as outlined in the introduction.

### Symmetry

In our Covid-19 example, we assume that "reasonable" people are selectively excluded, due to them not sharing the prevalent beliefs of the group, therefore leading to the adoption of potentially harmful beliefs as general or common beliefs within the restricted group.
However, while in our model, we can define the real world a priori, this is not possible in reality.
Consider for example two groups: scientists and conspiracy theorists.
It is likely that these two groups maintain opposing beliefs.
However, since in reality we cannot objectively determine which world is the real world, there is a symmetry between the beliefs of these two groups.
This symmetry is due to both groups assuming different worlds to be the real world.
Therefore, the perspective on whether the exclusion of a doubter would be beneficial to the group, depends on which world is assumed to be the real world.
So, for both groups, the exclusion of doubters from their group appears to be equally reasonable.

### Two Types of Not Believing 

Based on the symmetry outlined above, we cannot objectively know whether the exclusion of someone from a group is beneficial.
However, this does not mean that excluding members who do not share the prevalent belief of the group is desirable.
This is because we have yet to distinguish between two types of not believing.
There is a potentially important difference to be made between a person _believing something not to be the case_ ($$B_i ¬ϕ$$), and a person _not believing something to be the case_ ($$¬B_i ϕ$$).
While in the former case, an agent does not hold a world in which $$ϕ$$ is true for possible, an agent in the latter case merely holds a world where $$ϕ$$ is false for possible.
For example, let ϕ be "5G causes Covid-19".
Now, a group member who maintains the belief $$B_i ¬ϕ$$ does not hold it for possible that 5G is causing Covid-19, while a group member whose belief is expressed by $$¬B_i ϕ$$ merely holds it for possible that Covid-19 is not caused by 5G.
However, the presence of either of the two agents in a group where otherwise $$ϕ$$ would be generally or commonly believed, would lead to the same result in _beliefmaker_: this agent would prevent $$ϕ$$ from being general or common belief.
This is because in both cases, the agent holds at least one world for possible in which $$¬ϕ$$ is the case.
 
### Paranoia and Naivety 

Since in reality we cannot establish with complete certainty which world is the real world, there is a symmetry between opposing beliefs, as stated above.
Therefore, both the common belief in a formula ($$F ϕ$$), as well as the common belief in the negation of that formula ($$F ¬ϕ$$) appear undesirable, since, in either case, the "correct" belief could be the excluded one.
However, we might feel somewhat uncomfortable with this conclusion.
For example, it could be argued that in the case of the 5G conspiracy theory, it would be desirable that there would indeed be a common belief, namely that the conspiracy theory is false.
Nevertheless, our caution regarding both common beliefs will become clearer once we look at another example: let $$ϕ$$ now be "The police purposefully escalates protests".
If a group would commonly believe this proposition ($$F ϕ$$), this group may be said to display paranoia, because they would not even hold it for possible that the police is not purposefully escalating protests.
A paranoid group may maintain an unrealistically antagonistic image of police forces as a whole, thereby contributing to the distrust between protesters and the police, and potentially worsen the situation.
However, if a group would commonly believe this proposition to be false, that group may be said to display naivety, since they would not even hold it for possible that the police is indeed purposefully escalating protests.
A naive group may therefore fail to detect sinister methods deployed by the police when they occur, falsely blame the protestors, and potentially excuse police brutality.
Therefore, both common beliefs can lead to a distorted perception of reality, and therefore come with a risk for the respective group.

### Final Thoughts 

In the [introduction](https://bick95.github.io/beliefmaker/index), we have stated that some of the benefits of preventing shared belief within a group are slowing down group polarization and avoiding undesirable consequences, such as the sinister attribution error or positional jockeying.
We have further shown that, since in reality we cannot know which world is the real world, there is a symmetry between opposing beliefs.
Based on our argument, it should therefore be the goal to prevent both the general/common belief in something to be the case, as well as the general/common belief in it not being the case, with respect to one's group.
A possible solution here is to always hold _multiple_ worlds for possible.
This is in line with the $$¬B_i ϕ$$ type of not believing, and it prevents both $$F ¬ϕ$$ and $$F ϕ$$.
By not believing either one or the other (in the logical sense, meaning simultaneously holding both for possible), a single group member could therefore protect their group from both the danger of paranoia and that of naivety.
This type of not believing is what we call _open-mindedness_.
Therefore, our project and its discussion can be read as the suggestion to members of social groups to remain open-minded, for the sake of their group.
However, we do not want to suggest that due to the symmetry, all opposing beliefs should receive equal credence.
For example, it does indeed not seem fair to view the belief that 5G causes Covid-19 and the belief that 5G does not cause Covid-19 as equally valid.
Therefore, the symmetry argument should not be taken to its extremes.
It is not intended as an all-encompassing equalizer to all beliefs, and in some cases (such as racism and homophobia), the $$B_i ¬ϕ$$ type of not believing may be more appropriate.
Nonetheless, we would argue that the less spectacular type of not believing, $$¬B_i ϕ$$, while it may be negatively interpreted as uncertainty, can also be positively interpreted as open-mindedness or doxastic diversity, and as such, lead to potential benefits in social groups.