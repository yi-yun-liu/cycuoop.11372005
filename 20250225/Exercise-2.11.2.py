17 = n  # SyntaxError: cannot assign to literal
x = 1
y = 1
x = y = 1
print(x)  # Output: 1
print(y)  # Output: 1
x = 10;  # This works just fine, but the semi-colon is ignored.
print(x)  # Output: 10
x = 10.  # SyntaxError: unexpected '.' after number
