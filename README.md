# LambdaLite
Application-Level Optimization for Cold Start Latency in Serverless Computing

We aim to tackle this problem at the application level. Our guiding principle is to provide a vendor/platform-independent and developer-free technique that developers can easily adopt to optimize the cold start latency of serverless functions on existing platforms. 

<img width="605" alt="image" src="https://user-images.githubusercontent.com/79156929/190913660-04f93abb-980b-4e15-93b2-733c636d9ae4.png">

integrationFunMain.py is the approach overview of LambdaLite.



```Python
    # Step1: Optional File Elimination
    print("step1 start")
    prepare()
    print("step1 end")

    # Step2: Serverless Function Recognition
    print("step2 start")
    ymlFile,seedfun_list,entry_py,input_entry_point = serverless_func()
    print("step2 end")

    # Step3: Special Function Recognition
    print("step3 start")
    Identify_name,moshu_file = magic_func()
    used_package_name,moshu_file_final,used_fun_result_output_final = special_rule()
    print("step3 end")

    # Step4: Optional Function Generation 
    print("step4 start")
    re_FunRel = construct_graph()
    used_fun_result_output = initial_func()
    print("step4 end")

    # Step5: Function-level Rewriting
    print("step5 start")
    used_fun_result_output_final_re,buits_list_file = func_rewrite()
    print("step5 end")
```

After the serverless function is processed by the above LambdaLite, it can be run on AWS Lambda again.

The script to invoke the serverless function executed on AWS Lambda and obtain the performance result is in InvokeScript/invokeFunctionScript.py.

The script to invoke the serverless function executed on Google Cloud Functions and obtain the performance result is in InvokeScript/invokeCoogleFunction.py

In addition, we implement the JavaScript prototype of our approach in the directory JavaScript-prototype.

