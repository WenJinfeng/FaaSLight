

const fs = require('fs')
const path = require('path')

//delete file
function deleteFiles(dir) {
    var delFiles = ["test.js"];
    var delDir = [".bin", ".git", ".github","examples", ".idea", "test", "example","tests"];
    var popFiles = ["md","yml"];

    fs.readdir(dir, function (err, files) {
        files.forEach(function (filename) {
            var src = path.join(dir, filename)
            fs.stat(src, function (err, st) {
                if (err) {
                    throw err
                }
            // whether is file
                if (st.isFile()) {
                    // console.log("file is "+ filename)
                
                    if (delFiles.includes(filename)) {
                        fs.unlink(src, err => {
                            if (err) throw err
                            console.log('delete file ' + src)
                        })
                    }
                    tmp  = filename;
                    // tmp = tmp.split('.').pop()
                    // console.log(tmp)
                    if(popFiles.includes(tmp.split('.').pop())){
                        fs.unlink(src, err => {
                            if (err) throw err
                            console.log('delete pop name file ' + src)
                        })

                    }
                    // if(){

                    // }
                } else {// rescure direction
                    
                    if(delDir.includes(filename)){
                        deleteDirAll(src);
                    }else{
                        deleteFiles(src)
                    }
                }
            })
        })
    })
}

//delete directory
function deleteDirAll(DirName){
    var files = [];
    if(fs.existsSync(DirName)){
        files=fs.readdirSync(DirName);
        files.forEach(function(file, index){
            var curPath = DirName+"/"+file;
            if(fs.statSync(curPath).isDirectory()){
                deleteDirAll(curPath);
            }else{
                fs.unlinkSync(curPath);
            }
        });
        fs.rmdirSync(DirName);
        console.log('delete directory' + DirName)
    }
}

module.exports = deleteFiles;
