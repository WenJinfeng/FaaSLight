# LambdaLite
Application-level Performance Optimization for Serverless Computing

We aim to optimize the cold start time from the application developers' perspective. Our appraoch is a vendor- and platform-independent technique that application developers can adopt.

integrationFunMain.py is the approach overview of LambdaLite.

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

    # Step5: Initial useful function generation
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

