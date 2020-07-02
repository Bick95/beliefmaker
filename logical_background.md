---
title: Logical Background
layout: default
filename: logical_background
--- 
# Logical background

## Knowledge and belief
In epistemic logic, both knowledge and belief are expressed in terms of Kripke models $$M =$$ $$<$$$$S,R,v$$$$>$$, where:
* $$S$$ is a non-empty set of states;
* $$R$$ is a subset of the Cartesian product of $$S$$ $$\times$$ $$S$$;
* $$v$$: $$S→ (P → \{t,f\})$$

The main difference between knowledge and belief is that when an agent _knows_ $$p$$, then $$p$$ has to be true, but when an agent _believes_ $$p$$, then $$p$$ does not have to be true (Hintakka, 1962). This is reflected in the axioms of the system $$S5$$, representing the properties of knowledge, the third of which ($$K_i ϕ → ϕ$$) states that known facts are true (Meyer &amp; van der Hoek, 1995).

Instead of $$S5$$, the project _beliefmaker_ is making use of the system $$KD45$$, which can be seen as a doxastic (belief-oriented) counterpart to the epistemic (knowledge-oriented) $$S5$$. Since the agent believing $$p$$ does not have to mean that $$p$$ is indeed true, $$S5$$’s third axiom is changed in $$KD45$$ to simply state that a knowledge base cannot be contradictory ($$\neg B_i\bot$$). Except for the third axiom, $$KD45$$ shares its axioms with $$S5$$ (the $$K$$ in $$S5$$’s axiom is here replaced by a $$B$$, indicating belief). $$KD45$$’s axioms are listed below:
* $$A1$$: All instances of propositional tautologies
* $$A2$$: $$(B_i ϕ \wedge B_i (ϕ → ψ) → B_i ψ$$
* $$D$$: $$\neg B_i\bot$$ (a knowledge base cannot be inconsistent)
* $$A4$$: $$B_i ϕ → B_iB_i ϕ$$ (an agent believes that they believe something)
* $$A5$$: $$\neg B_i ϕ → B_i \neg B_i ϕ$$ (an agent believes that they don’t believe something)

In $$KD45$$, we say that an agent in a specific world believes a formula $$ϕ$$ if and only if that formula is true in all worlds that the agent can access from that specific world. Formally, $$(M,s) \models B_i ϕ$$ iff $$(M,t) \models ϕ$$ for all $$t$$ such that $$(s,t) \in R_i$$. In this definition, replacing $$B$$ with $$K$$ would give us the definition of the agent's knowledge of a formula instead. Thus, we can distinguish between knowledge and belief only relative to a real world, which has to be defined a priori.

When an agent can access a state $$s$$, this means that the agent holds that state for possible. For example, take two states $$s$$ and $$t$$, let an agent $$a$$ have the accessibility relation $$R_a = \{(s,t), (s,s)\}$$, and let $$p$$ hold at both $$s$$ and $$t$$. Now, from world $$s$$, agent $$a$$ can access both $$t$$ and $$s$$ itself. That means that $$p$$ holds in every world that $$a$$ holds for possible. If now one of $$s$$ or $$t$$ represents the real world, then we could say that $$a$$ _knows_ that $$p$$. However, if the real world is not accessible for $$a$$ (say the real world is some third world $$u$$), then we can only say that $$a$$ _believes_ that $$p$$. Note however that an agent in the real world (here meaning real world in the sense of a practical application, e.g. in the context of a person believing a conspiracy theory) cannot distinguish between knowledge and belief (this will be discussed further in the more philosophically oriented section). In this project, we will focus only on belief, specifically in reference to system $$KD45$$ and corresponding Kripke models.

## General belief and common belief

A sentence is generally believed in a group of agents iff every agent in that group holds the same belief (e.g. "COVID-19 is caused by 5G towers"). This can be seen as a straightforward extension of the definition of belief in one agent. Formally, let $$F ϕ$$ mean „everybody (in that group) believes ϕ“. Then, general belief is defined as:

$$F ϕ = B_1 ϕ \wedge … \wedge B_m ϕ$$ for all agents $$1, ..., m$$.

This means that every agent in the group only holds worlds for possible in which a certain formula, ϕ, holds.

Common belief is less straightforward. We define common belief by making use of Kraus and Lehmann’s (1988) adaptation of Lewis’ (2002) definition of common knowledge. According to this definition, a formula $$ϕ$$ is commonly believed among a group of people $$P$$ iff:
* Everyone in $$P$$ believes that $$ϕ$$ holds, and
* Everyone in $$P$$ believes that everyone in $$P$$ believes that $$ϕ$$ holds, and
* Everyone in $$P$$ believes that everyone in $$P$$ believes that $$P$$ believes that $$ϕ$$ holds, etc. etc. ad infinitum.

This means that everybody believes that everybody believes (and so forth) that $$ϕ$$ is true. It also means that every formula which is commonly believed is also generally believed, but not vice versa. For example, if everybody in a group believes that COVID-19 is caused by 5G internet towers, but one member of the group still holds it for possible that another member holds it for possible that it is not the case, then although the group _generally_ believes that 5G causes COVID-19, the group does not _commonly_ believe that this is the case.

Within Kripke models, a formula is common belief iff, from a specific world within the model, the formula holds true in all worlds that are accessible by any number of agents in any number of steps via accessibility relations. Formally:

$$(M, s) \models Cϕ$$  iff $$(M, t) \models ϕ$$ for all $$t$$ such that $$(s, t)$$ is in the transitive closure of the union of the accessibility relations $$R$$.

Our project _beliefmaker_ shows how, by removing agents from a Kripke model, a formula can become generally and/or commonly believed in the given model. This process is outlined using a concrete example, which describes how an initial group with different beliefs regarding COVID-19 can come, upon exclusion of members, to generally/commonly believe in a conspiracy theory.



