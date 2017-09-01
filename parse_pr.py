import logging
import traceback

from pygithub3 import Github
from pygithub3 import exceptions

from utils import file_utils

logging.basicConfig()
log = logging.getLogger('PARSE-PR')
log.setLevel(logging.INFO)

user = 'apache'
repo = 'drill'

gh = Github(user=user, repo=repo)
gh.repos.set_token(token='*****')
log.info('Got repo %s/%s ' % (user, repo))

pull_requests = gh.pull_requests.list(state='closed').all()
closed_pull_requests = list()
header = ('url', 'owner', 'committer', 'decision', 'submission date', 'decision date')
closed_pull_requests.append(header)

log.info('Parsing closed pull requests')
for pr in pull_requests:
    merged_at = None
    created_at = pr.created_at
    url = pr.html_url
    owner = pr.user['login']
    state = pr.state
    committer = None
    if pr.merged_at is not None or pr.merge_commit_sha is not None:
        state = 'merged'
        sha = pr.merge_commit_sha
        try:
            commit = gh.repos.commits.get(sha=sha)
            committer = commit.author
        except exceptions.NotFound:
            log.warning('Cannot find commit for pr %s' % url)
            continue
        if pr.merged_at is None:
            merged_at = pr.closed_at

    row = (url, owner, committer, state, created_at, merged_at)
    closed_pull_requests.append(row)

file_utils.save_corpus(corpus=closed_pull_requests, filename='{0}-closed-pullrequests.csv'.format(repo))

pull_requests = gh.pull_requests.list(state='open').all()
open_pull_requests = list()
header = ('url', 'owner', 'commenter', 'decision', 'submission date', 'last comment')
open_pull_requests.append(header)

log.info('Parsing open pull requests')
for pr in pull_requests:
    created_at = pr.created_at
    last_commented_at = None
    url = pr.html_url
    state = pr.state
    owner = pr.user['login']
    commenter = None
    commenters = dict()
    try:
        comments = gh.pull_requests.comments.list(number=pr.number).all()
        for c in comments:
            try:
                nc = commenters[c.user['login']]
                commenters[c.user['login']] = nc + 1
            except KeyError:
                commenters[c.user['login']] = 1

        # TODO improve this
        if len(commenters) > 0:
            commenter, _ = sorted(commenters.iteritems(), key=lambda (k, v): (v, k), reverse=True).pop(0)
        else:
            commenter = owner
    except:
        log.warning('Error trying to get comments for pr %s' % url)
        traceback.print_exc()
        pass

    row = (url, owner, commenter, state, created_at, last_commented_at)
    open_pull_requests.append(row)

file_utils.save_corpus(corpus=open_pull_requests, filename='{0}-open-pullrequests.csv'.format(repo))

log.info('Done')
