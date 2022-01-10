print("\nQ1a\n")
# Q1a: Replicate the following functions as lambda functions


def square(n):
    return n*n


def percentage(n):
    return n/100


def multiplier(n, m):
    return n*m


def addition(a, b, c):
    return a + b + c

# A1a:

l_square = lambda n: n*n

l_percentage = lambda n: n/100

l_multiplier = lambda n, m: n*m

l_addition = lambda a, b, c: a + b + c

print("\nQ1b\n")
# Q1b: Write an explanation of how this factorial lambda function works
factorial = lambda a: a*factorial(a-1) if (a>1) else 1

# A1b:
"""
The lambda function above takes the input of any integer and then works backwards from 1.
When the value of factorial(a-1) reaches 1, it replaces the value with 1 and then uses the values
to work up towards the final answer of a * a-1 * .... * 1
"""

print("\nQ1c\n")
# Q1c: Using the Map function alongside a lambda function, take the list_of_numbers
# and generate a list of all of the numbers squared
list_of_numbers = [23, 345, 45, 76, 87, 4, 2, 0]

squares = list(map(lambda x: x*x, list_of_numbers))

# A1c:

# -------------------------------------------------------------------------------------- #
