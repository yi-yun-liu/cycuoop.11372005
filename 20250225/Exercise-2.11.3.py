import math  # Import the math module to access pi

# Part 1: Calculate the volume of a sphere with radius 5
radius = 5  # Radius in centimeters
volume = (4/3) * math.pi * (radius ** 3)  # Volume in cubic centimeters

# Display the result
print("The volume of the sphere with radius", radius, "cm is", volume, "cubic centimeters.")

import math  # Import the math module to access trigonometric functions

# Part 2: Compute sin^2(x) + cos^2(x) for x = 42 radians
x = 42  # Angle in radians
sin_value = math.sin(x)  # Calculate sine of x
cos_value = math.cos(x)  # Calculate cosine of x

# Sum of squared sine and cosine
result = sin_value**2 + cos_value**2

# Display the result
print("sin^2(x) + cos^2(x) for x =", x, "is approximately", result)

import math  # Import the math module to access mathematical constants and functions

# Part 3: Compute e^2 using three methods

# Method 1: Using math.e and exponentiation operator (**)
e_squared_1 = math.e ** 2

# Method 2: Using math.pow
e_squared_2 = math.pow(math.e, 2)

# Method 3: Using math.exp (computes e raised to the power of x)
e_squared_3 = math.exp(2)

# Display the results
print("Using math.e and **: e^2 =", e_squared_1)
print("Using math.pow: e^2 =", e_squared_2)
print("Using math.exp: e^2 =", e_squared_3)
