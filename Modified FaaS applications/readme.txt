
This directory is to provide the modifed and optimized FaaS applications. Due to the file size limit of GitHub, you can see link: https://drive.google.com/drive/folders/1RvswL4Emzs4Btyqgk7GW2WhYO2TH7hWF?usp=share_link.

We have converted the FaaS applications for AWS to the format required by Google Cloud Functions and converted the applications for Google Cloud Functions to the format required by AWS. Then we have applied our approach to the converted applications to further demonstrate its generalization.

Specifically, App1 to App19 are originally developed for AWS Lambda. We manually convert these applications for AWS Lambda to the format required by Google Cloud Functions. App1 to App14 are written in Python, and the input field of their handler is converted from "event" and "context" as "request". App16 and App19 are written in JavaScript, and the input field of their handler is converted from "event", "context" and "callback" as "req" and "res". Meanwhile, variables about input fields are replaced to the corresponding varivales in the code body.

App20 to App22 are originally developed for Google Cloud Functions. They are written in Python, and the input field of their handler is converted from "request" as "event" and "context". Meanwhile, variables about input fields are replaced to the corresponding varivales in the code body.
