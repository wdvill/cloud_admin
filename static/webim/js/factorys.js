angular.module('myApp.factorys', []).factory('cookie', function() {

    function setCookie(name, value) {
        var Days = 30;
        var exp = new Date();
        exp.setTime(exp.getTime() + Days * 24 * 60 * 60 * 1000);
        document.cookie = name + "=" + escape(value) + ";expires=" + exp.toGMTString();
    }

    function getCookie(name) {
        var arr, reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)");
        if (arr = document.cookie.match(reg)) return unescape(arr[2]);
        else return null;
    }

    function delCookie(name) {
        var exp = new Date();
        exp.setTime(exp.getTime() - 1);
        var cval = getCookie(name);
        if (cval != null) document.cookie = name + "=" + cval + ";expires=" + exp.toGMTString();
    }

    return {
        GetCookie: getCookie,
        SetCookie: setCookie,
        DelCookie: delCookie
    }
}).factory('avatar_split', function($sce) {
    function split(avatar) {
        var avatars = avatar.split(',');
        var ava_len = avatars.length;
        if (ava_len == 1) {
            avatar = '<div>';
            avatar += '<img class="im_dialog_photo" src="' + avatars[0] + '">';
        } else {
            avatar = '<div class="avatar">';
            for (var i = 0; i < ava_len; i++) {
                if (i < 4) {
                    if (ava_len == 2) {
                        avatar += '<img class="im_dialog_photo two" src="' + avatars[i] + '">';
                        continue
                    } else if (ava_len == 3) {
                        avatar += '<img class="im_dialog_photo three" src="' + avatars[i] + '">';
                        continue
                    } else {
                        avatar += '<img class="im_dialog_photo four" src="' + avatars[i] + '">';
                        continue
                    }
                } else {
                    break;
                }
            }
        }
        avatar += '</div>';
        return $sce.trustAsHtml(avatar);
    }
    return {
        split: split
    }
});
