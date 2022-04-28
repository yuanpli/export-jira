#!/usr/bin/env python
# encoding: utf-8
from platform import release
from turtle import color
from company import TargetJira
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os


def main():
    if len(sys.argv) != 2:
        print('Usage: python %s <jira_release>' %
              os.path.basename(sys.argv[0]))
        exit(-1)

    release = sys.argv[1]

    project_jira = TargetJira(
        'TEST', 'test@company.com', '4CsIAArEAzrBg6AN0A1xB64A')

    jira_issues = project_jira.get_issues(release)
    issues = []
    for issue in jira_issues:
        comp = 'NaN'
        if(len(issue.fields.components) > 0):
            comp = str(issue.fields.components[0].name)

        d = {
            'Key':             issue.key,
            'Summary':         str(issue.fields.summary),
            'Component':       comp,
            'IssueType':       str(issue.fields.issuetype.name),
            'Status':          str(issue.fields.status.name),
            'Configuration':   str(issue.fields.customfield_10630)
        }
        issues.append(d)
    # JSON to pandas DataFrame
    issues_df = pd.DataFrame.from_records(issues)

    print('Total Issues: '+str(issues_df.shape[0]))
    excel_name = './project_jira_'+release+'.xlsx'

    writer = pd.ExcelWriter(excel_name)

    issues_df.to_excel(writer, sheet_name='Tickets', index=False)

    write_status_sheet(release, issues_df, writer)

    write_component_sheet(release, issues_df, writer)

    write_configuration_sheet(issues_df, writer)

    writer.save()
    print('Export to file: '+excel_name)
    plt.show()


def write_configuration_sheet(issues_df, writer):
    filtered_df = issues_df[issues_df.Configuration != 'None']
    component_agg = filtered_df.groupby(
        ['Component', 'Key']).apply(agg_configs_func).reset_index()
    component_agg.to_excel(
        writer, sheet_name='Configrations', index=False)


def write_component_sheet(release, issues_df, writer):
    component_agg = issues_df.groupby(
        'Component').apply(agg_component_func).reset_index()
    component_agg.to_excel(writer, sheet_name='Component_Agg', index=False)
    component_agg.plot.bar(x='Component', y='Count', color='green',
                           title=release+': Distribution of Component', rot=15)
    for index, data in zip(component_agg["Component"], component_agg["Count"]):
        data = round(data, 4)
        plt.text(x=component_agg['Component'].loc[lambda x: x ==
                 index].index.tolist()[0], y=data+0.1, s=f"{data}")


def write_status_sheet(release, issues_df, writer):
    status_agg = issues_df.groupby(
        'Status').apply(agg_status_func).reset_index()

    status_agg.to_excel(writer, sheet_name='Status_Agg', index=False)
    status_agg.plot.bar(x='Status', y='Count', color='orange',
                        title=release+': Distribution of Status', rot=15)
    for index, data in zip(status_agg["Status"], status_agg["Count"]):
        data = round(data, 4)
        plt.text(x=status_agg['Status'].loc[lambda x: x ==
                 index].index.tolist()[0], y=data+0.1, s=f"{data}")


def agg_status_func(x):
    return pd.Series({
        'Count': x['Key'].count(),
        'Keys': '; '.join(x['Key'].unique()),
    })


def agg_component_func(x):
    return pd.Series({
        'Count': x['Key'].count()
    })


def agg_configs_func(x):
    return pd.Series({
        'Configuration': ''.join(x['Configuration'].unique())
    })


if __name__ == '__main__':
    main()
