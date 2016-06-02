var ExtractTextPlugin = require("extract-text-webpack-plugin");
var path = require('path');
var glob = require('glob');

//遍历入口文件
function getEntry(globPath) {
  var files = glob.sync(globPath);
  var entries = {},
    entry, dirname, basename, pathname, extname;

  for (var i = 0; i < files.length; i++) {
    entry = files[i];
    dirname = path.dirname(entry);
    extname = path.extname(entry);
    basename = path.basename(entry, extname);
    entries[basename] = './' + entry;
  }
  return entries;
}

module.exports = {
  entry: getEntry('{src/*.js,src/views/**/*.js}'),
  output: {
    path: '../static/production',
    publicPath: '/static/production/',
    filename: '[name].min.js'
  },
  devtool: 'source-map',
  externals: {
    "jquery": "jQuery",
    "vue": "Vue",
  },
  watch: './src',
  module: {
    loaders: [{
      test: /\.vue$/,
      loader: 'vue'
    }, {
      test: /\.js$/,
      loader: 'babel!eslint',
      // make sure to exclude 3rd party code in node_modules
      exclude: /node_modules/
    }, {
      // edit this for additional asset file types
      test: /\.(png|jpg|gif)$/,
      loader: 'url',
      query: {
        // inline files smaller then 10kb as base64 dataURL
        limit: 100000,
        // fallback to file-loader with this naming scheme
        name: 'images/[name].[ext]?[hash]'
      }
    }, {
      test: /\.css$/,
      loaders: ['style', 'css']
    }, {
      test: /\.scss$/,
      loaders: ['style', 'css', 'sass']
    }]
  },
  // vue-loader config:
  // lint all JavaScript inside *.vue files with ESLint
  // make sure to adjust your .eslintrc
  vue: {
    loaders: {
      js: 'babel!eslint',
      scss: 'style!css!sass'
    }
  }
}