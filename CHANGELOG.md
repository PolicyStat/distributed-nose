Changelog
=========

## 0.1.2

Test selection for Class-based tests no longer groups all methods from the same
class to the same test node. Hashing by module + method name will on average
give a better distribution. For (naughty) folks who tend to make a few huge
TestCase classes, this might make a fairly large difference.
