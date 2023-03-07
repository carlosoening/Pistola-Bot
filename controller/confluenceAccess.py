from decouple import config
from atlassian import Confluence

def getConfluenceConnection():
    confluence = Confluence(
    url='https://logprosistemas.atlassian.net/',
    api_version='cloud',
    username=config('JIRA_USERNAME'),
    password=config('JIRA_ACCESS_TOKEN')
    )
    return confluence