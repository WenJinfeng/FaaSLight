# LambdaLite
Application-level Performance Optimization for Serverless Computing

We aim to optimize the cold start time from the application developers' perspective. Our appraoch is a vendor- and platform-independent technique that application developers can adopt.

intergrationFunMain.py is the approach overview of LambdaLite.

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

    time_tmp = time.time()

    # Step4: Constructing call graph 
    print("step4 start")
    re_FunRel = construct_graph()
    print("step4 end")

    time_end = time.time()
    print("Spending of step4:"+str(time_end-time_tmp))

    # Step5: Initial useful function generation
    print("step5 start")
    used_fun_result_output = initial_func()
    print("step5 end")

    # Step6: Special rule query
    print("step6 start")
    used_package_name,moshu_file_final = special_rule()
    print("step6 end")

    # Step7: Final useful function generation
    print("step7 start")
    used_fun_result_output_final = final_rule()
    print("step7 end")

    # Step8: Function-level rewriting
    print("step8 start")
    used_fun_result_output_final_re,buits_list_file = func_rewrite()
    print("step8 end")

    # Step9: Import-level rewriting
    print("step9 start")
    import_rewrite()
    print("step9 end")

    time_tmp = time.time()
    print("All spending:"+str(time_tmp-time_start))
