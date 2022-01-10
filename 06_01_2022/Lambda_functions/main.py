def add(x, y):
    return x+y

addition = lambda x, y: x+y

print(addition(1, 2))

savings = [234, 450, 32, 456, 740]

bonus = list(map(lambda x: x*1.1, savings))
print(bonus)