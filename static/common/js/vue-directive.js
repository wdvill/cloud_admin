Vue.config.delimiters = ['{[', ']}'];
Vue.filter('date_to_str', function (value, length) {
  if (!length) {
    length = 10;
  }
  return value.substr(0, parseInt(length));
});

Vue.filter('date_to_hour', function (value, length) {
  if (!length) {
    length = 16;
  }
  return value.substr(0, parseInt(length));
});


Vue.directive('yzj-year', {
  params: ['type'],
  update: function (start) {
    var currentDate = new Date();
    start = parseInt(start);
    end = currentDate.getFullYear();
    for (var i = end; i >= start; i--) {
      if (i == end && this.params.type == 'start') {
        this.el.innerHTML += '<option value="">入学时间</option><option value="' + i + '">' + i + '年</option>';
      } else if (i == end && this.params.type == 'end') {
        this.el.innerHTML += '<option value="">毕业时间</option><option value="' + i + '">' + i + '年</option>';
      } else {
        this.el.innerHTML += '<option value="' + i + '">' + i + '年</option>';
      }
    }
  },
});
Vue.directive('yzj-month', {
  bind: function () {
    for (var i = 1; i < 13; i++) {
      if (i == 1) {
        this.el.innerHTML += '<option selected value="' + i + '">' + i + ' 月</option>';
      } else {
        this.el.innerHTML += '<option value="' + i + '">' + i + ' 月</option>';
      }

    }
  },
});


Vue.directive('yzj-error-dailog', {
  deep: true,
  update: function () {
    console.log(this.message);
    this.el.innerHTML = '<div style="display:block;" class="modal fade" id="yzj-error" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">' +
      '<div class="modal-dialog modal-warning" role="document">' +
      '<div class="modal-content">' +
      '<div class="modal-header"></div>' +
      '<div class="modal-body"><h4 class="modal-title text-center text-danger" id="myModalLabel"><strong>{{message}}</strong></h4></div>' +
      '<div class="modal-footer text-center">' +
      '<button type="button" data-dismiss="modal"  class="btn btn-danger btn-sm">确定</button>' +
      '</div></div></div></div>',
      // $("#yzj-error").'show';
      $("#yzj-error").hide();
  },
  show: function (message) {
    if (!message) {
      message = "错误信息";
    }
    $("#yzj-error").html($("#yzj-error").html().replace('{{message}}', message));
    $("#yzj-error").modal('show');
  },
  hide: function () {
    $("#yzj-error").modal('hide');
  }
});

//分页指令

Vue.directive('page', {
  data: null,
  params: ['query'],
  acceptStatement: true,
  update: function (pageObject) {
    var self = this;
    str = "";
    if (!pageObject) {
      return;
    }
    var maxPage = Math.ceil(pageObject.itemsCount / pageObject.pageSize);
    var pageNo = pageObject.pageNo;
    var str = '<nav class="sabrosus"><ul class="pagination">';
    if (maxPage > 10) {
      if (pageNo > 3) { //minPage + 2
        str += '<li><a href="javascript:;">《</a></li>';
        str += '<li><span>......</span></li>';
      }
      for (var i = pageNo <= 2 ? 1 : pageNo - 2; i <= (pageNo >= maxPage - 2 ? maxPage : pageNo + 2); i++) {
        if (i == 1) {
          if (pageNo == 1) {
            str += '<li  class="disabled"><span>《</span></li>';
            str += '<li class="active"><span>' + i + '</span></li>';
          } else {
            str += '<li><a href="javascript:;">《</a></li>';
            str += '<li><a href="javascript:;">' + i + '</a></li>';
          }
        } else if (i == maxPage) {
          if (pageNo == maxPage) {
            str += '<li class="active"><span >' + i + '</span></li>';
            str += '<li class="disabled"><span>》</span></li>';
          } else {
            str += '<li><a href="javascript:;">' + i + '</a></li>';
            str += '<li><a href="javascript:;">》</a></li>';
          }
        } else {
          if (pageNo == i) {
            str += '<li class="active"><span>' + i + '</span></li>';
          } else {
            str += '<li><a href="javascript:;" >' + i + '</a></li>';
          }
        }
      }
      if (pageNo < maxPage - 2) {
        str += '<li><span>......</span></li>';
        str += '<li><a href="javascript:;">》</a></li>';
      }
    } else if (maxPage <= 10 && maxPage > 1) {
      for (var i = 1; i <= maxPage; i++) {
        if (i == 1) {
          if (pageNo == 1) {
            str += '<li class="disabled"><span>《</span></li>';
            str += '<li class="active"><span >' + i + '</span></li>';
          } else {
            str += '<li><a href="javascript:;">《</a></li>';
            str += '<li><a href="javascript:;">' + i + '</a></li>';
          }
        } else if (i == maxPage) {
          if (pageNo == maxPage) {
            str += '<li  class="active"><span >' + i + '</span></li>';
            str += '<li class="disabled"><span >》</span></li>';
          } else {
            str += '<li><a href="javascript:;">' + i + '</a></li>';
            str += '<li><a href="javascript:;">》</a></li>';
          }
        } else {
          if (pageNo == i) {
            str += '<li class="active"><span>' + i + '</span></li> ';
          } else {
            str += '<li> <a href="javascript:;" >' + i + '</a></li> ';
          }
        }
      }
    }
    str += '</ul></nav>';
    this.el.innerHTML = str;
    $("nav[class=sabrosus]").find('a').on('click', function () {
      var text = $(this).html();
      var pageNo = pageObject.pageNo;
      if ($.trim(text) == '《') {
        pageObject.pageNo = pageNo - 1;
      } else if ($.trim(text) == '》') {
        pageObject.pageNo = pageNo + 1;
      } else {
        pageObject.pageNo = parseInt(text);
      }
      self.params.query.call(self);
    });
  },
});