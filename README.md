

```bash
cd aws_batch_fargate_stack/lambda_list_files
rm code.zip
zip code.zip lambda_function.py
aws s3 cp code.zip s3://awstests-lavkge/src/code.zip


YAML_CONF=file:///Users/gaetan/Documents/dev/AWS/first_tests/aws_batch_fargate_stack/stack.yaml

aws cloudformation create-stack --stack-name NOAAFargateJobStack --template-body $YAML_CONF --capabilities CAPABILITY_NAMED_IAM

aws cloudformation update-stack \
  --stack-name NOAAFargateJobStack \
  --template-body $YAML_CONF \
  --capabilities CAPABILITY_NAMED_IAM

```
