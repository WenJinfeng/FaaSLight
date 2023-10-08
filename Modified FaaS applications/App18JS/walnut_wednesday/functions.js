'use strict';

const request = require('request');
const url = require('url');
const cheerio = require('cheerio');
const moment = require('moment-timezone');

const requestUrl = "http://www.downtowncleveland.com/events/walnut-wednesday"

module.exports.trucks = (event, context, callback) => {

  request(requestUrl, function (error, response, html) {
    if (!error && response.statusCode == 200) {
      var trucklistJpeg = getData(html);

      var message;
      if (validate(trucklistJpeg)) {
        message = trucklistJpeg;
      } else {
        message = "Hang tight, it looks like the truck list hasn't been posted yet.";
      }

      callback(null, createResponse(message, event, 200));
    } else {
      callback(null, createResponse("Whoops. I couldn't find any trunks :(.", event, 500));
    }
  });

  function getData(html) {
    var $ = cheerio.load(html);

    var imgSrc = $('img[src*="trucklist"]').first().attr('src');
    return imgSrc ? url.resolve(requestUrl, imgSrc) : null;
  }

  function validate(trucklist) {
    var today = moment().tz("America/New_York").format('MMMM-DD').toUpperCase();

		return trucklist.indexOf(today) !== -1;
  }

  function createResponse(message, event, code) {
    const response = {
          statusCode: code,
          body: JSON.stringify({
            message: message,
            input: event,
          }),
        };

    return response;
  }
};
