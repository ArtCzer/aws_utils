import json
import sys
import subprocess
import boto3

if __name__ == "__main__":
    function_name = ""
    op = "help"
    version = ""
    alias = 'live'
    # print(f"Arguments count: {len(sys.argv)}")
    for i, arg in enumerate(sys.argv):
        if arg=="list":
            op="list-versions-by-function"
        if arg=="update":
            op="update-alias"
        if arg=="--fn":
            function_name=sys.argv[i+1]
        if arg=="--version":
            version=sys.argv[i+1]
        if arg=="--alias":
            alias=sys.argv[i+1]
    if op=="help":
        print("NAME:")
        print("  lambdautil")
        print("")
        print("SYNOPSIS:")
        print("  Provide a wrapper around `aws lambda update-alias`to help manage AWS Lambda versions")
        print("")
        print("USAGE:")
        print("  lambdautil <operation> --fn <function name> <...other parameters>")
        print("")
        print("EAXMPLE:")
        print("  lambdautil list --fn <function name>")
        print("  - This will list all versions of the specified function")
        print("  lambdautil update --fn <function name> --version 12 --alias production")
        print("  - This will update the alias called 'production' to version 12")
        print("")
        print("OPERATIONS:")
        print("  list   - lists version for the specified function")
        print("  update - updates the live version for the specified function")
        print("  help   - [DEFAULT] display this help text")
        print("")
        print("PARAMETERS:")
        print("  --fn      - specifies the funtion name")
        print("  --version - specifies the version to update to")
        print("  --alias   - specifies the Alias name to update to (Default is 'live')")
        sys.exit("")

    if function_name=="":
        sys.exit("Function name not specified, use --fn <function_name> to specify a function")
    
    client = boto3.client('lambda')

    if op=="list-versions-by-function":
        print("Version list for ",function_name)
        versions = client.list_versions_by_function(FunctionName=function_name)
        for i, arg in enumerate(versions["Versions"]):
            print("Version: ", arg["Version"],"Date: ",arg["LastModified"], " Description: ", arg["Description"])
    
    if op=="update-alias":
        if version=="":
            sys.exit("Version not specified, use --version <version_number> to specify a function version")
        print("Updating version for ",function_name)
        process = client.update_alias(FunctionName=function_name,FunctionVersion=version,Name=alias)
    
    live = client.get_alias(FunctionName=function_name,Name=alias)
    print("Live version: ",live["FunctionVersion"])