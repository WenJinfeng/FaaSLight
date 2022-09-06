const path = require('path');
const fs = require('fs');




function getFunListfromSeed(seed_name,input_package, app_name){
    // handler seed functions format
    var seed_name_new = [];
    seed_name.forEach(s_n => {
    let fun_name = s_n.split("\.").pop();
    s_n_new = s_n.replace("\."+fun_name, "") + "----"+fun_name;
    seed_name_new.push(s_n_new);
    // console.log(seed_name_new);
    });
    
    //read json data about call graph data
    data = fs.readFileSync("cg/"+app_name+".json");
    var callRel = JSON.parse(data);

    //start get inital function set through seed functions
    var use_func = [];
    use_func = use_func.concat(seed_name_new);
    // use_func = Array.from(new Set(use_func));
    use_func.forEach(use_func_i =>{
        let temp_key = use_func_i.split("----");
        //temp_key[0] represent file location
        //temp_key[1] represent function name
        let new_data = [];
        // console.log(callRel[use_func_i]);
        // console.log(temp_key[1]);
        new_data = new_data.concat(callRel[temp_key[0]]);
        new_data = new_data.concat(callRel[use_func_i]);
        use_func = use_func.concat(new_data);
        use_func = Array.from(new Set(use_func));
    });

    //test using a key seed
    // use_func = ['node_modules/request/index----request']

    var use_func_size=0;
    var num = 0;
    // var size = use_func.length;
    while(use_func.length > use_func_size){
        num = num +1;
        console.log("iteration for " + num + " time");
        use_func_size = use_func.length;
        let add_data = [];
        //start add data
        use_func.forEach(fun_j =>{
            console.log("-----------"+fun_j);
            if(fun_j && (fun_j.indexOf("----")!=-1)){//appear
                let temp_key = fun_j.split("----");
                if(Object.keys(callRel).includes(temp_key[0])){
                    add_data = add_data.concat(callRel[temp_key[0]]);
                    add_data.push(temp_key[0]);
                }
                if(Object.keys(callRel).includes(fun_j)){
                    add_data = add_data.concat(callRel[fun_j]);
                }
                
                
            }else{
                if(Object.keys(callRel).includes(fun_j)){
                    add_data = add_data.concat(callRel[fun_j]);
                }
                
            }
            // console.log(add_data);
            
        });
        use_func = use_func.concat(add_data);
        use_func = Array.from(new Set(use_func));
    }


    //write to file one by one 
    fWriteName = "result/"+app_name+".txt";
    var fWrite = fs.createWriteStream(fWriteName);
    use_func.forEach(each_fun =>{
        fWrite.write(each_fun+"\n");
    });

    // //read function one by one
    // var rl = readline.createInterface({
    //     input: fs.createReadStream(path.join(input_package,"use_fun.txt"))
    // });
    // rl.on('line', line => {
    //     console.log(line);
    //   })







    // console.log(use_func);



}



module.exports = getFunListfromSeed;