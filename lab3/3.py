words = {
"ZERO":"0","ONE":"1","TWO":"2","THREE":"3","FOUR":"4",
"FIVE":"5","SIX":"6","SEVEN":"7","EIGHT":"8","NINE":"9"
}
n = input()
for x in words:
    n = n.replace(x, words[x])
result = str(eval(n))
rev = {val:key for key,val in words.items()}
answer = ""
for digit in result:
    answer += rev[digit]
print(answer)