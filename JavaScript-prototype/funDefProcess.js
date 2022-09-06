var U2 = require("uglify-js");
const fs = require('fs');
const path = require('path');
const R = require('ramda');
const rootDir=[];

function add_loginfo(code, inputfile, rootDir) {

    var file_name = inputfile.replace(rootDir, '').replace(/\.js$/, '');
    // var file_name ="ssssss";
    var ast = U2.parse(code);

    // accumulate `parseInt()` nodes in this array
    // var parseint_nodes = [];
    ast.walk(new U2.TreeWalker(function(node){
        if (node instanceof U2.AST_Defun) {
            // parseint_nodes.push(node);
            var fun_name = R.path(['name', 'name'], node);
            var codeStr = `${file_name}=${fun_name}`.toString();
            codeStr = "console.log('"+codeStr+"')";
            console.log(codeStr);
            // var codeStr = "console.log(${file_name}=${fun_name})";
            // var codeStr = "console.log(\"hello\")";
            let addnode = transProgram(codeStr);
            node.body = addnode.body.concat(node.body)
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
function inserthandlerJS(filePath){
    if(rootDir.length==0){
        rootDir.push(filePath);
    }
    //read all file list
    fs.readdir(filePath,function(err,files){
        if(err){
            console.warn(err)
        }else{
            //read all file list
            files.forEach(function(filename){
                //get the absolute path of the current file
                var filedir = path.join(filePath, filename);
                // console.log(filedir);
                //return fs.Stats object
                fs.stat(filedir,function(eror, stats){
                    if(eror){
                        console.warn('obtain file stats failed');
                    }else{
                        var isFile = stats.isFile();//is file
                        var isDir = stats.isDirectory();//is directory
                        // console.log(isFile)
                        if(isFile&&(filename.endsWith("\.js"))&&!filename.startsWith("\.")){
                            console.log(filedir);// read content
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
                            inserthandlerJS(filedir);
                            
                        }
                    }
                })
            });
        }
    });
}

module.exports = inserthandlerJS;