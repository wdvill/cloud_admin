Vue.config.delimiters = ['{[', ']}'];

function Profile() {
  this.con = null;
  var that = this;
  $('#english').selectlist({
    zIndex: 10,
    onChange: function(){
      that.check_english();
    }
  });
  $('#language').selectlist({
    zIndex: 10,
    onChange: function(){
      that.check_language();
    }
  });
  $('#workload').selectlist({
    zIndex: 9,
    onChange: function(){
      that.check_workload();
    }
  });
  $.i18n();
}

Profile.prototype.check_english = function() {
  this.con.english_level = $("input[name='english']").val();
  validict['english'](this.con);
};

Profile.prototype.check_language = function() {
  var txt = $("input[name='language']").val();
};

Profile.prototype.check_workload = function() {
  this.con.workload = $("input[name='workload']").val();
  validict['workload'](this.con);
};

Profile.prototype.init_skills = function() {
  var arr = $("#ipt-skills").val().split(",");
  var arr1 = [];
  for(var i=0;i<arr.length;i++){
    arr1.push({value: arr[i], text:arr[i]});
  }

  $('#select-skills').selectize({
     maxItems: 10,
     plugins: ['remove_button'],
     options: opts,
     delimiter: ',',
     create: true,
  });
};

Profile.prototype.update_profile = function() {
  var flag = true;
  var con = this.con;
  var that = this;
  for(var x in validict){
    if(validict[x](con) == false){
      flag = false;
    }
  }
  if(!flag){
    return;
  }
  var obj = {};
  for(var i=0;i<con.other_languages.length;i++){
    obj[con.other_languages[i].name] = con.other_languages[i].level;
  }
  $.ajax({
    type: "post",
    url: "/api/user/profile",
    cache: false,
    dataType: "json",
    data: {
      title: con.title,
      intro: con.intro,
      workload: con.workload,
      english: con.english_level,
      email: con.email,
      skills: con.skills,
      other: JSON.stringify(obj),
      _xsrf: Cookies.get("_xsrf")
    },
    error: function (xhr, textStatus) {
    },
    success: function (json) {
      if(json.error_code != 0){
        con.remoteErr = CODE[json.error_code];
      }else{
        location.href="/users/profile/step/3";
      }
    }
  });
};

Profile.prototype.select_language = function(is_close) {
  var lang = $("input[name='language']").val();
  if(lang == "none"){
    alert("请选择一门语言");
    return;
  }
  var level_obj = $('input[name=language]:checked', '#modal-lang');
  var level = level_obj.val();
  var level_txt = level_obj.attr("data");
  if(!level){
    alert("请选择水平");
    return;
  }
  this.con.errLanguages = "";
  var a = this.con.other_languages;
  for(var i=0;i<a.length;i++){
    if(a[i].name == lang){
      if(a[i].level == level){
      }else{
        a[i].level = level;
        a[i].level_txt = level_txt;
      }
      if(is_close){
        $(".addlanguage").modal('hide');
      }
      return;
    }
  }
  var txt = $("#language .select-button").val();
  this.con.other_languages.push({"name":lang, "name_txt":txt, "level":level, "level_txt":level_txt});
  if(is_close){
    $(".addlanguage").modal('hide');
  }
};

Profile.prototype.edit_language = function(index) {
  var obj = this.con.other_languages[index];
  $("input[name=language][value='"+obj.level+"']").prop("checked",true);
  $("input[name='language']").val(obj.name);
  $("#language .select-button").val(obj.name_txt);
  $(".addlanguage").modal('show');
};

Profile.prototype.upload_avatar = function() {
  var con = this.con;
  if(!con.x || con.x == ""){
    alert("请选择图片");
    return;
  }
  var formData = new FormData();
  var f = $("#photo")[0].files[0];
  if(!f){
    alert("请选择图片");
    return;
  }
  formData.append('file', f);
  var params = "x=" + con.x + "&y=" + con.y + "&w=" + con.w + "&h=" + con.h;
  params += "&_xsrf=" + Cookies.get("_xsrf") + "&boundx=" + boundx + "&boundy=" + boundy;
  $.ajax({
    url: '/api/attachment?t=avatar&' + params,
    type: 'POST',
    cache: false,
    data: formData,
    processData: false,
    contentType: false,

    error: function (xhr, textStatus) {
    },
    success: function (json) {
      json = $.parseJSON(json);
      if(json.error_code>0){
        alert(CODE[json.error_code]);
        return;
      }
      $("#photo_view").attr("src", json.avatar);
      $("#btn-closeM").click();
    }
  });
};

var profile = new Profile();

var v = new Vue({
  el: "#body",
  data: {
    address: "",
    title: "",
    email: "",
    skills: "",
    english_level: "",
    other_languages: [],
    workload: "",
    intro: "",
    x: "",
    y: "",
    w: "",
    h: "",

    errAddress: "",
    errTitle: "",
    errEmail: "",
    errSkills: "",
    errEnglish: "",
    errIntro: "",
    errLanguages: "",
    errWorkload: ""
  },
  created: function() {
    profile.con = this;
    profile.init_skills();
  },
  methods: {
    check_language: function() {
    },
    edit_other_languages: function(obj) {
      profile.edit_language(obj);
    },
    delete_other_languages: function(obj) {
      this.other_languages.splice(obj, 1);
    },
    prev_category: function() {
      location.href="/users/profile/step/1";
    },
    save_go_on: function() {
      profile.update_profile();
    },
    validate: function(name) {
      validict[name](this);
    },
    save_language: function() {
      profile.select_language(true);
    },
    save_language_on: function() {
      profile.select_language(false);
    },
    upload_avatar: function() {
      profile.upload_avatar();
    }
  }
});

var validict = {
  "email": function(fr) {
    var reg_email = /^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$/;
    if(!reg_email.test(fr.email)){
      fr.errEmail = "邮箱错误";
      return false;
    }else{
      fr.errEmail = "";
    }
  },
  "title": function(fr) {
    if(fr.title == ""){
      fr.errTitle = "此字段不能为空";
      return false;
    }else if(fr.title.length > 100){
      fr.errTitle = "职称在30个字符以内";
      return false;
    }else{
      fr.errTitle = "";
    }
  },
  "english": function(fr) {
    if(fr.english_level == "none" || fr.english_level == ""){
      fr.errEnglish = "请选择英语水平";
      return false;
      alert("aaa");
    }else{
      fr.errEnglish = "";
    }
  },
  "intro": function(fr) {
    if(fr.intro == ""){
      fr.errIntro = "请填写个人简介";
      return false;
    }else{
      fr.errIntro = "";
    }
  },
  "other_languages": function(fr) {
    if(fr.other_languages.length > 0){
      fr.errLanguages = "";
    }else{
      fr.errLanguages = "请选择其他语言";
      return false;
    }
  },
  "workload": function(fr) {
    var num = /^\d*$/;
    if(fr.workload == ""){
      fr.errWorkload = "此字段不能为空";
      return false;
    }
    if(!num.test(fr.workload)){
      fr.errWorkload = "请选择您的工作时长";
      return false;
    }else{
      fr.errWorkload = "";
    }
  }
};
