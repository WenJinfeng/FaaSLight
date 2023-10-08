module.exports = `
<html>
  <head>
    <title>Show Me A Dog</title>
    <style>{{{css}}}</style>
  </head>
  <body>
    <h1>Show Me A...</h1>
    <div>
      <ul class="breed-list">
        {{#each breeds}}
          <li class="breed-list-item"><a href="{{this}}">{{this}}</a></li>
        {{/each}}
      </ul>
    </div>
    <div class="about">
      <div>Coded by <a href="http://mattholland.info/">Matt Holland</a></div>
      <div>Powered by <a href="https://dog.ceo/">Dog CEO's</a> <a href="https://dog.ceo/dog-api/">Dog API</a> and the <a href="http://vision.stanford.edu/aditya86/ImageNetDogs/">Stanford Dogs Dataset</a></div>
      <div><a href="https://github.com/hollandmatt/show-me-a-dog">Source Code</a></div>
    </div>
  </body>
</html>
`;
