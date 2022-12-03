# LambdaLite
Application-Level FaaS Optimization for Cold Start Latency in Serverless Computing

We aim to tackle this problem at the application level. Our guiding principle is to provide a vendor/platform-independent and developer-free technique that developers can easily adopt to optimize the cold start performance of FaaS applications on existing platforms. 
]
![image](https://user-images.githubusercontent.com/79156929/205443005-d5895a62-da5b-4fab-9a22-ac8291130223.png)

integrationFunMain.py is the approach overview of LambdaLite.



```Python
    # Preprocessing
    print("start")
    prepare()
    print("end")

    # Serverless function
    print("start")
    ymlFile,seedfun_list,entry_py,input_entry_point = serverless_func()
    print("end")

    # Magic function
    print("start")
    Identify_name,moshu_file = magic_func()
    print("end")

    # Constructing call graph 
    print("start")
    re_FunRel = construct_graph()
    print("end")

    # Initial useful function generation
    print("start")
    used_fun_result_output = initial_func()
    print("end")

    # Special rule query
    print("start")
    used_package_name,moshu_file_final,used_fun_result_output_final = special_rule()
    print("end")

    # Final useful function generation
    print("start")
    used_fun_result_output_final = final_rule()
    print("end")

    # Function-level rewriting
    print("start")
    used_fun_result_output_final_re,buits_list_file = func_rewrite()
    print("end")

```

After the serverless function is processed by the above LambdaLite, it can be run on AWS Lambda again.

The script to invoke the serverless function executed on AWS Lambda and obtain the performance result is in InvokeScript/invokeFunctionScript.py.

The script to invoke the serverless function executed on Google Cloud Functions and obtain the performance result is in InvokeScript/invokeCoogleFunction.py

In addition, we implement the JavaScript prototype of our approach in the directory JavaScript-prototype.

The directory "Modified FaaS applications" is to provide the modifed and optimized FaaS applications

