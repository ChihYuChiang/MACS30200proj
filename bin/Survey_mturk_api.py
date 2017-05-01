#--Setting up
import time
import boto3 #AWS mturk API access

mturk = boto3.client('mturk')


#--Configure
totalCount = 16 #Total HITs completed (for request token)
batch = 3 #Number of HITs to be automated in a batch
gap = 3 * 60 * 60 #Gap hours between each HIT


#--Define function for recursion
count = totalCount
def callAPI():
    global count

    response = mturk.create_hit_with_hit_type(
        HITTypeId='3MHB1T0JXN7YQQHPEMXFW8J0CHKJS7',
        MaxAssignments=5,
        LifetimeInSeconds=gap,
        UniqueRequestToken='t' + str(count), #For identifying request error and duplication
        HITLayoutId='3QB0JFJO76IFNHYHGO9RY6P9J9DWAR'
    )
    print(response)

    count += 1
    time.sleep(gap)


#--Recur the batch number of times
while count < totalCount + batch:
    callAPI()