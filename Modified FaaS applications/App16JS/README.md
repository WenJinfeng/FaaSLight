# Microcosm2RSS

A Serverless Lambda function in Node.js to take a Microcosm "Forum" and present it as an RSS feed. Allows you to monitor specific Microcosms for new posts.

I wrote it to monitor the [News forum](http://forum.espruino.com/microcosms/557/) on https://forum.espruino.com inside Feedly.

Installation:

```bash
npm install -g serverless
git clone git@github.com:conoro/microcosm2rss.git
cd microcosm2rss
npm install
serverless deploy
```

Then subscribe in your RSS reader to a URL like:

```
https://your-URL-for-your-Serverless-function/dev/?site=https://espruino.microco.sm&microcosm=557
```

(Assumes you have your AWS config already setup)


LICENSE Apache-2.0



Copyright Conor O'Neill 2017, conor@conoroneill.com
