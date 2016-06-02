angular.module('myApp.services', []).service('PG', function() {
    "use strict";
    var self = this,
        GroupRecord = {},
        SingleRecord = {};
    //key: session_id
    self.MsgRecord = {
            "group": {},
            "single": {}
        }
        //所有项目
    self.AllProject = [];
    //浅谈中的项目
    self.interviews = [];

    self.receive_session_record = 531;
    self.msg_record = 777;
    self.receive_msg_record = 778;
    self.create_group = 1029;
    self.create_group_ret = 1030;
    self.group_list = 1025;
    self.group_list_rep = 1028;
    self.return_upload_status = 12138;
    self.session_id;
    self.session_list;
    self.isfirst = true;
    self.profile;
    self.userinfo = {};

    self.setRecord = function(msg_type, key, val) {
        if (!key || !val) {
            return new Error("key and val is not undefined!");
        }
        // Single
        var group = self.MsgRecord["group"],
            single = self.MsgRecord["single"];
        if (msg_type == 17 || msg_type == 18) {
            //群组消息
            if (!group[key]) {
                group[key] = [];
            }
            group[key].push(val);
        } else if (msg_type == 1 || msg_type == 2) {
            //个人消息
            if (!single[key]) {
                single[key] = [];
            }
            single[key].push(val);
        }
    }

    self.getRecord = function(type, key) {
        if (type !== "group" || type !== "single") {
            return new Error("Invalid type value");
        }
        return self.MsgRecord[type][key];
    }

    self.GetType = function(session_type) {
        var type = "";
        if (session_type == 1) {
            type = "single";
        } else if (session_type == 2) {
            type = "group";
        }
        return type;
    }

    self.GetTypeForMsgType = function(msg_type) {
        var type = "";
        if (msg_type == 1 || msg_type == 2) {
            type = "single";
        } else if (msg_type == 17 || msg_type == 18) {
            type = "group";
        }
        return type;
    }

    self.GetTypeForSessionType = function(session_type) {
        if (session_type == 1) {
            return "single";
        } else if (session_type == 2) {
            return "group";
        } else {
            return "";
        }
    }

    self.SetGroup = function(group_name, group_info) {
        if (typeof group_info != "object") {
            return new Error("group_info must be obj");
        }
        GroupRecord[group_name] = group_info;
    }

    self.IsGroups = function(group_name) {
        if (GroupRecord[group_name]) {
            return true;
        }
        return false;
    }

    self.GetGroups = function(group_name) {
        return GroupRecord[group_name];
    }

    self.AllGroups = function() {
        return GroupRecord;
    }

    self.SetSingle = function(single_name, single_info) {
        if (typeof single_info != "object") {
            return new Error("single_info must be obj");
        }
        SingleRecord[single_name] = single_info;
    }

    self.GetSingle = function(single_name) {
        return SingleRecord[single_name];
    }

    return self;
}).service('Context', function($http, PG, cookie) {
    var self = this,
        uri = 'http://cloudwork.yunzujia.net',
        next = encodeURIComponent(uri + "/messages"),
        signin = '/signin?next=' + next,
        offer_url = uri + '/clients/proposal/';
    self.api = function(m, u, func) {
        var method,
            url = uri + u,
            res;
        if (m === "GET") {
            method = m;
        } else if (m === "POST") {
            method = m;
        }

        $http({
            method: method,
            url: url
        }).success(function(response, status, headers, config) {
            if (response.error_code === 80001) {
                window.location.href = signin;
            }

            if (response.error_code === 0) {
                func(response);
            }
        }).error(function(e) {
            console.error(e);
        });
    }

    self.get = function(u, func) {
        return self.api("GET", u, func);
    }

    self.post = function(u, func) {
        return self.api("POST", u, func);
    }

    self.OfferUrl = function(offerid) {
        return new Array(offer_url,offerid,"/offer").join("");
    }

    return self;
});
