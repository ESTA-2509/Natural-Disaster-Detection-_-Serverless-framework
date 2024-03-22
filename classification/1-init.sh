#!/bin/bash

# sls create_domain --region us-east-1
# sls create_domain --region ap-southeast-1

aws dynamodb create-global-table \
  --global-table-name dfsys-db \
  --replication-group RegionName=us-east-1 RegionName=ap-southeast-1 \
  --region ap-southeast-1
