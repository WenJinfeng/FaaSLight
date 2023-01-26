# FaaSLight: General Application-Level FaaS Optimization for Cold Start Latency in Serverless Computing


This work has been accepted in **ACM Transactions on Software Engineering and Methodology (TOSEM)**.

We aim to tackle this problem at the application level. Our guiding principle is to provide a vendor/platform-independent and developer-free technique that developers can easily adopt to optimize the cold start performance of FaaS applications on existing platforms. 


<img width="636" alt="image" src="https://user-images.githubusercontent.com/51308506/214823513-996e33d2-5160-4770-8323-dfdbadf02efc.png">


integrationFunMain.py is the approach overview of FaaSLight.

After the serverless function is processed by the above FaaSLight, it can be run on AWS Lambda again.

The script to invoke the serverless function executed on AWS Lambda and obtain the performance result is in InvokeScript/invokeFunctionScript.py.

The script to invoke the serverless function executed on Google Cloud Functions and obtain the performance result is in InvokeScript/invokeCoogleFunction.py

In addition, we implement the JavaScript prototype of our approach in the directory JavaScript-prototype.

The directory "Modified FaaS applications" is to provide the modifed and optimized FaaS applications.

