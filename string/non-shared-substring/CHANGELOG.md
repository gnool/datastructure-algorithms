# Changelog
## 1.1 (2017-08-28)
- Added a new attribute **total_length** to Node class. This stores the total substring length traced up to root. Root has total_length equals zero. This new attribute is used to speed up self.shortest().
- In self.shortest(), after processing both input strings in the suffix tree, the algorithm does not trace *all* the "marked" nodes to root to compare which gives the shortest non-shared substring. Instead, it first finds which node's parent has the lowest total_length. Only then it traces from this node back to root to construct the required substring.
