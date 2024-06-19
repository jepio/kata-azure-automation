import azure.functions as func
from datetime import datetime,timezone,timedelta
import json
import logging
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient

app = func.FunctionApp()

credential = DefaultAzureCredential()
sub = "2efae366-54ff-4d92-b51e-7454e50408e3"

@app.timer_trigger(schedule="*/15 * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def TimerExample(myTimer: func.TimerRequest) -> None:
    
    if myTimer.past_due:
        logging.info('The timer is past due!')

    client = ResourceManagementClient(credential, sub)
    resources = client.resources.list(filter="tagName eq 'CreatedUTC'") 
    utcnow = datetime.now(tz=timezone.utc)
    rgs_to_delete = set()
    for res in resources:
        if 'Microsoft.ContainerService/managedClusters' not in res.id:
            continue
        #logging.info(f'Found resource {res.id}')
        try:
            createdutc = datetime.fromisoformat(res.tags['CreatedUTC'].split('.')[0])
        except ValueError:
            continue
        createdutc = createdutc.astimezone(tz=timezone.utc)
        #logging.info(f'Created at {createdutc}, now {utcnow}')
        diff = utcnow - createdutc
        logging.info(f'Created {res.id} created {diff} ago')
        if diff > timedelta(hours=2):
            rg = res.id.partition('/providers')[0]
            rgs_to_delete.add(rg)
    for rg in rgs_to_delete:
        logging.info(f'Deleting {rg}')
        groupname = rg.partition('/resourceGroups')[2]
        client.resource_groups.begin_delete(groupname)
    logging.info('Python timer trigger function executed.')
