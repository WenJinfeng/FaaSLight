const fs = require('fs');
var exec = require('child_process').exec;

const input_package  = "AppX_path/"
var app_name = "AppX";


//Preprocessing
//-------------------------------------------

const deleteFiles = require('./removeFile');
deleteFiles(input_package);




// Serverless function 
//-------------------------------------------

var seed_func = [];
var ymlFile = input_package +"/"+"serverless.yml";
const getSlsFun = require('./slsFun');
const seed_func = getSlsFun(ymlFile);
console.log(seed_func);//[ 'handler.list', 'handler.show' ]





//Constructing call graph 
//get call graph information to cgInfo.json
//-------------------------------------------

const iterationCG = require("./staticAdd");
iterationCG(input_package, app_name);





// Initial indispensable function generation
//-------------------------------------------

const getFunListfromSeed = require("./initialFun");
getFunListfromSeed(seed_func, input_package, app_name);





// Special rule query, such as preload functions 
//-------------------------------------------


//6.1 Obtain pre-loaded functions related with some package, via offline and dynamic ways. 
var log_name = app_name+".log";

//get a application copy
var new_input_package = input_package.substring(0,input_package.length-1)+"-copy";
var fse = require("fs-extra"); 

fse.copy(input_package.substring(0,input_package.length-1), new_input_package, (err)=>{
    if(err){
        console.log("Error");
    }
});

//start to add console information
var inserthandlerJS = require("./funDefProcess");
inserthandlerJS(new_input_package+"/");

//save pre-loaded log result
var cmdStr = "node "+new_input_package+"/handler.js > log/"+log_name;
// console.log(cmdStr)
exec(cmdStr, function(err,stout, stderr){
    if(err){
        console.log(stderr);
    }else{
        console.log(stout);
    }
});
console.log("complete")


//whitelist customization
customWhiteFun = [];


//Generate the final use functions related to the test code.
//connect initial result/+log/+customWhiteFun --- all used function
//save used function into result/XX-final.txt
const resultPro = require("./result_process");
resultPro(app_name, customWhiteFun);




// Function-level rewriting
//-------------------------------------------

const handlerJS = require('./funRewrite');
handlerJS(input_package, app_name);

//copy required files, then execute serverless function on the serverlese platform


fs.copyFile("gzip.gzip", input_package+"gzip.gzip", (err)=>{
    if(err){
        console.log("Error");
    }
});

fs.copyFile("templateCall.js", input_package+"node_modules/templateCall.js", (err)=>{
    if(err){
        console.log("Error");
    }
});

