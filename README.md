# FaaSLight: General Application-Level Cold-Start Latency Optimization for Function-as-a-Service in Serverless Computing


This work has been accepted in **ACM Transactions on Software Engineering and Methodology (TOSEM)**.

We aim to tackle this problem at the application level. Our guiding principle is to provide a vendor/platform-independent and developer-free technique that developers can easily adopt to optimize the cold start performance of FaaS applications on existing platforms. 


<img width="636" alt="image" src="https://user-images.githubusercontent.com/51308506/214823513-996e33d2-5160-4770-8323-dfdbadf02efc.png">


integrationFunMain.py is the approach overview of FaaSLight.

After the serverless function is processed by the above FaaSLight, it can be run on AWS Lambda or Google Cloud Functions again.

The script to invoke the serverless function executed on AWS Lambda and obtain the performance result is in InvokeScript/invokeFunctionScript.py.

The script to invoke the serverless function executed on Google Cloud Functions and obtain the performance result is in InvokeScript/invokeGoogleFunction.py

In addition, we implement the JavaScript prototype of our approach in the directory JavaScript-prototype.

The directory "Modified FaaS applications" is to provide the modifed FaaS applications (App1 - App22).

### Install Python 3.9 along with pip and set it as default python3.9
```
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.9
sudo apt install python3.9-venv python3.9-distutils
curl -sS https://bootstrap.pypa.io/get-pip.py | sudo python3.9
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1
sudo update-alternatives --config python3
python3 --version
```

### Install Dependencies
```
pip install wrapt lazy-object-proxy
```

### Run the program along with application directory that you wanna analyze
```
python3 integrationFunMain.py application_directory
```