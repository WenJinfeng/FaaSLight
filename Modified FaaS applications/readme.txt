
This directory is to provide the modifed and optimized FaaS applications. Due to the file size limit of GitHub, you can see link: https://drive.google.com/drive/folders/1RvswL4Emzs4Btyqgk7GW2WhYO2TH7hWF?usp=share_link.

We have converted the FaaS applications for AWS to the format required by Google Cloud Functions and converted the applications for Google Cloud Functions to the format required by AWS. Then we have applied our approach to the converted applications to further demonstrate its generalization.

The slight code changes are about the definition formats of serverless functions to trigger the executions. For example, on AWS Lambda, input fields of Python-based and JavaScript-based serverless functions are filled with "event" and "context", while Google Cloud Functions-based serverless functions are filled with ``request''.
