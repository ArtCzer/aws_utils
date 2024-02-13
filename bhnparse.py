import json
import sys
import subprocess
import boto3
import time

if __name__ == "__main__":
    request_id = ""
    env = "dev"
    days = 7
    # iterate through cmd line args
    for i, arg in enumerate(sys.argv):
        if arg=="--id":
            request_id=sys.argv[i+1]
        if arg=="--env":
            env=sys.argv[i+1]
        if arg=="--days":
            days=sys.argv[i+1]
        
    if request_id=="":
        print("NAME:")
        print("  gcparser")
        print("")
        print("SYNOPSIS:")
        print("  Provides a quick way to extract data from a BHN request using a request Id")
        print("")
        print("USAGE:")
        print("Example: Find entity id in prod in the last 7 days:")
        print("  bhnparse --id <request id> --env prod --days 7")
        print("")
        print("Example: Find entity id in dev in the last 3 days:")
        print("  bhnparse --id <request id> --env dev --days 3")
        sys.exit("")

    query_string = "fields @message | filter Level != 'Warning' | filter @message like /"+ request_id + "/ | filter @message like /eGiftManagement/ | sort @timestamp desc | limit 20"
    client = boto3.client('logs')
    query_id_response = client.start_query(
    logGroupName='cards/service',
    queryString=query_string,
    startTime = int(time.time()) - int(86400*int(days)),
    endTime = int(time.time()),
    limit=20
    )

    if env == "prod":
        start_len = 73
    else:
        start_len = 87

    query_id = query_id_response["queryId"]

    query_status = "Scheduled"
    while query_status == "Scheduled" or  query_status == "Running":

      response = client.get_query_results(
      queryId=query_id
      )
      query_status = response["status"]

    responsestr = str(response)
    start = responsestr.find("entityId") + start_len
    if start < 100:
        print("Not found!")
    else:
        end = start + 26
        print(responsestr[start:end])


