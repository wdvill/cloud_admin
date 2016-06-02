'use strict';
angular.module('myApp.directive', []).directive('init', function(
    $rootScope,
    websocket,
    $http,
    PG,
    $location
) {
    return {
        restrict: 'AE',
        link: function(scope, element, attr) {
            console.log("正在初始化。。。。。。");
            var win_height = $(window).height() - 50;
            $('.left').css('height', win_height);
            $('.tool-bar').css('height', win_height);
            $('.right').css('height', win_height);
            $('#msg-input').emojiarea({
                button: '.emoji-btn'
            });
            $('#add').dropdown();
            $('#creategroup').dropdown();
        }
    }
}).directive('scroller', function(PG, websocket) {
    return {
        restrict: 'AE',
        link: function(scope, element, attr) {
            $("#right-scrollbar").bind("scrolltop", function(e) {
                console.log(scope.dialog_info);
                var dialog_info = scope.dialog_info,
                    record = PG.MsgRecord[PG.GetTypeForSessionType(dialog_info.session_type)][dialog_info.mid],
                    last = record[0].msgid;

                console.log(record);
                if (record[0].msgid == 1) {
                    return
                }
                if (record) {

                    var msg = {
                        "user_id": PG.profile.imid,
                        "session_id": dialog_info.mid,
                        "msg_cnt": 5,
                        "msg_id_begin": record[0].msgid - 1,
                        "session_type": dialog_info.session_type
                    }
                }

                $("#right-scrollbar").nanoScroller({
                    scrollTo: $("#msg" + record[4].msgid)
                });
                websocket.send(PG.msg_record, msg);
            });
        }
    }
}).directive('dialog', function($rootScope, PG) {
    return {
        restrict: 'AE',
        link: function(scope, element, attr) {
            scope.Select = function(dialog) {
                $rootScope.$broadcast('history', dialog);
                PG.session_id = dialog.mid;
                $(element).parent().addClass("active-panel").siblings("li").removeClass("active-panel");
            }
            $rootScope.$on('CallSelect', function(e, dialog) {
                scope.Select(dialog);
            });
        }
    }
}).directive('chatrecord', function() {
    return {
        restrict: 'AE',
        templateUrl: templateUrl('chatrecord'),
        replace: false,
        link: function(scope, element, attr) {
            $('#history').bind('click', function() {
                $('#chatrecord').modal('show');
            })
        }
    }
}).directive('chatroom', function() {
    return {
        restrict: 'AE',
        templateUrl: templateUrl('chatroom'),
        replace: true,
        link: function(scope, element, attr) {
            $("#create_chatroom").click(function() {
                $('#chatroom').modal('show');
            });
        }
    }
}).directive('showImg', function() {
    return {
        restrict: 'AE',
        replace: false,
        link: function(scope, element, attr) {}
    }
}).directive('group', function() {
    return {
        restrict: 'AE',
        replace: false,
        templateUrl: templateUrl('group'),
        link: function(scope, element, attr) {

        }
    }
}).directive('contacts', function() {
    return {
        restrict: 'AE',
        replace: false,
        templateUrl: templateUrl('contacts'),
        link: function(scope, element, attr) {

        }
    }
}).directive('session', function() {
    return {
        restrict: 'AE',
        replace: false,
        templateUrl: templateUrl('session'),
        link: function(scope, element, attr) {

        }
    }
}).directive('sendmsg', function(PG, websocket, $rootScope) {
    return {
        restrict: 'AE',
        replace: false,
        link: function(scope, element, attr) {
            var dialog, msg = {};

            $(element).on('keydown', function(event) {
                if (event.keyCode == 13) {
                    msg.msg_data = scope.textarea;
                    SendMsg(scope.dialog_info, msg);
                }
            });

            scope.FileChanged = function() {
                var file = document.getElementById("file-input").files[0];
                if (!/image\/\w+/.test(file.type)) {
                    // alert("文件必须为图片！");
                    return false;
                }
                var reader = new FileReader();
                reader.readAsDataURL(file);
                reader.onload = function(e) {
                    console.log(e);
                    var img = new Image();
                    img.src = e.target.result;
                    if (img.complete) {
                        $(".emoji-wysiwyg-editor").append(CreateImage(img));
                    } else {
                        img.onload = function() {
                            $(".emoji-wysiwyg-editor").append(CreateImage(img));
                        }
                    }
                }
            }

            function CreateImage(img) {
                if (img.width > 260) {
                    return '<img style="width:260px;height:auto;"  src="' + img.src + '" alt=""/>';
                } else {
                    return '<img style="width:' + img.width + 'px;height:' + img.height + 'px;"  src="' + img.src + '" alt=""/>';
                }
            }

            scope.send = function(d) {
                dialog = d;
                var file = document.getElementById("file-input").files[0];
                if (file) {
                    SendImg(file);
                } else {
                    msg.msg_data = scope.textarea;
                    SendMsg(dialog, msg);
                }
            }

            function SendImg(file) {
                var reader = new FileReader();
                reader.readAsArrayBuffer(file)
                reader.onload = function(evt) {
                    var data = new Uint8Array(evt.target.result);
                    console.log(data);
                    websocket.sendByBlob(data);
                }
            }

            function SendMsg(dialog, msg) {

                //发送单点消息
                msg.from_user_id = PG.profile.imid;
                msg.msg_id = dialog.msgid + 1;
                msg.create_time = new Date().getTime();

                if (dialog.session_type == 1) {
                    //个人会话
                    msg.to_session_id = dialog.mid;
                    msg.msg_type = dialog.session_type;
                    websocket.send(769, msg);
                } else if (dialog.session_type == 2) {
                    //群组会话
                    msg.msg_type = 17;
                    msg.to_session_id = dialog.mid;
                    websocket.send(769, msg);
                }
                $(".emoji-wysiwyg-editor").empty();
            }

            //上传图片后返回的url
            $rootScope.$on(12138, function(e, msg) {
                var image = new Image();
                image.src = msg.body.url;
                if (image.complete) {
                    HandleSend(image, msg);
                } else {
                    image.onload = function() {
                        HandleSend(image, msg);
                    };
                }
            });

            function HandleSend(image, msg) {
                msg.msg_data = ImgMsgJoin(image.width, image.height, msg.body.url);
                SendMsg(dialog, msg);
                ClearUpload("file-input");
            }

            function ClearUpload(id) {
                var file = document.getElementById(id);
                if (file.outerHTML) {
                    file.outerHTML = file.outerHTML;
                } else {
                    file.value = "";
                }
            }

            function ImgMsgJoin(width, height, url) {
                return new Array('{"width": ',
                    width,
                    ',"height": ',
                    height,
                    ',"url": "&$#@~^@[{:',
                    url,
                    ':}]&$~@#@"}').join("");
            }
        }
    }
}).directive('allproject', function(PG) {
    return {
        restrict: 'AE',
        replace: false,
        templateUrl: templateUrl('all_project'),
        link: function(scope, element, attr) {

        }
    }
}).directive('pop', function() {
    return {
        restrict: 'AE',
        replace: false,
        templateUrl: templateUrl('pop'),
        link: function(scope, element, attr) {

        }
    }
}).directive('navbar', function() {
    return {
        restrict: 'AE',
        replace: false,
        templateUrl: templateUrl('nav'),
        link: function(scope, element, attr) {

        }
    }
});
