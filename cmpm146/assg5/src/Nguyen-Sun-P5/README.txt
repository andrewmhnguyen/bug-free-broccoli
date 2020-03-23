Andrew Nguyen and Yongshi Sun

Our search follows the basic A* algorithm found on both the reading from earlier
this quarter and the pseudocode in wikipedia. In addition, we also added a part 
in the if statement to make sure that we don't revisit states we have already 
previously visited. The heuristic that we implemented checks if there's already 
required equipment and returns infinity if we already have one and try to make 
another. In addition, it limits the amount of raw materials as we don't need large
amounts of it in order to craft most of the items unless the goal is large. 