import time
import boto3

count = 0

def executeSomething():
    #code here
    print('you are beautiful')
    time.sleep(2)
    global count
    count += 1

while count <= 3:
    executeSomething()

# mturk = boto3.client('mturk')

# response = mturk.get_account_balance()
# print(response)