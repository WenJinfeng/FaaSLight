
var readline = require('readline');
const fs = require('fs');



//read function one by one
function resultPro(file_name, whitelist){
    var info_final = [];
    var info1 = [];
    var info2 = [];
    
    // read contents of file about inital function list
    var data1 = fs.readFileSync("result/"+file_name+".txt", 'utf-8');
    
    //split the contents by new line
    var lines1 = data1.split(/\r?\n/);

    lines1.forEach(line1 => {

        if(line1.indexOf("----")!=-1){
            info1.push(line1);
        }

    });

    //read function pre-loaded list
    
    var data2 = fs.readFileSync("log/"+file_name+".log", 'utf-8');
    var lines2 = data2.split(/\r?\n/);
    // console.log(data2);
    lines2.forEach(line2 => {
        // console.log("------------"+line2);

        if((line2.indexOf("=")!=-1)){
            // console.log("===="+line2);
            let tmp = line2.split("=");
            line2 = tmp[0]+"----"+tmp[1];
            info2.push(line2);
        }
    });

    info2 = Array.from(new Set(info2));
    // info2= readlogdata(file_name);

    // console.log(info2.length);
    //put log data to add into result/data

    // fWriteName = "result/"+file_name+".txt";
    // var fWrite = fs.createWriteStream(fWriteName,{"flags":'a'});
    // info2.forEach(each_fun =>{
    //     fWrite.write(each_fun+"\n");
    // });



    console.log(info1.length);
    console.log(info2.length);


    info_final = info_final.concat(info1);
    info_final = info_final.concat(info2);
    info_final = info_final.concat(whitelist);
    
    info_final = Array.from(new Set(info_final));

    console.log(info_final.length);

    fWriteName = "result/"+file_name+"-final.txt";
    var fWrite = fs.createWriteStream(fWriteName);
    info_final.forEach(each_fun =>{
        fWrite.write(each_fun+"\n");
    });
    



    console.log("write complete");
    // console.log("result/"+file_name+".txt")
    // return info_final;
}




module.exports = resultPro;


