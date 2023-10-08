module.exports = `
<html>
  <head>
    <title>Show Me A Dog</title>
    <style>{{{css}}}</style>
  </head>
  <body>
    <h1>Here is your {{breed}}!</h1>
    <div><img src="{{image}}"></div>
    <div class="links">
      <div class="link"><a href="javascript:window.location.reload(false);">Another?</a></div>
      <div class="link"><a href=".">Change breed?</a></div>
    </div>
    <div class="about">
      <div>Coded by <a href="http://mattholland.info/">Matt Holland</a></div>
      <div>Powered by <a href="https://dog.ceo/">Dog CEO's</a> <a href="https://dog.ceo/dog-api/">Dog API</a> and the <a href="http://vision.stanford.edu/aditya86/ImageNetDogs/">Stanford Dogs Dataset</a></div>
      <div><a href="https://github.com/hollandmatt/show-me-a-dog">Source Code</a></div>
    </div>
  </body>
</html>
`;
