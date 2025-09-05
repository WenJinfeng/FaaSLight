# FaaSLight: General Application-Level Cold-Start Latency Optimization for Function-as-a-Service in Serverless Computing


This work has been accepted in **ACM Transactions on Software Engineering and Methodology (TOSEM)**.

We aim to tackle this problem at the application level. Our guiding principle is to provide a vendor/platform-independent and developer-free technique that developers can easily adopt to optimize the cold start performance of FaaS applications on existing platforms. 

The tool code is located in the "FaaSLight_Tool" directory, with "integrationFun.ipynb" serving as the execution entry point of FaaSLight.

After the serverless function is processed by the above FaaSLight, it can be run on AWS Lambda or Google Cloud Functions again.

The script to invoke the serverless function executed on AWS Lambda and obtain the performance result is in InvokeScript/invokeFunctionScript.py.

The script to invoke the serverless function executed on Google Cloud Functions and obtain the performance result is in InvokeScript/invokeGoogleFunction.py

In addition, we implement the JavaScript prototype of our approach in the directory JavaScript-prototype.

The directory "Modified FaaS applications" is to provide the modifed FaaS applications (App1 - App22).

