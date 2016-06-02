Vue.config.delimiters = ['{[', ']}'];


function FindHome(){
  this.con = null;
  this.categorys = null;
  this.user_categorys = null;
  $.i18n().then(function(data){
    window['CODE'] = data.CODE;
    window['COMMONS'] = data.COMMONS;
  });
}

FindHome.prototype.get_list = function(num){
  var con = this.con;
  $.ajax({
    type: "post",
    url: "/api/jobs",
    cache: false,
    dataType: "json",
    data: {
      pagenum: num,
      _xsrf: Cookies.get("_xsrf")
    },
    error: function (xhr, textStatus) {
    },
    success: function (json) {
      if(json.error_code == 0){
        for(var i=0; i<json.jobs.length; i++){
          json.jobs[i].level = COMMONS['_level'][json.jobs[i].level];
          json.jobs[i].paymethod = COMMONS['_paymethod'][json.jobs[i].paymethod];
          json.jobs[i].duration = COMMONS['_duration'][json.jobs[i].duration];
        }
        con.jobs = json.jobs;
        con.all = parseInt(json.count / con.pagesize) + 1;
        con.cur = json.pagenum;
      }else{
        alert(CODE[json.error_code]);
      }
    }
  });
};

FindHome.prototype.get_category = function(){
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
          if(json.categorys[i].pid == 0){
            arr[json.categorys[i].category_id] = {"name":json.categorys[i].name, "children":[]}
          }else{
            arr[json.categorys[i].pid]["children"].push({"name":json.categorys[i].name, "category_id":json.categorys[i].category_id});
          }
        }
        con.categorys = arr;
        that.categorys = arr;
      }else{
        alert(CODE[json.error_code]);
      }
    }
  });
};

FindHome.prototype.user_category = function(){
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
          json.categorys[i].name = COMMONS[json.categorys[i].name];
        }
        con.user_categorys = json.categorys;
        that.user_categorys = json.categorys;
      }else{
        alert(CODE[json.error_code]);
      }
    }
  });
};

FindHome.prototype.user_category_update = function(){
  var con = this.con;
  var that = this;
  $.ajax({
    type: "put",
    url: "/api/user/category",
    cache: false,
    dataType: "json",
    data: {
      category: con.select_categorys.join(),
      _xsrf: Cookies.get("_xsrf")
    },
    error: function (xhr, textStatus) {
    },
    success: function (json) {
      if(json.error_code == 0){
        $('#modal-cate').modal('hide');
        that.user_category();
      }else{
        alert(CODE[json.error_code]);
      }
    }
  });
};

var fh = new FindHome();

var container = new Vue({
  el: "#body",
  data: {
    keyword: "",
    jobs: "",
    user_categorys: "",
    categorys: "",
    select_categorys: [],
    all: 2,
    cur: 1,
    showFirst: true,
    showLast: false,
    pagesize: 10
  },
  created: function(){
    var that = this;
    fh.con = this;
    fh.get_list(1);
    fh.user_category();
    fh.get_category();
    $("#modal-cate").on('shown.bs.modal', function () {
      for(var i=0;i<fh.user_categorys.length;i++){
        that.select_categorys.push(fh.user_categorys[i].category_id.toString());
      }
    });
    $("#modal-cate").on('hidden.bs.modal', function () {
      that.select_categorys = [];
    });
  },
  watch: {
    select_categorys: function(val, oldval){
      if(val.length > 10){
        alert("最多可选择10项类别");
        val.splice(val.length-1, 1);
        return;
      }
    }
  },
  methods: {
    search: function() {
      if(this.keyword != ""){
        location.href = "/jobs/find?q=" + this.keyword;
      }
    },
    update_user_category: function() {
      fh.user_category_update();
    },
    page_prev: function() {
      if(this.cur == 1){
        this.showFirst = true;
        return;
      }
      if(this.showLast == true){
        this.showLast = false;
      }
      this.cur--;
      fh.get_list(this.cur);
    },
    page_next: function() {
      if(this.cur == this.all){
        this.showLast = true;
        return;
      }
      if(this.showFirst == true){
        this.showFirst = false;
      }
      this.cur++;
      fh.get_list(this.cur);
    },
    page_cur: function(index) {
      if(index == this.cur){
        return;
      }
      if(index == 1){
        this.showFirst = true;
      }else{
        this.showFirst = false;
      }
      if(index == this.all){
        this.showLast = true;
      }else{
        this.showLast = false;
      }
      this.cur = index;
      fh.get_list(index);
    }
  },
  computed: {
    indexs: function(){
      var left = 1
      var right = this.all
      var ar = []
      if(this.all>= 11){
        if(this.cur > 5 && this.cur < this.all-4){
                left = this.cur - 5
                right = this.cur + 4
        }else{
            if(this.cur<=5){
                left = 1
                right = 10
            }else{
                right = this.all
                left = this.all -9
            }
        }
      }
      while (left <= right){
          ar.push(left);
          left ++;
      }
      return ar;
      },
    }
});
