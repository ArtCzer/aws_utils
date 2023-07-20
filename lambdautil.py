import json
import sys
import subprocess
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
    
    if op=="help":
        print("NAME:")
        print("  lambdautil")
        print("SYNOPSIS:")
        print("  Provide a wrapper around `aws lambda` CLI to help manage AWS Lambda versions")
        print("USAGE:")
        print("  lambdautil <operation> --fn <function name> <...other parameters>")
        print("OPERATIONS:")
        print("  list   - lists version for the specified function")
        print("  update - updates the live version for the specified function")
        print("  help   - display this help text")
        print("PARAMETERS:")
        print("  --fn      - specify the funtion name")
        print("  --version - specify the version to update to")
        sys.exit("")

    if function_name=="":
        sys.exit("Function name not specified, use --fn <function_name> to specify a function")
    
    if op=="list-versions-by-function":
        print("Version list for ",function_name)
        process = subprocess.run(['aws','lambda',op,'--function-name',function_name], 
            stdout=subprocess.PIPE, 
            universal_newlines=True)
        versions = json.loads(process.stdout)
        for i, arg in enumerate(versions["Versions"]):
            print("Version: ", arg["Version"],"Date: ",arg["LastModified"], " Description: ", arg["Description"])
    
    if op=="update-alias":
        if version=="":
            sys.exit("Version not specified, use --version <version_number> to specify a function version")
        print("Updating version for ",function_name)
        process = subprocess.run(['aws','lambda',op,'--function-name',function_name,'--function-version',version,'--name',alias], 
            stdout=subprocess.PIPE, 
            universal_newlines=True)

    process = subprocess.run(['aws','lambda',"get-alias",'--function-name',function_name,"--name",alias], 
        stdout=subprocess.PIPE, 
        universal_newlines=True)
    live = json.loads(process.stdout)
    print("Live version: ",live["FunctionVersion"])