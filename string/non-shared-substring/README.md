# Overview
Given two input strings s1 and s2, this code finds the shortest substring of s1 which does not appear in s2.
There is an alternative implementation that constructs a suffix tree from s1+"#"+s2+"$", but the current approach first constructs the suffix tree based on only s1, and use s2 to further "process" the resulting suffix tree.

# Note of usage
- There is no need to append any special characters (such as "#" or "$") to the end of the two input strings.
- The input strings can be of different lengths.
- The input strings cannot contain "#" or "$" - these are reserved by the program to mark ends of strings.
