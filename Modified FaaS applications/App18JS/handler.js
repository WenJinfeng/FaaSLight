var init_st = (new Date()).valueOf();
const request = require('request');
const cheerio = require('cheerio');
const moment = require('moment-timezone');

const menuUrl = "http://marketcreationscafe.com/lunch/cleveland-oh/"
var init_ed = (new Date()).valueOf();

//module.exports.menu = (event, context, callback) => {
module.exports.menu = (req, res) => {
  var fun_st=(new Date()).valueOf();

  request(menuUrl, function (error, response, html) {
    if (!error && response.statusCode == 200) {
      var data = getData(html);

      var message;
      var date = data.shift();
      if (isToday(date)) {
        message = data.join("\n\n");
      } else {
        message = "Hang tight, it looks like today's menu hasn't been posted yet.";
      }
      // console.log(message);
    //   console.log(createResponse(message, req, 200));
    var fun_ed = (new Date()).valueOf();
    res.send(JSON.stringify({
        log:{"info":',InitStart:'+init_st+',' + 'InitEnd:'+init_ed+',' + 'functionStart:'+fun_st+','+ 'functionEnd:'+fun_ed+','}
  }))
    } else {
        var fun_ed = (new Date()).valueOf();
    res.send(JSON.stringify({
        log:{"info":',InitStart:'+init_st+',' + 'InitEnd:'+init_ed+',' + 'functionStart:'+fun_st+','+ 'functionEnd:'+fun_ed+','}
  }))
    //   console.log(createResponse("Whoops. I couldn't retrieve the menu.", req, 500));
      // callback(null, createResponse("Whoops. I couldn't retrieve the menu.", event, 500));
    }
//     var fun_ed = (new Date()).valueOf();
//     res.send(JSON.stringify({
//         log:{"info":',InitStart:'+init_st+',' + 'InitEnd:'+init_ed+',' + 'functionStart:'+fun_st+','+ 'functionEnd:'+fun_ed+','}
//   }))
    // console.log(",functioStart:" + tm_st+ ",");
  }
  );
  

  function getData(html) {
    var data = [];

    var $ = cheerio.load(html, { normalizeWhitespace: true });
    $("div[id='content'] article div").children().each(function(i, element) {
      var item = $(this).text();
      if (item.trim()) {
        data.push(item);
      }
    });

    return data;
  }

  function isToday(date) {
    var today = moment().tz("America/New_York").format('MM/DD/YY');

    return (date === today);
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


// menu("", "", "");