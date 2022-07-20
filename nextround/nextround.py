input_str = input()
n, k = int(input_str[0]), int(input_str[2])

input_scores_str = input().split(' ')

input_scores = [int(x) for x in input_scores_str]

input_scores.sort()

cut = input_scores[k-1]

count = 0
for i in range(len(input_scores)):
    if input_scores[i] >= cut != 0:
        count += 1


print(count)






