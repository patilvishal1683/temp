import boto3
import pprint
import json

OWNER = "patilvishal1683"
REPO_NAME = "temp"
issue_alarm = []

# def create_issue(**kwargs) -> bool:
#     print(kwargs.get('url'))
#     print(kwargs.get("metadata"))
#     print(json.dumps(kwargs.get('issue_metadata')))
#     try:
#         result = requests.post(url=kwargs.get('url'), headers=kwargs.get("metadata"),
#                                data=json.dumps(kwargs.get('issue_metadata')))
#         if result.status_code == 201:
#             print("Created")
#         else:
#             print(result)
#     except Exception as e:
#         print(e)


if __name__ == "__main__":
    """ AWS CONNECTION """
    client = boto3.client('cloudwatch')
    response = client.describe_alarms()

    # api_endpoint = f'https://api.github.com/repos/{OWNER}/{REPO_NAME}/issues'
    #
    # metadata = {
    #     "Content-Type": "application/json",
    #     "Authorization": "token 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"
    # }

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        if response.get('MetricAlarms'):
            for alarm in response.get('MetricAlarms'):
                issue_data = {
                    'title': alarm.get('AlarmName'),
                    "body": 'This is a test issue created using the GitHub API and Python requests library.',
                    'labels': ['bug']
                }
                issue_alarm.append(issue_data)
        else:
            print("No MetricAlarms alarms found")

    print(json.dumps(issue_alarm))