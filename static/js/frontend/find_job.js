var getValueByName = function(name) {
  var paramArr = location.search.substr(1).split('&'),
    parameter = {};
  for (var i = 0, len = paramArr.length; i < len; i++) {
    var param = paramArr[i].split('=');
    parameter[param[0]] = param[1];
  }
  return parameter[name] ? parameter[name] : ''
};
$.i18n().then(function(data) {
  window['CODE'] = data.CODE;
  window['COMMONS'] = data.COMMONS;
  new Vue({
    el: "body",
    data: {
      globel: {},
      categories: [], //项目父分类
      child_categories: [], //项目子分类
      category_ids: [],
      current_parent: '',
      current_child: '',
      paymethods: [],
      levels: [],
      durations: [],
      workloads: [],
      works: [],
      keyword: "",
      pageObject: {
        itemsCount: 0,
        pageNo: 1,
        pageSize: 10
      },
      subscribes: [],
      time_sort: 'up'
    },
    watch: {
      'category_ids': function(val, oldVal) {
        this.query_work_list();
      },
      'paymethods': function(val, oldVal) {
        this.query_work_list();
      },
      'levels': function(val, oldVal) {
        this.query_work_list();
      },
      'durations': function(val, oldVal) {
        this.query_work_list();
      },
      'workloads': function(val, oldVal) {
        this.query_work_list();
      }
    },
    ready: function() {
      var that = this;
      var category_id = getValueByName('category');
      that.globel = COMMONS;
      that.globel.level_price = {
        'entry': '<100元/小时',
        'middle': '100元-300元/小时',
        'expert': '>300元/小时'
      }
      Service.get('CommonService').category({
        category_id: 0
      }).success(function(result) {
        that.categories = result.categorys;
      });
      this.keyword = decodeURI(getValueByName('q'));
      var pid = decodeURI(getValueByName('pid'));
      if (pid) {
        this.category_pid = pid;
      }
      var cid = decodeURI(getValueByName('cid'));
      if (cid) {
        this.category_ids = [cid * 1];
      }
      /*
      if(category_id) {
        this.category_ids = [category_id]
      }
      */
      this.query_work_list();
      this.subscribe_works();
    },
    methods: {
      query_work_list: function() {
        var that = this;
        var data = {
          workload: that.workloads.join(","),
          duration: that.durations.join(","),
          level: that.levels.join(","),
          paymethod: that.paymethods.join(","),
          categorys: that.category_ids.join(","),
          pagesize: 10,
          keyword: that.keyword,
          pagenum: that.pageObject.pageNo,
        }

        Service.get('WorkService').works(data).success(function(result) {
          that.pageObject = {
            itemsCount: result.count,
            pageNo: result.pagenum,
            pageSize: data.pagesize
          };
          that.works = result.jobs;
          _.sortBy(that.works, 'create_at');
        });

        this.remeber();


      },
      remeber: function() {
        if (localStorage) {
          var old = localStorage.getItem('search_keywords');
          var current = [];
          if (old && this.keyword) {
            old = old.split(',');
            old.push(this.keyword);
            current = $.unique(old);
            if (current.length > 5) {
              current = current.splice(current.length - 5, 5);
            }
            localStorage.setItem('search_keywords', current);
          } else if (this.keyword) {
            localStorage.setItem('search_keywords', this.keyword);
          }

        }
      },
      sortByTime: function() {
        var sort = null;
        if (this.time_sort == 'up') {
          this.time_sort = 'down';
          //_.sortBy(this.works, 'create_at');
          this.works.reverse();
        } else {
          this.time_sort = 'up';
          //_.sortBy(this.works, 'create_at');
          this.works.reverse();
        }
      },
      select_child_category: function() {
        var that = this;
        if (!that.category_pid) {
          return;
        }
        Service.get('CommonService').category({
          category_id: that.category_pid
        }).success(function(result) {
          that.child_categories = result.categorys;
          if (_.findIndex(that.child_categories, {
              category_id: that.category_ids[0] * 1
            }) < 0) {
            that.category_ids = [];
          }
        })
      },
      search: function() {
        this.query_work_list();
        $("#addSubscribe").attr("disabled", false);
        $("#addSubscribe").html("+  添加到我的订阅");
      },
      enter: function(event) {
        if (event.keyCode === 13) {
          event.stopPropagation()
          event.preventDefault()
          this.query_work_list();
          $("#addSubscribe").attr("disabled", false);
          $("#addSubscribe").html("+  添加到我的订阅");
        }
      },
      collect: function(item) {
        var that = this;
        data = {
          target_id: item.id
        }
        if (item.favorite) {
          Service.get('WorkService').del_collect(data).success(function(result) {
            if (result.error_code == 0) {
              item.favorite = false;
            }
          });
        } else {
          Service.get('WorkService').collect(data).success(function(result) {
            if (result.error_code == 0) {
              item.favorite = true;
            }
          });
        }


      },
      subscribe_works: function() {
        var that = this;
        Service.get('WorkService').subscribe_works().success(function(result) {
          if (result.error_code == 0) {
            that.subscribes = result.subscribes
          }
        });
      },
      /* 添加订阅 */
      subscribe: function() {
        if (this.keyword == "") {
          return;
        }
        for (var i = 0; i < this.subscribes.length; i++) {
          if (this.subscribes[i].name == this.keyword) {
            return;
          }
        }
        var data = {
          name: this.keyword,
          duration: this.durations.join(),
          workload: this.workloads.join(),
          paymethod: this.paymethods.join(),
          level: this.levels.join(),
          keyword: this.keyword
        };
        Service.get('WorkService').post_subscribe(data).success(function(result) {
          if (result.error_code != 0) {
            alert(result.msg);
          } else {
            $("#addSubscribe").attr("disabled", true);
            $("#addSubscribe").html("已添加");
          }
        });
      }
    }
  });
})