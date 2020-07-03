---
title: Example
layout: default
filename: example
--- 
## Example

### From Situation to Input Model

Suppose that the beliefs of a group of four friends, Anna, Ben, Clara and David, can be summarized as follows:

* __Anna__ believes that Covid-19 exists, that 5G causes Covid-19, and that Bill Gates uses Covid-19 to reduce the world population. Furthermore, Anna believes that her beliefs are shared by all other group members.
* __Ben__ believes that Covid-19 exists and that it is caused by 5G. However, Ben believes that Bill Gates does not use Covid-19 to reduce the world population. Furthermore, Ben believes that Anna and David hold it for possible that Bill Gates uses Covid-19 to reduce the world population.
* __Clara__ believes that Covid-19 exists, that 5G causes Covid-19, and that Bill Gates uses Covid-19 to reduce the world population. However, she believes that Ben and David hold it for possible that 5G does not cause Covid-19, and that Bill Gates does not use Covid-19 to reduce the world population. 
* Lastly, __David__ believes that Covid-19 exists, but he believes that 5G does not cause Covid-19, and that Bill Gates does not use Covid-19 to reduce the world population.  

The statements that the friends do (not) believe in can be represented by the following propositions:

* $$p$$: Covid-19 exists
* $$q$$: 5G causes Covid-19
* $$r$$: Bill Gates uses Covid-19 to reduce the world population

Let us assume that in the real world, Covid-19 exists, but it is not caused by 5G, and Bill Gates is not using it to reduce the world population.
Then, the situation may be captured in a pointed Kripke model $$(M, s_1)$$, where $$A =\{a,b,c,d\}$$, and $$M =$$ $$<$$$$S,R,v$$$$>$$ with:
* $$S=\{s_1,s_2,s_3,s_4,s_5,s_6\}\notag$$
* $$R_{a}=\{(s_1,s_2),(s_2,s_2),(s_3,s_3),(s_4,s_5),(s_5,s_5),(s_6,s_6)\}\notag$$
* $$R_{b}=\{(s_1,s_4),(s_2,s_2),(s_3,s_3),(s_3,s_6),(s_4,s_4),(s_5,s_5),\\  (s_6,s_3),(s_6,s_6)\}\notag$$
* $$R_{c}=\{(s_1,s_3),(s_2,s_2),(s_3,s_3),(s_4,s_4),(s_5,s_5),(s_6,s_6)\}\notag$$
* $$R_{d}=\{(s_1,s_1),(s_2,s_2),(s_3,s_3),(s_3,s_6),(s_4,s_4),(s_4,s_5),\\  (s_5,s_4),(s_5,s_5),(s_6,s_3),(s_6,s_6)\}\notag$$
* $$v(p)=\{s_1,s_2,s_3,s_4,s_5,s_6\}\notag$$
* $$v(q)=\{s_2,s_3,s_4,s_5\}\notag$$
* $$v(r)=\{s_2,s_3,s_5\}\notag$$

As input to _beliefmaker_, we only need to provide the model's point, its accessibility relations and its valuation. This looks as follows:

```
{'real_world': 1,
'R': {'a': [[1,2],[2,2],[3,3],[4,5],[5,5],[6,6]],
'b':[[1,4],[2,2],[3,3],[3,6],[4,4],[5,5],[6,3],[6,6]],
'c':[[1,3],[2,2],[3,3],[4,4],[5,5],[6,6]],
'd':[[1,1],[2,2],[3,3],[3,6],[4,4],[4,5],[5,4],[5,5],[6,3],[6,6]]},
'V': {'p': [1,2,3,4,5,6], 'q': [2,3,4,5], 'r': [2,3,5]}}
```

The visualization of the aforementioned model looks as follows:

![img_model_1][model_1]

### Establishing Shared Belief

In the above model, it is already generally and commonly believed that Covid-19 exists, since all group members believe that Covid-19 exists, and all members do not hold it for possible that any member holds it for possible that Covid-19 does not exist. However, we can see that in the group at this point, there is no general or common belief that 5G causes Covid-19, because David believes that it is not. Now, suppose that David is being excluded from the group (possibly due to his position as a doubter). This will lead us to a new, restricted model: 

```
{'real_world': 1,
'R': {'a': [[1, 2], [2, 2], [3, 3], [4, 5], [5, 5], [6, 6]], 
'b': [[1, 4], [2, 2], [3, 3], [3, 6], [4, 4], [5, 5], [6, 3], [6, 6]], 
'c': [[1, 3], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6]]},
'V': {'p': [1, 2, 3, 4, 5, 6], 'q': [2, 3, 4, 5], 'r': [2, 3, 5]}} 
```

In this new restricted group, consisting only of Anna, Ben, and Clara, it is now _general_ belief that 5G causes Covid-19. This is because none of the remaining members holds it for possible that it is otherwise. However, there is still no _common_ belief that 5G causes Covid-19. This is the case, because Ben believes that Clara holds it for possible that 5G does not cause Covid-19. Therefore, there are now two ways to achieve the common belief that 5G causes Covid-19. Firstly, Ben could also be excluded from the group, leading all remaining group members (Anna and Clara) to believe that 5G causes Covid-19, and to believe that everyone (in the group) believes that 5G causes Covid-19, and so forth, ad infinitum. The corresponding input model is displayed below:

```
{'real_world': 1,
'R': {'a': [[1, 2], [2, 2], [3, 3], [4, 5], [5, 5], [6, 6]], 
'c': [[1, 3], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6]]},
'V': {'p': [1, 2, 3, 4, 5, 6], 'q': [2, 3, 4, 5], 'r': [2, 3, 5]}}
```

Alternatively, it would also suffice to remove Clara from the second model (where David was already excluded). Then, since Clara is no longer part of the group anymore, Ben’s belief that Clara holds it for possible that 5G does not cause Covid-19, does not interfere with the proposition to be commonly believed anymore. The respective model is displayed below:  

```
{'real_world': 1,
'R': {'a': [[1, 2], [2, 2], [3, 3], [4, 5], [5, 5], [6, 6]], 
'b': [[1, 4], [2, 2], [3, 3], [3, 6], [4, 4], [5, 5], [6, 3], [6, 6]]}, 
'V': {'p': [1, 2, 3, 4, 5, 6], 'q': [2, 3, 4, 5], 'r': [2, 3, 5]}}
```

If we would instead desire for the group to maintain the general or common belief that Bill Gates uses Covid-19 to reduce the world population, this would also require the removal of both Clara and David. Here, there is no difference between who has to be removed to acquire general or common belief. In both cases, the corresponding Kripke model is the same as the Kripke model corresponding to the first possible way of introducing the common belief that 5G causes Covid-19, as displayed above.

[model_1]: https://github.com/Bick95/beliefmaker/blob/gh-pages/images/example_model_1.png "Visualization of model"
