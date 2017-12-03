import time
import pandas as pd
import boto3 #AWS mturk API access

class Hit:
    def __init__(self, hitType, hitLayout):
        self.type = hitType
        self.layout = hitLayout


#--Configurations
Hit_sand = Hit(
    hitType='3GSIANI2QTZ3L86789WGQS7C6GNPDZ',
    hitLayout='3T77RDP6O26QFOF5C6FQFYMXR2OZQ0'
)
Hit_prod = Hit(
    hitType='31SXY3N7KEJ7IU43DSQI25K85QRB0F',
    hitLayout='36O2T6W7PUKYFKK4BXVRGTGJTWEDES'
)
TASK_TYPE = 0 #0:sand; 1:production
BATCH = 5 #Number assignments in a batch (HIT)
LIFE_TIME = int(2 * 60 * 60) #Life time of a HIT in sec (can be viewed on the MTurk worker board)


#--Connect to mturk server
#0:sand; 1:production
def connect(taskType):
    #Decide target server by taskType
    serverUrl = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com' if taskType == 0 else 'https://mturk-requester.us-east-1.amazonaws.com'

    #Decide HIT info to be used by taskType
    HIT = Hit_sand if taskType == 0 else Hit_prod

    #Connect
    mturk = boto3.client('mturk', endpoint_url=serverUrl)
    
    return (mturk, HIT)
mturk, HIT = connect(TASK_TYPE)


'''
------------------------------------------------------------
Create HIT
- HIT is a batch of assignments.
- An assignment is what a Turker really performs.
- Assignment >= 10 incurs additional cost.
- Only assignments exclude repeated Turkers. i.e. a Turker can take multiple HITs
------------------------------------------------------------
'''
def create(token=''):
    response = mturk.create_hit_with_hit_type(
        HITTypeId=HIT.type,
        HITLayoutId=HIT.layout,
        MaxAssignments=BATCH,
        LifetimeInSeconds=LIFE_TIME,
        UniqueRequestToken='t' + token if token != '' else str(time.time()) #For identifying request error and duplication
    )
    print(response['HIT']['HITId'])
    print(response['HIT']['CreationTime'])
    print(response['HIT']['Title'])
create()








'''
------------------------------------------------------------
Acquire HIT info
------------------------------------------------------------
'''
response = mturk.list_hits(MaxResults=100)
HITs = pd.DataFrame.from_dict(response['HITs'])
while 'NextToken' in response:
    response = mturk.list_hits(MaxResults=100, NextToken=response['NextToken'])
    HITs = pd.concat([HITs, pd.DataFrame.from_dict(response['HITs'])])

#Filter by HIT status
#Assignable | Unassignable | Reviewable | Reviewing | Disposed
HITs.query('HITStatus == "Reviewable"')









'''
------------------------------------------------------------
Acquire assignment info
------------------------------------------------------------
'''
#--Acquire assignment info
#AssignmentStatuses=['Submitted'|'Approved'|'Rejected']
response = mturk.list_assignments_for_hit(
    HITId='3QOPOPHLGN60QK5O6ZJ5NWR8WSEWBU',
    MaxResults=100,
    AssignmentStatuses=[
        'Submitted', 'Approved','Rejected',
    ]
)
response['Assignments']








'''
------------------------------------------------------------
Create new HIT by specified time gap
------------------------------------------------------------
'''
#--Configure
totalCount = 5 #Total HITs completed (for request token)
batch = 5 #Number of HITs to be automated in a batch
gap = int(2 * 60 * 60) #Gap hours between each HIT


#--Define function for recursion
count = totalCount
def callAPI():
    global count


    count += 1
    time.sleep(gap)


#--Recur the batch number of times
while count < totalCount + batch:
    callAPI()








'''
------------------------------------------------------------
Block worker
------------------------------------------------------------
'''
response = mturk.create_worker_block(
    WorkerId='A3DS068PGQ5RBN',
    Reason='As stated in the previous email.'
)
print(response)