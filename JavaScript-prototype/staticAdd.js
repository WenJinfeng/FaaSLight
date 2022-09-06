
const fs = require('fs');
const UglifyJS = require('uglify-js');
const R = require('ramda');
const path = require('path');


//represent as file----function

const localize = (currentFile, fn) => fn ? `${currentFile}----${fn}` : `${currentFile}`
const callRel = {};
const softConn = 
{"request":"node_modules/request/index",
"rss":"node_modules/rss/lib/index",
"xml":"node_modules/xml/lib/xml",
"extend":"node_modules/extend/index",
"cheerio":"node_modules/cheerio/lib/cheerio",
"moment-timezone":"node_modules/moment-timezone/moment-timezone",
"aws-sdk":"node_modules/aws-sdk/lib/aws",
"sharp":"node_modules/sharp/lib/index"
};
const definedFunctions = [];

const rootDir=[];



function add_info(input, rootDir, app_name){

    var currentFile = input.replace(rootDir, '').replace(/\.js$/, '');
 

    var code = fs.readFileSync(input, 'utf-8');
    // store path level informaton
    // const localModules = [];
    // console.log(code);

    // definedFunctions.push(localize(currentFile, 'Program'));
    var toplevel;
    try{
        toplevel = UglifyJS.parse(code);
    }catch(e){
        console.log(e);
    }
    var calls = [];
    var relatedPackage = {};
    // console.log(toplevel);
    const walker = new UglifyJS.TreeWalker(function(node){
        //check for function calls
        const isDefinition = node instanceof UglifyJS.AST_Definitions;
        const isCall = node instanceof UglifyJS.AST_Call;
        const isDefun = node instanceof UglifyJS.AST_Defun;
        const isDotAccess = node instanceof UglifyJS.AST_Dot;
        const isSimpleStatement = node instanceof UglifyJS.AST_SimpleStatement;
        const isAssign = node instanceof UglifyJS.AST_Assign
 
        if(isAssign && (node.right instanceof UglifyJS.AST_Call) && (typeof(node.right.expression.name)!='object') && node.right.args[0] && node.right.args[0].value && (typeof(node.right.args[0].value)!='object') &&(node.right.expression.name =="require"&& typeof(node.left.property)!='object')){
            // console.log(node.right.args[0].value);
            // console.log(node.left.property);
            local_name = node.left.property;
            location_name = node.right.args[0].value;


            if(!Object.keys(relatedPackage).includes(local_name)){
                relatedPackage[local_name]=location_name;
                
            }
            
            
        }

        if(isDefinition){
            if(node.definitions[0].value && node.definitions[0].value.expression && node.definitions[0].value.expression.name === 'require'){
                // console.log()
                const localName = R.pipe(R.head, R.path(['name', 'name']))(node.definitions);
                // console.log(typeof(localName))
                // if(typeof(localName)!='string'){
                //     // console.log(localName.length)
                //     localName = node.definitions.name.names[0].key;
                // }


                
                const location = node.definitions[0].value.args[0].value;
                // console.log([localName, location]);
                if(!Object.keys(relatedPackage).includes(localName)){
                    relatedPackage[localName]=location;
                }
                
                //match path level
                // if(/^\./.test(location)){
                //     localModules.push([localName, location]);
                // }
                // console.log(/^\./.test(location));
            }
            
            // console.log(relatedPackage);
        }else if(isCall || isDotAccess){
            // console.log(node.print_to_string({ beautify: true }))

            if(typeof(node.expression.name)!="object"){
                if(isCall && /(Number|Date|callback|require)/.test(node.expression.name)){
                
                    return;
                }
            }
            
            

            var p =walker.find_parent(UglifyJS.AST_Defun);
            // console.log(p instanceof UglifyJS.AST_Defun)
            var name = R.path(['name', 'name'], p);
            // console.log('name------'+p.name.name)

            
            

            if(isCall && node.expression.name !== undefined){
                
                // is common call of functions

                var tmpCuttentFile1 = currentFile;
                var tmpCuttentFile2 = currentFile;

                if(Object.keys(relatedPackage).includes(name)){
                    tmpCuttentFile1 = relatedPackage[name];
                    if(/^\./.test(tmpCuttentFile1)){
                        let oo = tmpCuttentFile1.replace("\.\/","");
                        let newCurrentFile = currentFile.split("\/");
                        let bb = newCurrentFile.length;
                        newCurrentFile.length = bb-1;
                        newCurrentFile.push(oo);
                        //cat string
    
                        tmpCuttentFile1 = newCurrentFile.join('/');
                        // console.log(newCurrentFile);
                    }
                    if(Object.keys(softConn).includes(tmpCuttentFile1)){
                        tmpCuttentFile1 = softConn[tmpCuttentFile1];
                    }
                    
                }else if(Object.keys(relatedPackage).includes(node.expression.name)){
                    tmpCuttentFile2 = relatedPackage[node.expression.name];
                    if(/^\./.test(tmpCuttentFile2)){
                        let oo = tmpCuttentFile2.replace("\.\/","");
                        let newCurrentFile = currentFile.split("\/");
                        let bb = newCurrentFile.length;
                        newCurrentFile.length = bb-1;
                        newCurrentFile.push(oo);
                        //cat string
    
                        tmpCuttentFile2 = newCurrentFile.join('/');
                        // console.log(newCurrentFile);
                    }
                    if(Object.keys(softConn).includes(tmpCuttentFile2)){
                        tmpCuttentFile2 = softConn[tmpCuttentFile2];
                    }
                }
                if((typeof(name)!="object")&&(typeof(node.expression.name)!="object")){

                    calls.push([localize(tmpCuttentFile1, name), localize(tmpCuttentFile2, node.expression.name)]);
                    // console.log(calls)
                }
                
            }else{
                // console.log("-------")
                let module, prop;
                if(isCall){
                    // method call
                    module = node.expression.start.value;
                    prop = node.expression.property;
                }else if(isDotAccess){
                    module = node.start.value;
                    prop = node.property;
                }
                if(Object.keys(relatedPackage).includes(module)){
                    let tmplocation = relatedPackage[module];
                    if(/^\./.test(tmplocation)){
                        let oo = tmplocation.replace("\.\/","");
                        let newCurrentFile = currentFile.split("\/");
                        let bb = newCurrentFile.length;
                        newCurrentFile.length = bb-1;
                        newCurrentFile.push(oo);
                        //cat string
        
                        tmplocation = newCurrentFile.join('/');
                        // console.log(newCurrentFile);
                    }
                    if(Object.keys(softConn).includes(tmplocation)){
                        tmplocation = softConn[tmplocation];
                    }

                    if((typeof(name)!="object")&&(typeof(prop)!="object")){
                        calls.push([localize(currentFile, name), localize(tmplocation, prop)]);
                    }
                    
                }


            }
            
        }else if(isSimpleStatement){
            // console.log("===");
            // console.log(node.body);

            // specific for module.exports = xxx connection;
            if(node.body instanceof UglifyJS.AST_Assign){
                if(node.body.start.value=="module" && node.body.operator == "="){
                    if(node.body.right.name){
                        if(typeof(node.body.right.name)!="object"){
                            calls.push([localize(currentFile), localize(currentFile, node.body.right.name)]);
                        }
                        
                    }else if(node.body.right.right && node.body.right.right.name){
                        if(typeof(node.body.right.right.name)!="object"){
                            calls.push([localize(currentFile), localize(currentFile, node.body.right.right.name)]);
                        }
                        
                    }
                    
                }
                // console.log(node.body.left.property);
                // console.log(node.body.operator);
                // console.log(node.body.right.name);
            }



            // console.log(node.body.left.property);
            // console.log(node.body.right.name);

            
            // definedFunctions.push(localize(currentFile, R.path(['name', 'name'], node)));
            // console.log(localize(currentFile, R.path(['name', 'name'], node)))
        }else if(isDefun){
            if(typeof(node.name.name)!="object"){
                definedFunctions.push(localize(currentFile, node.name.name));
            }
            
        }
    
    })
    // console.log("===");
    toplevel.walk(walker);
    // try{
    //     toplevel.walk(walker);
    // }catch(e){
    //     console.log(e)
    // }
    // console.log(calls);
    //handler calls format
    
    for (let i in calls){
        // console.log(calls[i]);
        // callRel[calls[i][0]].push(calls[i][1]);
        if(!Object.keys(callRel).includes(calls[i][0])){
            callRel[calls[i][0]]=[]
            callRel[calls[i][0]].push(calls[i][1]);

        }else{
            callRel[calls[i][0]].push(calls[i][1]);
            
            callRel[calls[i][0]] = Array.from(new Set(callRel[calls[i][0]]));
        }
        
        
    }
    // console.log(relatedPackage);
    // console.log(callRel);
    console.log("---------------")
    saveCGData(callRel, app_name);
    // saveFunDef(definedFunctions, app_name);

    // return callRel;


}





function saveCGData(callRel, app_name){
    // write json data
    let str = JSON.stringify(callRel,"","\t");
    fs.writeFile("cg/"+app_name+".json",str, function(err){
        if(err){
            console.log("write error");
        }
    });


}
function saveFunDef(definedFunctions, app_name){
    // write json data
    let str = JSON.stringify(definedFunctions,"","\t");
    fs.writeFile("fundef/"+app_name+".json",str, function(err){
        if(err){
            console.log("write error");
        }
    });

    //read json data
    // fs.readFile('output.json', "utf-8", function (err, data) {
    //     if (err) {
    //         console.log(err);
    //     }
    //     var person = JSON.parse(data);
    //     console.log(person)
           
    // })
}


function iterationCG(filePath, app_name){
    if(rootDir.length==0){
        rootDir.push(filePath);
    }
    
    fs.readdir(filePath,function(err,files){
        if(err){
            console.warn(err)
        }else{
            
            files.forEach(function(filename){
                
                var filedir = path.join(filePath, filename);
                // console.log(filedir);
                
                fs.stat(filedir,function(eror, stats){
                    if(eror){
                        console.warn('obtain file stats failed');
                    }else{
                        var isFile = stats.isFile();
                        var isDir = stats.isDirectory();
                        // console.log(isFile)
                        if(isFile&&(filename.endsWith("\.js"))&&!filename.startsWith("\.")){
                            console.log(filedir);
                            // var content = fs.readFileSync(filedir, 'utf-8');
                            // console.log(content);
                            add_info(filedir, rootDir[0], app_name);


                        }
                        if(isDir){
                            iterationCG(filedir, app_name);
                            
                        }
                    }
                })
            });
        }
    });
}



module.exports = iterationCG;
