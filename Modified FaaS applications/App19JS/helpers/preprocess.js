const sharp = require('sharp')

const getImageType = require('./get-image-type')

const preprocces = async (image, size, q, t) => {
  const sharpType = getImageType(t) || getImageType('webp')

  const processed = await sharp(Buffer.from(image.buffer))
    .resize({
      width: size.w,
      height: size.h,
      fit: 'cover'
    })
    .rotate()
    [sharpType.extension]({ q }) // eslint-disable-line
    .toBuffer()

  return {
    image: processed,
    contentType: sharpType.contentType
  }
}

module.exports = preprocces