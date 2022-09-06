
const fs = require('fs');
const zlib = require('zlib'); 
function rewrite_template(findKey, funname,returnnum){
    
    //return format generation
    var return_string = "";
    
    if(returnnum!=0){
        return_string = "global['r0']="

    }


    var LOC = "";
    var callRel;

    // console.log(global["clearInterval"])
    if(!Object.keys(global).includes("on_demand_loading")){
        var readBuffer1 = fs.readFileSync("gzip.gzip")
        var decodeBuffer1 = zlib.unzipSync(readBuffer1)
        global['on_demand_loading']= JSON.parse(decodeBuffer1.toString('utf-8'));
        // var data = fs.readFileSync("gzip.json");
        // global['on_demand_loading'] = JSON.parse(data);

    }
    
    LOC = global['on_demand_loading'][findKey];

    // LOC = fs.readFileSync("gzipinfo.txt", 'utf-8');

    
    // console.log(funname);

    LOC = LOC+"\n"+return_string+funname+";";
    // console.log(LOC);

    // eval(LOC);
    return LOC;
}


module.exports.rewrite_template = rewrite_template;
