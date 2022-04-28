#!/usr/bin/env python
# encoding: utf-8
from jira import JIRA
import time


def func_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print("call %s, time: %f" % (func.__name__, end - start))
        return result
    return wrapper


class TargetJira:
    instance = None

    def __init__(self, project, userEmail, apiToken):
        self.project = project
        self.userEmail = userEmail
        self.apiToken = apiToken
        TargetJira.instance = JIRA('https://company.atlassian.net/',
                                   basic_auth=(userEmail, apiToken))

    @func_time
    def get_issues(self, release):
        size = 100
        initial = 0
        all_issues = []
        fields = ['key', 'summary', 'status',
                  'components', 'issuetype', 'customfield_10630']
        while True:
            start = initial * size
            # search all issues by specified version
            issues = TargetJira.instance.search_issues(
                'project = {} AND fixVersion = "{}" ORDER BY key'.format(self.project, release), startAt=start, maxResults=size, fields=fields)
            all_issues = all_issues + issues
            if(len(issues) < size):
                break
            else:
                initial = initial+1
        return all_issues
