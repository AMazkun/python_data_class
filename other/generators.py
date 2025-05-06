
l = [x for x in range(10)]
s = (x for x in range(10))
d = { x : x * 2  for x in range(10)}

print(l)

print(s)
for i in s:
    print(i, end=" ")
print()

print(d)