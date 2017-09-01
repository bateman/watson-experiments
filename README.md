# watson-experiments

Currently supports only Apache Software Foundation (ASF) [projects](https://www.apache.org/index.html#projects-list)

## Steps

### 1. Extract emails from mbox archive
`$ sh mlstats-run.sh http://url.to/mailinglist/mbox/archive`

### 2. Extract pull requests from project's GitHub
`parse_pr.py`

### 3. Extract core-team (committers) members
`get_core_team.py`

### 4. Analyze propensity to trust (measure agreeableness score)
`tone-analyzer.py PROJECT_NAME`

### 5. Building dataset for logistic regression analysis
`prepare-datasets.py`
