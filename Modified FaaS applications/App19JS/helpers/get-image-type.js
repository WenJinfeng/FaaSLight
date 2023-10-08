const types = require('./types')

const getImageType = (t) => types.find(item => item.extension === t)

module.exports = getImageType
