Vue.config.delimiters = ['{[', ']}'];

function Search(){
  this.loading = false;
  this.pagesize = 10;
  this.container = null;
  $.i18n().then(function(data){
    window['CODE'] = data.CODE;
    window['COMMONS'] = data.COMMONS;
  });
}

Search.prototype.search = function(pagenum){
  var data = {};
  data.workload = [];
  data.duration = [];
  data.level = [];
  data.paymethod = [];
  var container = this.container;
  if(container.load_part){
    data.workload.push(1);
  }
  if(container.load_full){
    data.workload.push(2);
  }
  if(container.load_none){
    data.workload.push(3);
  }
  data.workload = data.workload.join();

  if(container.dur_day){
    data.duration.push(1);
  }
  if(container.dur_week){
    data.duration.push(2);
  }
  if(container.dur_month){
    data.duration.push(3);
  }
  if(container.dur_year){
    data.duration.push(4);
  }
  if(container.dur_none){
    data.duration.push(5);
  }
  data.duration = data.duration.join();

  if(container.level_entry){
    data.level.push("entry");
  }
  if(container.level_middle){
    data.level.push("middle");
  }
  if(container.level_high){
    data.level.push("expert");
  }
  data.level = data.level.join();

  if(container.type_hour){
    data.paymethod.push("hour");
  }
  if(container.type_fixed){
    data.paymethod.push("fixed");
  }
  data.paymethod = data.paymethod.join();

  data.category_id = container.cate_selected;
  data.keyword = container.keyword;
  data.pagenum = pagenum;
  data.pagesize = this.pagesize;
  data._xsrf = Cookies.get("_xsrf");

  var that = this;
  $.ajax({
    type: "post",
    url: "/api/jobs/search",
    cache: false,
    dataType: "json",
    data: data,
    error: function (xhr, textStatus) {
    },
    success: function (json) {
      if(json.error_code == 0){
        for(var i=0; i<json.jobs.length; i++){
          json.jobs[i].level = COMMONS[json.jobs[i].level];
          json.jobs[i].paymethod = COMMONS[json.jobs[i].paymethod];
          json.jobs[i].duration = COMMONS[json.jobs[i].duration];
        }
        container.jobs = json.jobs;
        container.all = parseInt(json.count / that.pagesize) + 1;
        container.cur = json.pagenum;
      }else{
        alert(CODE[json.error_code]);
      }
    }
  });
};

Search.prototype.get_category = function(that){
  $.ajax({
    type: "post",
    url: "/api/category",
    cache: false,
    dataType: "json",
    data: {
      _xsrf: Cookies.get("_xsrf"),
      category_id: 0
    },
    error: function (xhr, textStatus) {
    },
    success: function (json) {
      if(json.error_code == 0){
        for(var i=0; i<json.categorys.length; i++){
          json.categorys[i].name = COMMONS[json.categorys[i].name];
        }
        that.category = json.categorys;
      }else{
        alert(CODE[json.error_code]);
      }
    }
  });
};

var search = new Search();
var container = new Vue({
  el: "#find-job-con",
  data: {
    category: "",
    cate_selected: 0,
    budget: 0,
    budget_step: 100,
    type_hour: true,
    type_fixed: true,
    level_entry: true,
    level_middle: true,
    level_high: true,
    dur_day: true,
    dur_week: true,
    dur_month: true,
    dur_year: true,
    dur_none: true,
    load_part: true,
    load_full: true,
    load_none: true,
    keyword: "",
    jobs: "",

    cur: 1,
    showFirst: true,
    showLast: false,
    all: 1
  },
  created: function() {
    search.container = this;
    search.get_category(this);
    var q = $.getParameterByName("q");
    if(q != ""){
      this.keyword = q;
      search.search();
    }
  },
  methods: {
    search: function() {
      if(this.keyword != ""){
        this.jobs = "";
        search.search();
      }
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
      search.search(this.cur);
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
      search.search(this.cur);
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
      search.search(index);
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
