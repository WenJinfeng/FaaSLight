var init_st = (new Date()).valueOf();
var request = require('request'); // for fetching the feed

var RSS = require('rss');
var init_ed = (new Date()).valueOf();
// module.exports.
module.exports.microcosm = (req, res) => {


    var fun_st=(new Date()).valueOf();
    req={"query":{"site": "https://espruino.microco.sm", "microcosm": "557"}}

    /* lets create an rss feed */
    var feed = new RSS({
        title: 'Microcosm2RSS',
        description: 'Return latest posts in a Microcosm Forum as an RSS feed',
        feed_url: 'http://example.com/rss.xml',
        site_url: 'http://example.com',
        image_url: 'http://example.com/icon.png',
        docs: 'http://example.com/rss/docs.html',
        managingEditor: 'conor@conoroneill.com',
        webMaster: 'conor@conoroneill.com',
        copyright: '2017 Conor ONeill',
        language: 'en',
        pubDate: 'Nov 18, 2017 08:00:00 GMT',
        ttl: '60',
    });

    console.log("ddd");

    // e.g.  https://espruino.microco.sm/api/v1/microcosms/557

    siteURL = req.query.site;
    // siteURL = "https://espruino.microco.sm"
    microcosmID = req.query.microcosm;
    // microcosmID = "557"
    console.log(siteURL);
    console.log(microcosmID);

    request(siteURL + "/api/v1/microcosms/" + microcosmID, { json: true }, function (error, response, body) {
        console.log('error:', error);

        for (var i = 0; i < body.data.items.items.length; i++) {
            var topic = body.data.items.items[i];
            feed.item({
                title: topic.item.title,
                description: topic.item.title,
                url: siteURL + "/conversations/" + topic.item.id, // link to the item
                author: topic.item.meta.createdBy.profileName + "@example.com", // optional - defaults to feed author property
                date: topic.item.meta.created // any format that js Date can parse.
            });

        }

        feed.title = body.data.title;
        feed.description = body.data.description;
        feed.site_url = req.query.site + "/" + req.query.microcosm;
        // feed.site_url = "https://espruino.microco.sm" + "/" + "557";
        feed.image_url = body.data.logoUrl;

        var xml = feed.xml();
        
        
        // console.log("succeed")
        // context.succeed(xml);

    });
    var fun_ed = (new Date()).valueOf();
    res.send(JSON.stringify({
        log:{"info":',InitStart:'+init_st+',' + 'InitEnd:'+init_ed+',' + 'functionStart:'+fun_st+','+ 'functionEnd:'+fun_ed+','}
  }))
    // console.log(",functioStart:" + tm_st+ ",")
};

// event1 ={"query":{"site": "https://espruino.microco.sm", "microcosm": "557"}}
// microcosm(event1,"","")