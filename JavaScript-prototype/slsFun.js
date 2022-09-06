
const fs = require('fs');
const yaml = require('js-yaml');
const UglifyJS = require('uglify-js');

function getSlsFun(ymlFile){
    // find yml file
    var seed_func = new Array();
    //if exsits, get handler content
    if(fs.existsSync(ymlFile)){
        // console.log("exist!")
        const doc = yaml.load(fs.readFileSync(ymlFile, 'utf-8'));
        // console.log(doc);

        Object.keys(doc["functions"]).forEach(function (item1){
            Object.keys(doc["functions"][item1]).forEach(function (item2){
                if(item2=="handler"){
                    // console.log("find"+doc["functions"][item1][item2]);
                    seed_func.push(doc["functions"][item1][item2]);
                    // console.log(seed_func);
                }
            })
        });
    }
    //if not exsits, use the next step to find entry functions, i.e., parse code

    return seed_func;
}


function parseCode(file_name){

    var code = fs.readFileSync(file_name, 'utf-8');
    var ast = UglifyJS.parse(code); 
    // ast.figure_out_scope();
    
    
    ast.walk(new UglifyJS.TreeWalker(function(node){
        console.log(node);
        
        // if(node instanceof UglifyJS.AST_Defun){
        //     console.log(node);
            // console.log(node.print_to_string({beautify: true}));
        // }
    }
    
    ));
    console.log("=======");
    // console.log(ast)
    



}



module.exports = getSlsFun;
