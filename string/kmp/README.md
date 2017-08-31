# Overview
This is an implementation of the Knuth-Morris-Pratt algorithm to find all the occurences of a pattern in a string. This algorithm runs in O(|P|+|T|) time, where |P| and |T| are the string lengths of pattern and text respectively.

# Notes of implementation
kmp.py finds the matches by first constructing the prefix function for pattern. It then matches the text to the pattern. If the pattern has to be matched against different texts, the prefix function constructed can be reused.

kmp2.py finds the matches by constructing the prefix function for pattern+"$"+text, where "$" must be any character that does not appear in neither pattern nor text. The code is "cleaner" and possibly easier to understand than kmp.py. However, such a construction may suffer from the inflexibilities where:
- The prefix function has to be constructed each time a new text is used.
- It is necessary to know which character does not appear in pattern/text beforehand.
