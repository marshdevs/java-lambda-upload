***1. java-lambda-upload:***
Automated solution for uploading Java code changes to AWS Lambda function. 

Takes a new .jar file, replaces the previous .jar in S3, and modifies the function code in Lambda. This change is not published as a new version.

**1.** Build .jar artifact

**2.** Run java-lambda-upload.py

**3.** Test lambda function

***2. cpp_driver.py:*** Acts as an interactive file manager for writing C++ code. Automates the ls, g++, and rm commands.
