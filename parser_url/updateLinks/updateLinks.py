from urllib.request import urlopen

input = open('oldLinks.txt', 'r')
f = open('newLinks.txt', 'w')
count = 0
for i in input:
    try:
        a = i.replace('\n', '')
        resp = urlopen(a)
        f.write(resp.url + '\n')
        count += 1
        print(count)
    except:
        print(count)
        continue
