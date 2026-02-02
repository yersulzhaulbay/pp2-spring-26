n = int(input())
db = {}
for _ in range(n):
    parts = input().split()
    if parts[0] == "set":
        db[parts[1]] = parts[2]
    else:
        key = parts[1]
        if key in db:
            print(db[key])
        else:
            print(f"KE: no key {key} found in the document")