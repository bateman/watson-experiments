#!/usr/bin/env bash
#mongoexport -h localhost -d github -c pull_requests --type=csv --fields html_url,user.login,merged_by.login,state,created_at,merged_at -q '{"owner":"$1", "repo":"$2", "state":"closed"}' --out "$2-closed-pullrequests.csv"

mongoexport -h localhost -d github -c pull_requests --type=csv --fields html_url,user.login,merged_by.login,state,created_at,merged_at -q '{"owner":"apache", "repo":"drill", "state":"closed"}' --out "closed-pullrequests.csv"
