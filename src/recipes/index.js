fs = require("fs");
files = fs.readdirSync(__dirname).filter(function (filename) {
  return filename.indexOf("_") !== 0 && filename.indexOf(".md") >= 0 &&
    filename != "index.md";
});

recipes = [];
files.forEach(function (file) {
  var title = file;
  while (title.indexOf("-") >= 0)
    title = title.replace("-", " ");
  title = title.replace(".md", " ");

  var words = title.split(" ");
  for (var i = 0; i < words.length; i++)
    words[i] = words[i].charAt(0).toUpperCase() + words[i].slice(1);

  var recipe = {};
  recipe.title = words.join(' ');
  recipe.href = file.replace(".md", "");

  recipes.push(recipe);
});

module.exports.recipes = recipes;
