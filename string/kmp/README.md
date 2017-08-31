# Overview
This is an implementation of the Knuth-Morris-Pratt algorithm to find all the occurences of a pattern in a string. This algorithm runs in O(|P|+|T|) time, where |P| and |T| are the string lengths of pattern and text respectively.

# Notes of implementation
The current implementation finds the matches by constructing the prefix function for pattern+"$"+text, where "$" must be any character that does not appear in neither pattern nor text. Therefore, such a construction may suffer from the inflexibilities where:
- The prefix function has to be constructed each time a new text is used.
- It is necessary to know which character does not appear in pattern/text beforehand.

It is possible to implement the algorithm differently by constructing the prefix function for pattern, and match the text with the string subsequently. This would also save time if the same pattern needs to be matched against different texts, since the same prefix function can be reused.
