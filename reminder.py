import datetime
import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr
import json
import make_day




class Database:

    dynamodb = boto3.resource('dynamodb', endpoint_url="http://192.168.137.7:8000")

    def __init__(self, table):
        self.query = Database.dynamodb.Table(table)

    def users_scan(self):
        list_users = []
        list_company = set()
        response = self.query.scan()['Items']
        for item in response:
            item['Username'] = User(item['Username'], item['company'], item['Email'])
            list_users.append(item['Username'])
            list_company.add(item['company'])
        return list_users, list_company

    def check_timesheet_templates(self, company, data):
        start_day = data - datetime.timedelta(days=30)
        response = self.query.query(
            KeyConditionExpression=Key('company').eq(company) &
            Key('date_key').between(str(start_day), str(data)),
        )
        if response['Count'] == 0:
            return 'None'

        for period in response['Items']:
            list_days = []
            for date in period['Dates']:
                date_dict = json.loads(date)
                list_days.append(datetime.datetime.strptime(date_dict["dateKey"], '%Y-%m-%d').date())
            if day in list_days:
                if day == max(list_days):
                    return 'Exists', period['date_key']
                if day in list_days:
                    return 'contains'
                return 'None'
        return 'None'

    def check_report(self, user, data):
        company_username = user.company + '#' + user.username
        resp = self.query.query(
            KeyConditionExpression=Key('company_username').eq(company_username),
            ProjectionExpression='Username, Consent, Dates',
            FilterExpression=Attr('Dates').contains(str(data))
        )['Items']

        if resp != [] and resp[0]['Consent']:
            return True
        return False


class User:

    def __init__(self, username, company, email):
        self.username = username
        self.email = email
        self.company = company
        self.table_timesheet_templates = False

    def set_timesheet_templates(self, value):
        """set timesheet templates exists"""
        self.table_timesheet_templates = value


def start_block(data):
    make_user_list = Database("Users")
    table_timesheet_templates = Database('TimesheetTemplates')

    list_users, list_company = Database.users_scan(make_user_list)
    for company in list_company:
        response = Database.check_timesheet_templates(
            table_timesheet_templates, company, day)
        for user in list_users:
            if user.company == company:
                user.set_timesheet_templates(response)
    check_table_report = Database("ReportPeriods")
    for user in list_users:
        if 'Exists' in user.table_timesheet_templates:
            if Database.check_report(check_table_report,
                                            user, user.table_timesheet_templates[1]):
                print(data, user.username, '\t', "report done")
            else:
                print(data, user.username, '\t', "SEND EMAIL")
        elif user.table_timesheet_templates == 'contains':
            print(data, user.username, '\t', "Not need report")
        elif data.weekday() == 4:
            if Database.check_report(check_table_report, user, data):
                print(data, user.username, '\t', "report done")
            else:
                print(data, user.username, '\t', "SEND EMAIL")
        else:
            print(data, user.username, '\t', "Not need report")


if __name__ == "__main__":
    # For work
    # data = datetime.date.today()
    # For test
    day = datetime.datetime.strptime('2022-03-13', '%Y-%m-%d').date()

    start_block(day)

    # for test

    for i in range(6):
        Database.list_users = []
        Database.list_company = set()
        day = make_day.back_day(day)
        start_block(day)
