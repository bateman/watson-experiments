import json
import logging
import sys

import requests

from utils import file_utils

logging.basicConfig()
log = logging.getLogger('GET-CORE')
log.setLevel(logging.INFO)

# check api limit
# curl -i 'https://api.github.com/users/bateman?client_id=7883480a7ca5510ee780&client_secret=ff3b25fc79f01dc9750b875268ee78d1cc01e32b'


user = 'apache'
repo = 'drill'

url = 'https://api.github.com/repos/{0}/{1}/contributors?client_id=7883480a7ca5510ee780&client_secret=ff3b25fc79f01dc9750b875268ee78d1cc01e32b'.format(
    user, repo)

response = requests.get(url, params={'auth-token': '2f4f0e4d7ced015a65fce4464e90ee0d5a5e6ded'}, verify=True)
# For successful API call, response code will be 200 (OK)
log.debug('HTTP request returned response code %s' % response.status_code)
core_team = list()
core_team.append(('nickname', 'name', 'email', 'github id'))

if response.ok:
    data = json.loads(response.content)

    for c in data:
        log.info('Analyzing user %s' % c['login'])
        url = 'https://api.github.com/users/{0}?client_id=7883480a7ca5510ee780&' \
              'client_secret=ff3b25fc79f01dc9750b875268ee78d1cc01e32b'.format(c['login'])

        response = requests.get(url, params={'auth-token': '2f4f0e4d7ced015a65fce4464e90ee0d5a5e6ded'}, verify=True)
        # For successful API call, response code will be 200 (OK)
        log.debug('HTTP request returned response code %s' % response.status_code)

        if response.ok:
            data = json.loads(response.content)
            core_team.append((c['login'], data['name'], data['email'], c['id']))
        else:
            # If response code is not ok (200), print the resulting http error code with description
            response.raise_for_status()
            log.error('HTTP request failed')
            sys.exit(-1)

    senders = dict()
    reader, _file = file_utils.load_corpus(filename=repo + '-senders.csv', type='csv', delim=';')
    row_num = 0  # skip header
    for row in reader:
        if row_num != 0:
            name, email = row
            senders[email] = name
        row_num += 1

    row_num = 0
    new_emails = dict()
    for c in core_team:
        if row_num != 0:
            nickname, name, email, github_id = c
            for email_k, name_v in senders.iteritems():
                if name_v in (nickname, name):
                    if email_k != email:
                        log.info('Found new emails for user %s: %s %s' % (name, email, email_k))
                        if email is not None:
                            new_emails[email] = github_id
                        new_emails[email_k] = github_id
                if email == email_k:
                    if name_v not in (nickname, name):
                        log.warning(
                            'Found different name for user id %s: %s %s %s' % (github_id, name_v, nickname, name))
        row_num += 1

    # check for multiple emails
    c_add = list()
    c_remove = list()
    row_num = 0
    for c in core_team:
        if row_num != 0:
            nickname, name, email, github_id = c
            keys = [k for k, v in new_emails.iteritems() if v == github_id]
            if len(keys) > 0:
                emails = ':'.join(keys)
                c_new = (nickname, name, emails, github_id)
                c_add.append(c_new)
                c_remove.append(c)
        row_num += 1

    for c in c_remove:
        core_team.remove(c)
    for c in c_add:
        core_team.append(c)

    log.info('Saving file')
    file_utils.save_corpus(corpus=core_team, filename='{0}-coreteam.csv'.format(repo))
    _file.close()
    log.info('Done')
else:
    # If response code is not ok (200), print the resulting http error code with description
    response.raise_for_status()
    log.error('HTTP request failed')
    sys.exit(-1)


# emails = gh.users.emails.list()

# gh = Github(user=user, repo=repo)
# gh.repos.set_credentials(login='bateman', password='77eraPS3')
# #gh.repos.set_token(token='2f4f0e4d7ced015a65fce4464e90ee0d5a5e6ded')
# log.info('Using repo %s/%s' % (user, repo))
# for _login, _id in contributors:
#     user = gh.users.get(_login)
#     core_team.append((_login, user.name, user.email, _id))
