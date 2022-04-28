## Preparation
### Create Jira API token
Create an API token from your Atlassian account:

- Log in to https://id.atlassian.com/manage/api-tokens.
- Click Create API token.
- From the dialog that appears, enter a memorable and concise Label for your token and click Create.
- Click Copy to clipboard, then paste the token to your script, or elsewhere to save  
![](https://images.ctfassets.net/zsv3d0ugroxu/1RYvh9lqgeZjjNe5S3Hbfb/155e846a1cb38f30bf17512b6dfd2229/screenshot_NewAPIToken)

**Note:**

- For security reasons, it isn't possible to view the token after closing the creation dialog; if necessary, create a new token.
- You should store the token securely, just as for any password.

## Install Dependencies
Run with the following command line to install all required libraries. 

```pip install -r ./requirements.txt```

## Run the tool
To run the tool, execute the following command line to export the Jira tickets into excel.

```python main.py <jira_release>```

Example:
```
(base) ➜ python main.py 2.18
call search_issues_with_release, time: 3.195686
Total Issues: 112
Export to file: ./jira_2.18.xlsx
```