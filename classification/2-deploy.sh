#!/bin/bash

cd ../dashboard
npm run build
cd ../classification

sls deploy --region us-east-1
sls deploy --region ap-southeast-1