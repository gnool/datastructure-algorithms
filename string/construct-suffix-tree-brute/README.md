# Overview
This code constructs the suffix tree of a given input string with running time of O(|string|^2) and memory consumption of O(|string|).
For faster construction one can use Ukkonen's algorithm which runs in O(|string|).

# Note of usage
Please append a character (one which does not already appear in your input string) to your input string to mark the end of the string.
Otherwise the algorithm would not work correctly in listing out all the edges.
If your input string is "banana", one example would be changing it to "banana#".
