import time
from datetime import datetime, timedelta
import pytz
from bs4 import BeautifulSoup
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
TASK_TYPE = 1 #0:sand; 1:production
BATCH = 5 #Number assignments in a batch (HIT)
LIFE_TIME = int(3 * 60 * 60) #Life time of a HIT in sec (can be viewed on the MTurk worker board)


#--Standard response report
def report(response):
    print(response['ResponseMetadata']['HTTPHeaders']['date'])
    print(response['ResponseMetadata']['HTTPStatusCode'])


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
Create HITs every specified time gap
------------------------------------------------------------
'''
TARGET_ASSIGNMENT = 10
currentAssignment = 0

while currentAssignment < TARGET_ASSIGNMENT:
    #Create a HIT (batch)
    create()

    #Update current 
    currentAssignment += BATCH

    #Sleep between each HIT (batch) created
    time.sleep(LIFE_TIME + 60 * 30)








'''
------------------------------------------------------------
Acquire HIT info
- http://boto3.readthedocs.io/en/latest/reference/services/mturk.html#MTurk.Client.list_hits
- Max number of result=100
------------------------------------------------------------
'''
#Initial request
response = mturk.list_hits(MaxResults=100)
HITs = pd.DataFrame.from_dict(response['HITs'])

#Concat subsequent results of pagination
while 'NextToken' in response:
    response = mturk.list_hits(MaxResults=100, NextToken=response['NextToken'])
    HITs = pd.concat([HITs, pd.DataFrame.from_dict(response['HITs'])],  ignore_index=True)

#All HITs
HITs

#Filter by HIT status
#Assignable | Unassignable | Reviewable | Reviewing | Disposed
HITs_reviewable = HITs.query('HITStatus == "Reviewable"')
HITs_reviewable








'''
------------------------------------------------------------
Extend HIT lifetime
- Using past time to immediately expire the HIT
------------------------------------------------------------
'''
#Set timezone
tz = pytz.timezone('PST')

response = mturk.update_expiration_for_hit(
    HITId='301KG0KX9C74FQ1LZFYCMPOSGD52HW',
    ExpireAt=datetime.now(tz=tz) + timedelta(minutes=120)
)
report(response)








'''
------------------------------------------------------------
Delete HIT
------------------------------------------------------------
'''
response = mturk.delete_hit(
    HITId='3VMV5CHJZ81KZT0NYO0RG8JFCP8GTH'
)
report(response)








'''
------------------------------------------------------------
Acquire completed assignment info
------------------------------------------------------------
'''
#Acquire all completed assignments in the HITs
#The assignment status can be specified
def getAssignments(HITs, assignmentStatus=['Submitted', 'Approved', 'Rejected']):
    assignments = pd.DataFrame()

    #Process each HIT in the HITs
    for index, HIT in HITs.iterrows():
        response = mturk.list_assignments_for_hit(
            HITId=HIT['HITId'],
            MaxResults=100,
            AssignmentStatuses=assignmentStatus
        )

        #Make target info a df and concat
        assignments = pd.concat([assignments, pd.DataFrame.from_dict(response['Assignments'])],  ignore_index=True)

    return assignments
assignments = getAssignments(HITs)

#Some processing to get the survey code
assignments['surveyCodes'] = assignments['Answer'].apply(lambda x: BeautifulSoup(x, 'html5lib').get_text().strip('\nsurveycode'))

#Print the result
assignments








'''
------------------------------------------------------------
Review assignments
------------------------------------------------------------
'''
def review(assignmentId, verdict, feedback):
    #Decide function to use
    reviewFunction = {
        0: mturk.approve_assignment,
        1: mturk.reject_assignment
    }

    #Review
    response = reviewFunction(AssignmentId=assignmentId, RequesterFeedback=feedback, OverrideRejection=True)
    
    report(response)


#0:approve; 1:reject
review('id', 0, 'feedback')








'''
------------------------------------------------------------
Notify worker
- Send email to worker
- Can notify a batch of worker; max=100
- Only those have previously approved or rejected work
------------------------------------------------------------
'''
response = mturk.notify_workers(
    Subject='string',
    MessageText='string',
    WorkerIds=[
        'A3DS068PGQ5RBN'
    ]
)
report(response)








'''
------------------------------------------------------------
Block worker
------------------------------------------------------------
'''
response = mturk.create_worker_block(
    WorkerId='A3DS068PGQ5RBN',
    Reason='As stated in the previous email.'
)
report(response)