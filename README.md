## Summary
Tool to help manage AWS Lambda Versions
Compatible with Linux, MacOS and Windows, Python 3 and above. 

You can use this tool to help roll back to previous versions of a Lambda function

## Prerequisites
- AWS IAM user credentials set up as a default profile
- Required permissions:
  - "lambda:ListVersionsByFunction",
  - "lambda:GetAlias",
  - "lambda:UpdateAlias"
## Example Usage
  lambdautil list --fn <function name>
  - This will list all versions of the specified function
  lambdautil update --fn <function name> --version 12 --alias production
  - This will update the alias called 'production' to version 12

## Example Output
Version list for  my-lambda-function-D6r1i2eIQ2nA
Version:  1 Date:  2023-07-19T05:14:04.000+0000  Description:  v1.0 Initial_commit
Version:  2 Date:  2023-07-19T05:27:27.000+0000  Description:  v1.1 some changes
Version:  3 Date:  2023-07-19T22:55:19.000+0000  Description:  v1.2 some changes
Version:  4 Date:  2023-07-19T23:02:11.000+0000  Description:  v1.3 some changes
Version:  5 Date:  2023-07-19T23:34:59.000+0000  Description:  v1.4 some changes

