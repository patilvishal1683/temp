import boto3
import pprint
import json
import requests
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('alarm-issue-logs.log', "a")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


OWNER = "patilvishal1683"
REPO_NAME = "temp"
issue_alarm = []


def check_issue_already_present(**kwargs) -> list:
    """
    This function is to get all the issues and create a list with the issue name and return it
    """
    try:
        payload = {
            "owner": OWNER,
            "repo": REPO_NAME
        }
        result = requests.get(url=kwargs.get('url'), headers=kwargs.get("metadata"),
                              data=json.dumps(payload))
        if result.status_code == 200:
            issues = [issue.get('title') for issue in result.json()]
            return issues
        else:
            logger.error(f"Error In Github get issue request {result.status_code}\n {result}")
            # raise Exception()
    except Exception as e:
        logging.exception("An Error Occurred in check_issue_already_present")
        pass


if __name__ == "__main__":
    """ AWS CONNECTION """
    client = boto3.client('cloudwatch')
    response = client.describe_alarms()
    """
    This endpoint is to get all issues from repo 
    """
    api_endpoint = f'https://api.github.com/repos/{OWNER}/{REPO_NAME}/issues'
    metadata = {
        "Content-Type": "application/json",
        "Authorization": "token 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"
    }
    all_issues = check_issue_already_present(metadata=metadata, url=api_endpoint)

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        if response.get('MetricAlarms'):
            for alarm in response.get('MetricAlarms'):
                pprint.pprint(alarm)
                # if alarm.get('StateValue') != "ALARM":
                #     continue
                # if alarm.get('AlarmName') in all_issues:
                #     pass
                # else:
                issue_data = {
                    'title': alarm.get('AlarmName'),
                    'body': json.dumps(alarm, default=str),
                    'labels': "alarm"
                }
                issue_alarm.append(issue_data)
        else:
            logger.debug(f"No MetricAlarms alarms present it given aw account")
    else:
        logger.debug(f"An error occurred in get alarm from aws account")
    print(json.dumps(issue_alarm))