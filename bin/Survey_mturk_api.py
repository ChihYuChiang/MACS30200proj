import time
import boto3 #AWS mturk API access

mturk = boto3.client('mturk')


#--Configure
totalCount = 9 #45, +2
batch = 2
gap = 3 * 60 * 60 #hours


#--Define function for recursion
count = totalCount
def callAPI():
    global count

    response = mturk.create_hit_with_hit_type(
        HITTypeId='3MHB1T0JXN7YQQHPEMXFW8J0CHKJS7',
        MaxAssignments=5,
        LifetimeInSeconds=gap,
        UniqueRequestToken='t' + str(count),
        HITLayoutId='3QB0JFJO76IFNHYHGO9RY6P9J9DWAR'
    )
    print(response)

    count += 1
    time.sleep(gap)

while count < totalCount + batch:
    callAPI()