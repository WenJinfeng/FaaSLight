# LambdaLite
Function-Level Optimization for Cold Start Latency in Serverless Computing

We aim to tackle this problem at the serverless function level. Our guiding principle is to provide a vendor/platform-independent and developer-free technique that developers can easily adopt to optimize the cold start latency of serverless functions on existing platforms. 

<img width="605" alt="image" src="https://user-images.githubusercontent.com/79156929/168273305-a86da262-6316-4727-816f-a4ea6ed6e879.png">

integrationFunMain.py is the approach overview of LambdaLite.



```Python

    # Step1: Preprocessing
    print("step1 start")
    prepare()
    print("step1 end")

    # Step2: Serverless function
    print("step2 start")
    ymlFile,seedfun_list,entry_py,input_entry_point = serverless_func()
    print("step2 end")

    # Step3: Magic function
    print("step3 start")
    Identify_name,moshu_file = magic_func()
    print("step3 end")

    # Step4: Constructing call graph 
    print("step4 start")
    re_FunRel = construct_graph()
    print("step4 end")

    # Step5: Initial indispensable function generation
    print("step5 start")
    used_fun_result_output = initial_func()
    print("step5 end")

    # Step6: Special rule query
    print("step6 start")
    used_package_name,moshu_file_final,used_fun_result_output_final = special_rule()
    print("step6 end")

    # Step7: Function-level rewriting
    print("step7 start")
    used_fun_result_output_final_re,buits_list_file = func_rewrite()
    print("step7 end")
```

After the serverless function is processed by the above LambdaLite, it can be run on AWS Lambda again.

The script to invoke the serverless function and obtain the performance result is in InvokeScript/invokeFunctionScript.py.

In addition, we implement the JavaScript prototype of our approach in the directory JavaScript-prototype.

