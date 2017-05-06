#%%
#--Setting up
import time
import boto3 #AWS mturk API access

mturk = boto3.client('mturk')




'''
------------------------------
Block worker
------------------------------
'''
#%%
response = mturk.create_worker_block(
    WorkerId='A3DS068PGQ5RBN',
    Reason='As stated in the previous email.'
)
print(response)




'''
------------------------------
Review assignments (in progress)
------------------------------
'''
#%%
#--Acquire HIT info
#Status='Reviewable'|'Reviewing'
response = mturk.list_reviewable_hits(
    HITTypeId='3MHB1T0JXN7YQQHPEMXFW8J0CHKJS7',
    Status='Reviewable',
    MaxResults=100
)
response['HITs']


#%%
#--Acquire assignment info
#AssignmentStatuses=['Submitted'|'Approved'|'Rejected']
response = mturk.list_assignments_for_hit(
    HITId='3ICOHX7ENCB7OA23YRXN5680YJRE09',
    MaxResults=100,
    AssignmentStatuses=[
        'Submitted', 'Approved','Rejected',
    ]
)
response['Assignments']




'''
------------------------------
Create new HIT by specified time gap
------------------------------
'''
#%%
#--Configure
totalCount = 39 #Total HITs completed (for request token)
batch = 2 #Number of HITs to be automated in a batch
gap = int(3.5 * 60 * 60) #Gap hours between each HIT


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