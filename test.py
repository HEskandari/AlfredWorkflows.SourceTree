#!/usr/bin/python
from STP import SourceTree

title = "NServiceBus.Persistence.Sql"
st = SourceTree()
print("Camel Cases: ")
print(st._camel_case_split(title))


print("\nSplit:")
print(st._split_match_words(title))

