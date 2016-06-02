angular.module('myApp.filters', []).filter('message', function($sce) {
        return function(data) {
            var info = data;
            var res = info.match(/\[[a-zA-Z0-9\u4e00-\u9fa5]+\]/ig);
            if (res != null) {
                for (var i = 0; i < res.length; i++) {
                    var src = $.emojiarea.path + '/' + $.emojiarea.icons[res[i]];
                    var img = '<img class="emoji" ng-src="' + src + '" src="' + src + '">';
                    info = info.replace(res[i], img);
                }
            }

            var d = info.match(/\&\$\#\@\~\^\@\[\{:(.*?):\}\]\&\$\~\@\#\@/ig);
            if (d != null) {
                var obj = JSON.parse(info),
                    imgUrl = d[0].replace(/(\&\$\#\@\~\^\@\[\{:)|(:\}\]\&\$\~\@\#\@)|(\\)/ig, ""),
                    width = 256;
                if (obj.width > width) {
                    info = '<img showImg style="width:' + width + 'px;height:auto;" class="msg-img" src="' + imgUrl + '" alt="img">';
                } else {
                    info = '<img showImg style="width:' + obj.width + 'px;height:auto" class="msg-img" src="' + imgUrl + '" alt="img">';
                }
            }

            return $sce.trustAsHtml(info);
        }
    }).filter('session_filter', function() {
        return function(data) {
            var info = data;
            if (!info) {
                return "";
            }
            var d = info.match(/\&\$\#\@\~\^\@\[\{:(.*?):\}\]\&\$\~\@\#\@/ig);
            if (d != null) {
                info = "[图片]"
            }
            return info;
        }
    }).filter('filter_img', function(avatar_split) {
        return function(avatar) {
            return avatar_split.split(avatar);
        }
    })
    /************************************
    日期格式化
    *************************************/
    .filter('dateAge', function() {
        return function(i) {
            var date1 = new Date();
            var date2 = new Date(i * 1000);
            var date3 = date1.getTime() - date2.getTime();
            var days = Math.floor(date3 / (24 * 3600 * 1000));
            if (days == 0) {
                return date2.getHours() + ':' + date2.getMinutes();
            }
            if (days < 7) {
                return days + '天前';
            } else {
                return (date2.getMonth() + 1) + '月' + date2.getDate() + '日';
            }
        };
    })

;
