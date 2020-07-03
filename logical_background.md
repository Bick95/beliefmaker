---
title: Logical Background
layout: default
filename: logical_background
--- 
# Logical Background

## Knowledge and Belief
Like knowledge, belief can be modelled using epistemic logic, which can then be called doxastic ("belief-related") logic. In particular, we can represent real-life situations using Kripke models $$M =$$ $$<$$$$S,R_1, ..., R_m,v$$$$>$$, where:
* $$S$$ is a non-empty set of states;
* $$R_i$$ is the accessibility relation of agent $$i \in A$$, a subset of the Cartesian product $$S$$ $$\times$$ $$S$$;
* $$v$$: $$S→ \mathcal{P}(P)$$

Here, $$A$$ is the set of agents, and $$P$$ is the set of propositions in the language.
Finally, a pointed Kripke model is a pair $$(M, s)$$ in which a "real world" (state $$s$$) is specified. This state is called the _point_.

The interpretation of the accessibility relations is as follows: when an agent can access a state $$t$$ from a state $$s$$ (i.e. $$(s,t)\in R$$), this means that the agent holds that state for possible. Belief is then defined as follows: in a given state, an agent _believes_ in a formula iff that formula is true in all states that the agent holds for possible. Formally, $$(M,s) \models B_i ϕ$$ iff $$(M,t) \models ϕ$$ for all $$t$$ such that $$(s,t) \in R_i$$.

The project _beliefmaker_ is based on the system $$KD45_{(m)}$$ (where $$m$$ is the size of $$A$$), a variant of epistemic logic which is particularly well-suited to model belief. This system is based on the following axioms (see e.g. Meyer &amp; van der Hoek, 1995):
* $$A1$$: All (instances of) propositional tautologies
* $$A2$$: $$(B_i ϕ \wedge B_i (ϕ → ψ) → B_i ψ$$
* $$A4$$: $$B_i ϕ → B_iB_i ϕ$$
* $$A5$$: $$\neg B_i ϕ → B_i \neg B_i ϕ$$
* $$D$$: $$\neg B_i\bot$$

Axioms $$A3$$, $$A4$$, and $$D$$ have reasonably intuitive interpretations. First, $$A4$$ implies that if an agent believes something, they must believe that they believe it. $$A5$$ implies that if an agent does not believe something, they must believe that they don't believe it. And finally, axiom $$D$$ implies that for every agent, there will always be a world that is in line with their beliefs (and by definition, in that world, $$\bot$$ does not hold). Each of these three axioms also restrict the class of legal $$S5$$-models by posing requirements on the accessibility relations. These requirements are as follows, for each relation $$R$$:
* $$R$$ must be transitive (due to axiom $$A4$$), meaning that for all states $$s$$, $$t$$, $$u$$: if $$(s,t) \in R$$ and $$(t,u) \in R$$, then $$(s,u) \in R$$;
* $$R$$ must be euclidean (due to axiom $$A5$$), meaning that for all states $$s$$, $$t$$, $$u$$: if $$(s,t) \in R$$ and $$(s,u) \in R$$, then $$(t,u) \in R$$ (and $$(u,t) \in R$$);
* $$R$$ must be serial (due to axiom $$D$$), meaning that for all states $$s$$, there is at least one state $$t$$ such that $$(s,t) \in R$$.

The system $$KD45_{(m)}$$ is very similar to the system $$S5_{(m)}$$, which is often used to model knowledge. However, there is one crucial difference, reflecting the intuitive difference between knowledge and belief: when an agent _knows_ that a formula $$\phi$$ is true, then $$\phi$$ has to be true; but when an agent merely _believes_ $$\phi$$, then $$\phi$$ does not have to be true (Hintakka, 1962). This means the requirements of belief are less strong than those of knowledge. This is reflected in axiom $$D$$ replacing $$S5$$'s axiom $$A3$$ ($$K_i ϕ → ϕ$$), which requires known facts to be true and hence requires $$R$$ to be not just serial, but reflexive (Meyer &amp; van der Hoek, 1995).


## General and Common Belief

There are two major notions of shared belief in a group, both of which are formalized by Kraus and Lehmann (1988), who adapt Lewis’ (2002) analysis in a doxastic context. First, a formula is _generally_ believed in a group of agents iff it is believed by every agent in that group. This can be seen as a straightforward extension of the definition of belief in one agent. Formally:

$$F ϕ = B_1 ϕ \wedge … \wedge B_m ϕ$$ for all agents $$1, ..., m$$.

Here, $$F ϕ$$ can be read as "everyone believes $$ϕ$$".

Second, a formula $$ϕ$$ is commonly believed in a group iff:
* Everyone (in that group) believes that $$ϕ$$ holds, and
* Everyone believes that everyone believes that $$ϕ$$ holds, and
* Everyone believes that everyone believes that everyone believes that $$ϕ$$ holds, etc., ad infinitum.

Thus, every formula which is commonly believed is also generally believed, but not vice versa. For example, suppose every member of a group believes that Covid-19 is caused by 5G internet towers, but one member still holds it for possible that another member holds it for possible that this is not the case. Then although the group generally believes that 5G causes Covid-19, the group does not commonly believe that this is the case.

In Kripke semantics, a formula is _commonly_ believed in a specific state $$s$$ iff that formula holds true in all states that are accessible from $$s$$, by any number of agents, in any positive number of steps. Formally:

$$(M, s) \models Cϕ$$  iff $$(M, t) \models ϕ$$ for all $$t$$ such that $$(s, t)$$ is in the transitive closure of the union of the accessibility relations $$R$$.

Our project _beliefmaker_ shows how, by removing agents from a pointed Kripke model, a formula can become generally and/or commonly believed in that model. This process is outlined using a concrete example, which describes how an initial group whose members have diverse beliefs regarding Covid-19 can come, upon exclusion of members, to generally/commonly believe in a conspiracy theory.