Andrew Nguyen
Liangyu Shi

Our modifications to mcts_modified.py were mainly just changing the explore factor. 
It should try to exploit paths when we are winning by lowering the explore factor,
making it focus more on already discovered and aken paths. On the other hand, if 
the bot loses, it will increase the explore factor and try to branch out to other 
paths that could potentially return more victories. 