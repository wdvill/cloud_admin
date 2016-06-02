'use strict';
angular.module('myApp.controllers', []).controller('InitController', function($scope, Context, PG, websocket, $rootScope, cookie) {

    $rootScope.reloadHistory = function(e) {
        var panel = e.target;
        var scrollTop, maxScroll, minScroll = 0;
        scrollTop = panel.scrollTop;
        maxScroll = panel.scrollHeight - panel.offsetHeight;
        if (scrollTop >= maxScroll) {
            // alert("滚动到底了");
            return false;
        }
        if (scrollTop <= 0) {
            // alert("滚动到顶了");
            return false;
        }
    };

    sysstatus(true, false, false);
    $scope.offer = false;
    $scope.offer_url = "";

    $scope.all_project = false;

    $scope.session = function() {
        sysstatus(true, false, false)
    }
    $scope.group = function() {
        sysstatus(false, true, false)
    }
    $scope.contacts = function() {
        sysstatus(false, false, true)
    }
    $scope.DbClickGroup = function(ginfo) {

        sysstatus(true, false, false)
        var offerid = 0;
        if (ginfo.offerid && ginfo.offerid > 0) {
            offerid = ginfo.offerid;
        }
        $rootScope.$broadcast('AddGroupToSession', {
            mid: ginfo.group_id,
            avatar: ginfo.group_avatar,
            name: ginfo.group_name,
            group_id: ginfo.group_id,
            session_type: ginfo.session_type,
            offerid: offerid
        });
    }

    $scope.DbClickContacts = function(contacts) {

        sysstatus(true, false, false)
        $rootScope.$broadcast('AddGroupToSession', {
            mid: contacts.id,
            avatar: contacts.avatar,
            name: contacts.name,
            session_type: contacts.session_type,
        });
    }

    Context.get("/api/user/profile", function(res) {
        PG.profile = res.profile;
        if (cookie.GetCookie("cuid") == "c") {
            PG.profile.avatar = res.profile.logo;
            PG.profile.name = res.profile.team_name;
        } else if (cookie.GetCookie("cuid") == "f") {}

        $scope.profile = PG.profile;
        console.log(PG.profile);
        sysinit(res.profile.imid)
    });

    function sysinit(imid) {
        //系统初始化
        var user_id = imid;
        setTimeout(function() {
            //获取群组列表
            websocket.GetGroupList();
            console.log("初始化成功。");
        }, 100);
    }

    function sysstatus(s, g, c) {
        $scope.session_record = s;
        $scope.group_record = g;
        $scope.contacts_record = c;
    }

}).controller('AppIMController', function($scope) {
    $scope.item_list = ['项目', '自由工作者', '报告', '消息'];
}).controller('AppIMDialogController', function($scope, PG, $rootScope, websocket, Context, cookie, avatar_split) {


    $rootScope.$on(PG.receive_session_record, function(e, dialog) {
        //接受会话记录
        var contact_session_list = dialog.body.contact_session_list || [],
            msgs = [],
            user_ids = "";;

        for (var i = 0; i < contact_session_list.length; i++) {
            user_ids += contact_session_list[i].session_id + ","
            if (contact_session_list[i].latest_msg_type == 18 || contact_session_list[i].latest_msg_type == 2) {
                contact_session_list[i].latest_msg_data = Base64.encode("[语音]")
            }
        };

        user_ids = user_ids.substring(0, user_ids.length - 1)

        var uri = "/api/friends/users?user_ids=" + user_ids;
        Context.get(uri, function(res) {
            if (res.msg == "ok" || res.error_code == 0) {
                msgs = Render(res, contact_session_list);
                $scope.IMDialog = msgs;
            }
            $scope.IMDialog = msgs;
        })
    });

    function Render(res, contact_session_list) {
        var users = res.users;
        var dia = [];
        for (var i = 0; i < contact_session_list.length; i++) {
            if (contact_session_list[i].latest_msg_data) {
                var info = Base64.decode(contact_session_list[i].latest_msg_data);
                var msg_row;

                if (contact_session_list[i].session_type == 1) {
                    for (var j = 0; j < users.length; j++) {
                        if (contact_session_list[i].session_id == users[j].id) {
                            msg_row = {
                                mid: contact_session_list[i].session_id,
                                session_type: contact_session_list[i].session_type,
                                msgContent: info,
                                msgid: contact_session_list[i].latest_msg_id,
                                time: contact_session_list[i].updated_time,
                                avatar: users[j].avatar,
                                name: users[j].name
                            }
                            if (msg_row) dia.push(msg_row);
                            contact_session_list[i].length = 0;
                        }
                    }
                }

                if (contact_session_list[i].session_type == 2) {
                    msg_row = {
                        mid: contact_session_list[i].session_id,
                        session_type: contact_session_list[i].session_type,
                        msgContent: info,
                        msgid: contact_session_list[i].latest_msg_id,
                        time: contact_session_list[i].updated_time,
                    }
                    var group_info = PG.GetGroups(contact_session_list[i].session_id)
                    if (group_info) {
                        msg_row.avatar = group_info.group_avatar;
                        msg_row.name = group_info.group_name;
                    } else {
                        msg_row.avatar = "";
                        msg_row.name = "";
                    }

                    contact_session_list[i].length = 0;
                    if (msg_row) {
                        msg_row.offerid = IsOffer(msg_row.mid);
                        dia.push(msg_row);
                    }
                }
            }
        }

        return dia;
    }

    function IsOffer(group_id) {
        var offerid = 0;
        console.log(PG.interviews);
        console.log(PG.AllProject);
        for (var i = 0; i < PG.interviews.length; i++) {
            if (group_id == PG.interviews[i].group_id) {
                offerid = PG.interviews[i].id;
                break;
            }
        }
        return offerid;
    }

    $rootScope.$on('AddGroupToSession', function(e, dialog) {
        var list = $scope.IMDialog || [];
        var ishave = false;
        for (var i = 0; i < list.length; i++) {
            if (!list[i]) {
                continue;
            }
            if (list[i].mid == dialog.mid) {
                ishave = true;
                break;
            }
        }
        if (ishave) {
            return;
        }
        //
        var dia = {
            avatar: dialog.avatar,
            mid: dialog.mid,
            msgid: "0",
            name: dialog.name,
            time: "",
            group_id: dialog.group_id || 0,
            session_type: dialog.session_type || 0,
            offerid: dialog.offerid || 0
        }
        list.splice(0, 0, dia);

        $scope.IMDialog = list;
    });



}).controller('HistoryMessagesController', function($scope, PG, $rootScope, websocket, Context, cookie) {
    $scope.session_id = "";
    $scope.textarea = "";
    $scope.chatrecordlist = [];

    $scope.CreateUserGroup = function() {
        $('#chatroom').modal('show');
    }

    $rootScope.$on('history', function(e, dialog) {
        //选择左侧按钮接执行的事件
        //获取消息数量
        $scope.dialog_info = dialog;
        var msg_cnt = 5;
        $scope.dialog_title = dialog.name;
        var type = PG.GetType(dialog.session_type);

        if (dialog.offerid && dialog.offerid > 0) {
            if (cookie.GetCookie("cuid") == "c") {
                $scope.offer = true;
                $scope.offer_url = Context.OfferUrl(dialog.offerid);
            }
        } else {
            $scope.offer = false;
        }

        if (PG.MsgRecord[type][dialog.mid]) {
            $scope.historys = PG.MsgRecord[type][dialog.mid];
        } else {
            var msg = {
                "user_id": PG.profile.imid, //发送方
                "session_id": dialog.mid, //接收方
                "msg_cnt": msg_cnt,
                "attach_data": "发送消息"
            }

            if (!dialog.msgid) {
                msg.msg_id_begin = 0
            }

            msg.msg_id_begin = dialog.msgid;

            if (dialog.session_type == 1) {
                msg.session_type = dialog.session_type;
            } else if (dialog.session_type == 2) {
                msg.session_type = dialog.session_type;
            }

            websocket.send(PG.msg_record, msg);
        }
    });

    //点击左侧会话后 从服务器接收到的消息
    $rootScope.$on(PG.receive_msg_record, function(e, msg) {
        //接受来自服务器的messages
        console.log(msg);

        var sid = msg.body.session_id;
        var type = PG.GetType(msg.body.session_type);
        var isfirstload = false;

        if (!PG.MsgRecord[type][sid]) {
            PG.MsgRecord[type][sid] = [];
            isfirstload = true;
        }
        var dia = [],
            msg_list = msg.body.msg_list,
            user_id = msg.body.user_id,
            ChatRecord = [];
        if (msg_list) {
            var attach_data = Base64.decode(msg.body.attach_data || "");
            for (var i = 0; i < msg_list.length; i++) {
                if (msg_list[i].msg_data) {
                    var belong = "other";
                    var data;
                    if (msg_list[i].msg_type == 2 || msg_list[i].msg_type == 18) {
                        data = '下载app接收语音消息';
                    } else {
                        data = Base64.decode(msg_list[i].msg_data);
                    }

                    var msg = {
                        message: data,
                        create_time: msg_list[i].create_time,
                        msgid: msg_list[i].msg_id,
                        uid: user_id,
                        sid: msg_list[i].from_session_id,
                    };
                    if (msg_list[i].from_session_id === PG.profile.imid) {
                        belong = "my";
                        msg.avatar = PG.profile.avatar;
                        msg.belong = belong;
                    } else {
                        var session_id = msg_list[i].from_session_id;
                        if (PG.GetSingle(session_id) && PG.GetSingle(session_id).id) {
                            msg.avatar = PG.GetSingle(session_id).avatar;
                        }
                        msg.belong = "other";
                    }
                    if (attach_data != "chatrecord") {
                        PG.setRecord(msg_list[i].msg_type, sid, msg);
                    } else {
                        ChatRecord.push(msg);
                    }
                }
            }

            if (attach_data == "chatrecord") {
                //聊天记录
                ChatRecord = ChatRecord.reverse();
                RenderChatRecord(ChatRecord);
                return;
            }

            if (PG.MsgRecord[type][sid]) {
                PG.MsgRecord[type][sid].sort(function(a, b) {
                    return a.msgid - b.msgid;
                });
            }
        } else {
            console.log('没有数据');
        }

        $scope.$apply(function() {
            $scope.historys = PG.MsgRecord[type][sid];
        });
        if (isfirstload) {
            setTimeout(function() {
                $("#right-scrollbar").nanoScroller({
                    scroll: 'bottom'
                });
            }, 200)
        }
    });

    //接受返回的消息
    $rootScope.$on(769, function(e, dialog) {
        //发送完消息ACK
        websocket.GetSessionRecord();
        var session_id;
        if (dialog.body.msg_data) {
            //服务器发过来的消息
            var data = dialog.body;
            data.msg_data = Base64.decode(data.msg_data);

            if (data.msg_type == 2 || data.msg_type == 18) {
                data.msg_data = '不支持的消息, 可在手机上查看';
            }

            var msg = {
                message: data.msg_data,
                belong: "other",
                create_time: data.create_time,
                msgid: data.msg_id,
                uid: data.to_session_id,
                sid: data.from_user_id,
            }

            if (PG.profile.imid == data.from_user_id) {
                //如果消息是由当前用户在其他设备上发的
                msg.belong = "my";
                msg.avatar = PG.profile.avatar;
                msg.name = PG.profile.name;
                session_id = data.to_session_id;
            } else {
                session_id = data.from_user_id;
                if (PG.GetSingle(session_id) && PG.GetSingle(session_id).id == session_id) {
                    msg.avatar = PG.GetSingle(session_id).avatar;
                }
            }

            // 根据消息类型将数据写入record中
            if (data.msg_type == 17 || data.msg_type == 18) {
                PG.setRecord(data.msg_type, data.to_session_id, msg)
            } else if (data.msg_type == 1 || data.msg_type == 2) {
                PG.setRecord(data.msg_type, session_id, msg)
                var type = Judge(dialog.body.msg_type)
                $scope.$apply(function() {
                    $scope.historys = PG.MsgRecord[type][session_id];
                });
            }

        } else {
            //自己发送的消息返回过来的ack
            session_id = dialog.body.session_id;
            var type = PG.GetType(dialog.body.session_type);
            if (!PG.MsgRecord[type][session_id]) {
                PG.MsgRecord[type][session_id] = [];
            }

            $scope.textarea = "";
            $scope.$apply(function() {
                $scope.historys = PG.MsgRecord[type][session_id];
            });
        }
    });

    function Judge(msg_type) {
        var type = "";
        if (msg_type == 1 || msg_type == 2) {
            type = "single";
        } else if (msg_type == 17 || msg_type == 18) {
            type = "group";
        }
        return type
    }

    function RenderChatRecord(dialog) {
        $scope.$apply(function() {
            $scope.chatrecordlist = dialog;
        });
    }

    $scope.chatrecord = function(dialog_info) {

        console.log(dialog_info);
        //发送单点消息
        var msg = {
            "user_id": PG.profile.imid,
            "session_id": dialog_info.mid,
            "msg_cnt": 100,
            "msg_id_begin": dialog_info.msgid,
            "session_type": dialog_info.session_type,
            "attach_data": "chatrecord"
        }
        websocket.send(777, msg)
    }

    $scope.doLoadHistory = function() {
        console.log('===');
    };

}).controller('CreateChatroom', function($scope, websocket, PG, $rootScope, Context) {
    Context.get("/api/friends", function(response) {
        if (response.friends) {
            var fri = response.friends;
            for (var i = 0; i < fri.length; i++) {
                fri[i].checked = false;
            }
            $scope.members = fri
        }
    });

    $scope.CreateGroup = function(id) {
        var members = [];
        var names = "";
        for (var i = 0; i < $scope.members.length; i++) {
            if ($scope.members[i].checked) {
                members.push($scope.members[i].id);
                names += $scope.members[i].name + "、";
            }
        }
        members.push(PG.profile.imid);
        if (members) {
            websocket.send(PG.create_group, {
                "user_id": PG.profile.imid,
                "group_type": 2,
                "group_name": names,
                "group_avatar": "",
                "member_id_list": members
            });
        }
    }

    $rootScope.$on(PG.create_group_ret, function(e, dialog) {});
}).controller('DialogRecordController', function($scope, Context, $rootScope, PG, websocket) {

    Context.get("/api/friends", function(response) {
        if (response.friends) {
            for (var i = 0; i < response.friends.length; i++) {
                response.friends[i].session_type = 1;
                PG.SetSingle(response.friends[i].id, response.friends[i]);
            }
            $scope.contacts_list = response.friends;
        }
    });

    // 初始化群组列表将需要的数据保存到缓存
    $rootScope.$on(1028, function(e, dialog) {
        var uri = "/api/friends/users?user_ids=",
            group_info_list = dialog.body.group_info_list,
            mems = "";
        Context.get("/api/proposal/im", function(response) {
            if (response.msg == "ok" && response.proposals) {
                var interview_info_list = [];
                PG.AllProject = response.proposals.all;
                PG.interviews = response.proposals.interview;

                if (group_info_list) {
                    for (var i = 0; i < group_info_list.length; i++) {
                        group_info_list[i].session_type = 2;
                        group_info_list[i].group_avatar = "";
                        group_info_list[i].interview = false;
                        group_info_list[i].offerid = 0;
                        mems += group_info_list[i].group_member_list.join(',') + ',';
                        var interview = response.proposals.interview;
                        for (var j = 0; j < interview.length; j++) {
                            if (group_info_list[i].group_id == interview[j].group_id) {
                                group_info_list[i].interview = true;
                                group_info_list[i].offerid = interview[j].id;
                                interview_info_list.push(group_info_list[i]);
                            }
                        }
                    }

                    var url = uri + mems;
                    $scope.interview_info_list = interview_info_list;
                    RenderGroup(url, dialog);
                } else {
                    GetSessionRecord();
                }
            }
        });
    });

    function RenderGroup(url, dialog) {
        Context.get(url, function(res) {
            var group_info_list = dialog.body.group_info_list,
                users = res.users;
            for (var i = 0; i < group_info_list.length; i++) {
                var avatar = "";
                //如果用户id所属群成员，那么就将用户头像逗号隔开拼接
                for (var j = 0; j < users.length; j++) {
                    if ($.inArray(users[j].id, group_info_list[i].group_member_list) > -1) {
                        group_info_list[i].group_avatar += users[j].avatar + ','
                    }
                }
                group_info_list[i].group_avatar = group_info_list[i].group_avatar.substr(0, group_info_list[i].group_avatar.length - 1)
                PG.SetGroup(group_info_list[i].group_id, group_info_list[i])
            }
            $scope.group_info_list = dialog.body.group_info_list;
            //获取会话记录
            GetSessionRecord();
        });
    }

    function GetSessionRecord() {
        websocket.GetSessionRecord();
        $("#loading").hide();
    }

}).controller('allproject', function($scope, PG) {
    $scope.AllProject = [];
    $("#allpro").on('click', function() {
        $scope.all_project = true;
        $scope.$apply(function() {
            $scope.AllProject = PG.AllProject;
        });
    });
});
