# Overview
The **suffix_array.py** module can be used to
- Build suffix array of a string using <code>SuffixArray.build()</code>
- Find occurences of patterns in string using <code>SuffixArray.match(patterns)</code>

# Note of implementation
Denote m as the pattern length and n as the string length.  

Constructing the suffix array takes
- Running time: <code>O(n log n)</code>
- Memory space: <code>O(n)</code>

Matching the pattern takes
- Running time: <code>O(m log n)</code>
- Memory space: <code>O(n)</code>
