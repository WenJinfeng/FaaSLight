const aws = require('aws-sdk')
// const { BUCKET } = require('./env')

var config = new aws.Config({
  accessKeyId: 'AKIAUMD2BUWB7NHFUXE3', secretAccessKey: '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', region: 'us-west-1'
});

config.update({
  'bucketname': "bucketwendycyn",
  
})

// Set AWS to use native promises
aws.config.setPromisesDependency(null)

const s3 = new aws.S3()

const getS3 = async (fileName) => {
  const params = {
    Bucket: "bucketwendycyn",
    Key: fileName
  }
  // console.log(params);
  try {
    // Check if Key exist
    await s3.headObject({
      Bucket: params.Bucket,
      Key: params.Key
    }).promise()

    // console.log('hhhhhh');

    // Get image from S3
    const data = await s3.getObject({
      Bucket: params.Bucket,
      Key: params.Key
    }).promise()

    // console.log(data);

    const contentType = data.ContentType
    const image = data.Body

    return { image, contentType }
  } catch (err) {
    if (err.statusCode === 404) {
      throw new Error(404, 'Not Found')
    } else {
      throw err
    }
  }
}

module.exports = {
  getS3
}
