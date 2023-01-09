Reinforcement Learning vs. Controls

Both Controls and RL can sometimes be useful in similar situations to try to achieve the same results. They
both need observations from the environment and then adjust their future actions based on the observations. 
However, they have many differences in how they actually work. Controls need to know the internal mechanisms 
of the system and how they work, while RL does not. Controls will have a set of rules to follow depending on 
the feedback it receives. It will react with a control for each scenario that it comes across. RL on the other
hand doesn't need to understand how the system works and can treat it as a black box. In this sense, it can 
work in some scenarios where controls might not be able to. RL will reward correct tendencies based on the 
results of previous actions performed and gradually improve. It will often require many more resources and 
work to compute than a Controls model would need.
