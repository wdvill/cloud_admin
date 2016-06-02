Vue.config.delimiters = ['{[', ']}'];

function UserCategory() {
  this.con = null;
  this.skills = [];
  $.i18n().then(function(data){
    window['CODE'] = data.CODE;
    window['COMMONS'] = data.COMMONS;
  });
}

UserCategory.prototype.get_category = function(){
  var con = this.con;
  var that = this;
  $.ajax({
    type: "post",
    url: "/api/category",
    cache: false,
    dataType: "json",
    data: {
      t: "all",
      category_id: 0,
      _xsrf: Cookies.get("_xsrf")
    },
    error: function (xhr, textStatus) {
    },
    success: function (json) {
      if(json.error_code == 0){
        var arr = {};
        for(var i=0; i<json.categorys.length; i++){
          json.categorys[i].name = COMMONS[json.categorys[i].name];
          var cid = json.categorys[i].category_id;
          var cname = json.categorys[i].name;
          if(json.categorys[i].pid == 0){
            arr[json.categorys[i].category_id] = {"name":cname, "category_id":cid, "children":[], "src":"/static/images/select-icon"+cid+".png"}
          }else{
            arr[json.categorys[i].pid]["children"].push({"name":cname, "category_id":cid});
          }
        }
        con.categorys = arr;
      }else{
        alert(CODE[json.error_code]);
      }
    }
  });
};

UserCategory.prototype.user_category = function(){
  var con = this.con;
  var that = this;
  $.ajax({
    type: "get",
    url: "/api/user/category",
    cache: false,
    dataType: "json",
    data: {
      _xsrf: Cookies.get("_xsrf")
    },
    error: function (xhr, textStatus) {
    },
    success: function (json) {
      if(json.error_code == 0){
        for(var i=0; i<json.categorys.length; i++){
          //json.categorys[i].name = COMMONS[json.categorys[i].name];
          $("#cate-" + json.categorys[i].category_id).addClass("active");
          that.skills.push(json.categorys[i].category_id);
        }
      }else{
        alert(CODE[json.error_code]);
      }
    }
  });
};

UserCategory.prototype.user_category_update = function(){
  var that = this;
  if(that.skills.length == 0){
    alert("请至少选择一个类别");
    return;
  }
  $.ajax({
    type: "post",
    url: "/api/user/category",
    cache: false,
    dataType: "json",
    data: {
      category: that.skills.join(),
      _xsrf: Cookies.get("_xsrf")
    },
    error: function (xhr, textStatus) {
    },
    success: function (json) {
      if(json.error_code == 0){
        location.href="/users/profile/step/2";
      }else{
        alert(CODE[json.error_code]);
      }
    }
  });
};

UserCategory.prototype.toggle_skill = function(cate_id) {
  var dom = $("#cate-" + cate_id);
  var i = this.skills.indexOf(cate_id);
  if(dom.hasClass("active")){
    dom.removeClass("active");
    if(i >= 0){
      this.skills.splice(i, 1);
    }
  }else{
    dom.addClass("active");
    if(i < 0){
      this.skills.push(cate_id);
    }
  }
};

var uc = new UserCategory();
var m = new Vue({
  el: "#layout",
  data: {
    categorys: "",
    cur_cate: "",
    isParent: true
  },
  created: function() {
    uc.con = this;
    uc.get_category();
    uc.user_category();
  },
  methods: {
    select_parent: function(cid) {
      this.isParent = false;
      this.cur_cate = cid;
    },
    toggle_skill: function(value, evt) {
      uc.toggle_skill(value);
    },
    reselect: function() {
      this.isParent = true;
      this.cur_cate = "";
    },
    update_user_category: function() {
      uc.user_category_update();
    }
  }
});
