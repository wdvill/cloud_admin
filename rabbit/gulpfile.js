var gulp = require('gulp');
var gutil = require('gulp-util');
var browserSync = require('browser-sync').create();
var webpack = require('webpack');

var config = require('./config/webpack.prod.config.js');

/** 编译webpack
 * 编译webpack
 */
gulp.task('webpack', function(cb) {
  var wpConfig = Object.create(config);
  webpack(wpConfig, function(err, stats) {
    if (err) console.log(err);
    gutil.log("[webpack:build]", stats.toString({
      colors: true
    }));
    if (cb) {
      cb();
    }
  })
});

/** 启动服务
 * 启动服务
 */
gulp.task('server', ['webpack'], function() {
  browserSync.init({
    proxy: "localhost:8080"
  });

  //对static和template文件夹进行监听
  gulp.watch(["../static/*", "../static/**/*", "../templates/*", "../templates/**/*"]).on('change', browserSync.reload);
});

/** 启动服务
 * 启动服务
 */
gulp.task('watch', function() {
  browserSync.init({
    proxy: "localhost:8080"
  });

  //对static和template文件夹进行监听
  gulp.watch(["../static/*", "../static/**/*", "../templates/*", "../templates/**/*"]).on('change', browserSync.reload);
});

/** 默认启动服务
 * 默认启动服务
 */
gulp.task('default', ['server']);