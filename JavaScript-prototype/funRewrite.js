var U2 = require("uglify-js");
const fs = require('fs');
const path = require('path');
const R = require('ramda');
const zlib = require('zlib')


const rootDir=[];
const use_func_info = [];
const AllFunDef={};

function add_loginfo(code, inputfile, rootDir) {
 
    // var file_name = inputfile.replace(rootDir, '').replace(/\.js$/, '');
    // var file_name ="ssssss";
    var ast = U2.parse(code);
    var localize = (currentFile, fn) => fn ? `${currentFile}----${fn}` : `${currentFile}`

    var currentFile = inputfile.replace(rootDir, '').replace(/\.js$/, '');
    
    //read used 

    

    // accumulate `parseInt()` nodes in this array
    // var parseint_nodes = [];
    ast.walk(new U2.TreeWalker(function(node){
        if (node instanceof U2.AST_Defun) {

            //check if this function is in used function list

            // console.log("function name====="+node.name.name);

            // console.log(node.print_to_string({beautify: true}));

            var fun_rep = localize(currentFile, R.path(['name', 'name'], node));


            if(!use_func_info.includes(fun_rep)){
                //line number >=3, then rewrite

                if(node.body.length>3){

                    //save function and rewrite funtion

                    //save function content,currentFile as key, function definication as value
                    AllFunDef[fun_rep] = node.print_to_string({beautify: true});
                    // console.log(AllFunDef)
    
                    //rewrite function
                    
                    var searFile = "templateCall.js";
                    var codeStr = "var customFun = require('"+searFile+"');";
                
                    // var codeStr = "var customFun = require('./templateCall');"
                    var tmp="";
                    node.argnames.forEach(argStr=>{
                        if(typeof(argStr.name)!="object"){
                            tmp = tmp+argStr.name+",";
                        }
                        
                        // console.log(argStr.name);
                    })
                    tmp=tmp.substring(0,tmp.length-1);
                    fun_n = `${node.name.name}`+"("+tmp+")";
                    var returnnum = 0;
                    var saveReturn = [];
                    node.body.forEach(codeline=>{
                        if(codeline instanceof U2.AST_Return){
                            saveReturn.push(codeline);
                        // console.log("hhhhh----"+codeline.value.name);
                            saveReturn[0].value = new U2.AST_SymbolRef({name:"r0"})
                        // saveReturn[0].value.name = "r0";
                        // saveReturn[0].value.value = "r0";

                        // console.log("hhhhh----"+saveReturn[0].value.name);
                            returnnum=1;
                        }
                    })
                    console.log(fun_rep);
                    codeStr = codeStr+"\n"+"var LOC = customFun.rewrite_template("+"\'"+fun_rep+"\',"+"\'"+fun_n+"\'"+","+returnnum+");";
                
                    codeStr = codeStr+"\n"+"eval(LOC);";

                    let addnode = transProgram(codeStr);
                    node.body = [];
                    node.body = addnode.body;
                    node.body= node.body.concat(saveReturn);


                }

            }

            // console.log(AllFunDef)
            saveUnusedFunc();
            





            // parseint_nodes.push(node);
            // var fun_name = R.path(['name', 'name'], node);
            // var codeStr = "var customFun = require('./templateCall');"

            // var codeStr = `${file_name}=${fun_name}`.toString();
            // codeStr = "console.log('"+codeStr+"')";
            // console.log(codeStr);
            // console.log(node.name.name);
            // var tmp="";
            // node.argnames.forEach(argStr=>{
            //     tmp = tmp+argStr.name+",";
            //     console.log(argStr.name);
            // })
            // tmp=tmp.substring(0,tmp.length-1);
            // fun_n = `${node.name.name}`+"("+tmp+")";

            // // var returnnum = 0;
            // var saveReturn = [];
            // node.body.forEach(codeline=>{
            //     if(codeline instanceof U2.AST_Return){
            //         saveReturn.push(codeline);
            //         // console.log("hhhhh----"+codeline.value.name);
            //         saveReturn[0].value.name = "r0";
            //         // returnnum=1;
            //     }
            // })
            
            // codeStr = codeStr+"\n"+"var LOC = customFun.rewrite_template("+"\'"+fun_n+"\'"+","+returnnum+");";
            // codeStr = codeStr+"\n"+"eval(LOC);";
            // if(returnnum!=0){
            //     // var reNode= U2.AST_Return("return r0")
            //     codeStr = codeStr+"\n"+"return r0;";
            // }
            // console.log(codeStr);

            // node.body


            // var codeStr = "console.log(${file_name}=${fun_name})";
            // var codeStr = "console.log(\"hello\")";
            // let addnode = transProgram(codeStr);
            // node.body = [];
            // addnode.body.push(reNode);
            // console.log(addnode.body)
            // node.body = addnode.body;
            //{value:new U2.AST_SymbolRef({name:"r0"})}
            // node.body = [];
            // if(returnnum!=0){
            //     var reNode= new U2.AST_Return({value:new U2.SymbolRef({})});
            //     // reNode.value.name = "r0";
            //     // codeStr = codeStr+"\n"+"return r0";
            // }
            // node.body= node.body.concat(saveReturn);
            // console.log(node.body.length)
            // let newnode = addnode.body.concat(node.body);
            // node.body = newnode.body;
        }
    }));


    return ast.print_to_string({ beautify: true });
    
}


//transfor a program as ast
function transProgram(codeStr){
    var ast1 = U2.parse(codeStr);
    // console.log(ast1.body);
    return ast1;
}

// test it

// function test() {
//     // zhushi
//     if (foo) {
//       parseInt('12342');
//     }
//     parseInt('0012', 3);
// }

// replace_parseint(test.toString());
// var codeStr = "console.log(\"hello\")";
// transProgram(codeStr);


//
function handlerJS(filePath, usedFun_file){
    if(rootDir.length==0){
        rootDir.push(filePath);
    }

    //read used function list
    var readata = fs.readFileSync("result/"+usedFun_file+"-final.txt", 'utf-8');
    var lines1=readata.split(/\r?\n/);
    lines1.forEach(line1 => {

        if(line1.indexOf("----")!=-1){
            use_func_info.push(line1);
        }

    });
    // console.log("used function information"+use_func_info)



    //read all file list
    fs.readdir(filePath,function(err,files){
        if(err){
            console.warn(err)
        }else{
            //read all file list
            files.forEach(function(filename){
                
                var filedir = path.join(filePath, filename);
                
                fs.stat(filedir,function(eror, stats){
                    if(eror){
                        console.warn('obtain file stats failed');
                    }else{
                        var isFile = stats.isFile();
                        var isDir = stats.isDirectory();
                        // console.log(isFile)
                        if(isFile&&(filename.endsWith("\.js"))&&!filename.startsWith("\.")){
                            console.log(filedir);
                            var content = fs.readFileSync(filedir, 'utf-8');
                            astCode = add_loginfo(content, filedir,rootDir[0]);
                            fs.writeFileSync(filedir,astCode, function(err){
                                if(err){
                                    console.log("write error");
                                }
                            });
                            console.log("write complete")

                            // console.log(content);
                            // add_info(filedir, rootDir[0]);


                        }
                        if(isDir){
                            handlerJS(filedir,usedFun_file);
                            
                        }
                    }
                })
            });
        }
    });

    
    // console.log(AllFunDef)
    // let str = JSON.stringify(AllFunDef,"","\t");
    // fs.writeFile("gzip.json",str, function(err){
    //     if(err){
    //         console.log("write error");
    //     }
    // });


}


function saveUnusedFunc(){
    // console.log("---------------save-----"+AllFunDef)
    let str = JSON.stringify(AllFunDef,"","\t");
    fs.writeFileSync("gzip.json",str, function(err){
        if(err){
            console.log("write error");
        }
    });
    var readBuffer = fs.readFileSync("gzip.json")
    var decodeBuffer = zlib.gzipSync(readBuffer)
    fs.writeFileSync("gzip.gzip",decodeBuffer)
}


module.exports = handlerJS;
