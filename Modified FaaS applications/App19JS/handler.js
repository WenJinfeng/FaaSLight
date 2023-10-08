var init_st = (new Date()).valueOf();
const fs = require('fs');
const preprocess = require('./helpers/preprocess')
const { getS3 } = require('./helpers/s3')

// async function handler(event, context, callback) {
var init_ed = (new Date()).valueOf();

module.exports.handler = async (req, res) => {
// async function handler(event, context, callback) {
  
  var fun_st=(new Date()).valueOf();
  
  req={queryStringParameters: {f:"1.jpeg",t:'jpeg'}};
  
  console.log(req)
  try {
    if (!req.queryStringParameters) throw new Error('Needs Query String Parameters')

    const f = req.queryStringParameters.f || ''
    const q = Math.abs(req.queryStringParameters.q) || 100
    const t = req.queryStringParameters.t || 'jepg'

    const size = {
      w: Math.abs(req.queryStringParameters.w) || null,
      h: Math.abs(req.queryStringParameters.h) || null
    }

    const file = await getS3(f)

    const processed = await preprocess(file.image, size, q, t)

    // console.log(processed)

    const buffer = Buffer.from(processed.image.buffer, 'base46')

    console.log(buffer)
    
  } catch (err) {
    console.error(err)
    // callback(null, err)
  }
  // console.log(",functioStart:" + tm_st+ ",");
  var fun_ed = (new Date()).valueOf();
  res.send(JSON.stringify({
        log:{"info":',InitStart:'+init_st+',' + 'InitEnd:'+init_ed+',' + 'functionStart:'+fun_st+','+ 'functionEnd:'+fun_ed+','}
  }))
}

// event1 = {queryStringParameters: {f:"./media/performance.png",t:'jpeg'}};
// event1 = {queryStringParameters: {f:"1.jpeg",t:'jpeg'}};
// handler(event1,"","")
// console.log(info)