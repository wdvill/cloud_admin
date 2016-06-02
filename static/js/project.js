Vue.config.delimiters = ['{[', ']}'];

// 桌面软件开发、手机应用、电子商务开发、WEB开发、产品管理、QA、SEO、脚本和工具、web 手机设计
var is_show_job_type = [5, 6, 8, 9, 10, 11, 12, 13];
// 桌面软件开发、手机应用
var is_show_platforms = [5, 8];
// 桌面软件开发、手机应用、电子商务开发、WEB开发、web 手机设计
var is_show_stage = [5, 6, 8, 12, 13];
// 桌面软件开发、手机应用、电子商务开发、WEB开发、脚本和工具
var is_show_language = [5, 6, 8, 11, 13];
var validict = {
  "category": function(obj) {
    if (obj.category == "") {
      obj.errCategory = "请选择分类";
      return false;
    } else {
      obj.errCategory = "";
    }
  },
  "name": function(obj) {
    if (obj.name.trim() == "") {
      obj.errName = "请输入项目名称";
      return false;
    } else {
      if (obj.name.length > 100) {
        obj.errName = "超出字数限制";
        return false;
      } else {
        obj.errName = "";
      }
    }
  },
  "description": function(obj) {
    if (obj.description.trim() == "") {
      obj.errDescription = "请输入项目描述";
      return false;
    } else {
      obj.errDescription = "";
    }
  },
  "hires1": function(obj) {
    if (obj.show_category == 1 && obj.hires1 == '') {
      obj.errHires1 = "请选择雇佣开发者人数";
      return false;
    } else {
      obj.errHires1 = "";
    }

    if (obj.show_category == 1 && obj.hires1 == 2 && obj.hires1_num == '') {
      obj.errHires1 = "请选输入需要雇佣的开发者人数";
      return false;
    } else {
      obj.errHires1 = "";
    }
  },
  "hires2": function(obj) {
    if (obj.show_category != 1 && obj.hires2 == '') {
      obj.errHires2 = "请选择雇佣开发者人数";
      return false;
    } else {
      obj.errHires2 = "";
    }

    if (obj.show_category != 1 && obj.hires2 == 2 && obj.hires2_num == '') {
      obj.errHires2 = "请选输入需要雇佣的开发者人数";
      return false;
    } else {
      obj.errHires2 = "";
    }
  },
  "job_type": function(obj) {
    if (obj.isShowJobType == true && obj.job_type == '') {
      obj.errJobType = "请选择是否有正在进行的项目或工作";
      return false;
    } else {
      obj.errJobType = "";
    }
  },
  "work_type": function(obj) {
    if (obj.job_type == 'once' && obj.work_type == "") {
      obj.errWorkType = "请选择工作描述";
      return false;
    } else {
      obj.errWorkType = "";
    }
  },
  "work_type2": function(obj) {

    if (obj.job_type == 'last' && obj.work_type2.length == 0) {
      obj.errWorkType2 = "请选择此项";
      return false;
    } else {
      obj.errWorkType2 = "";
    }
  },
  "platforms": function(obj) {
    if (obj.isShowPlatforms == true && obj.platforms == "") {
      obj.errPlatform = "请选择平台应用";
      return false;
    } else {
      obj.errPlatform = "";
    }
  },
  "stage": function(obj) {
    if (obj.isShowStage == true && obj.stage == "") {
      obj.errStage = "请选择项目所处阶段";
      return false;
    } else {
      obj.errStage = "";
    }
  },
  "api": function(obj) {
    if (obj.isShowStage == true && obj.api == "") {
      obj.errApi = "请选择是否集成API";
      return false;
    } else {
      obj.errApi = "";
    }
  },
  "paymethod": function(obj) {
    if (obj.paymethod == "") {
      obj.errPaymethod = "请选择一种付款方式";
      return false;
    } else {
      obj.errPaymethod = "";
    }
  },
  "level": function(obj) {
    if (obj.paymethod != "" && obj.level == "") {
      obj.errLevel = "请选择开发者需要的经验水平";
      return false;
    } else {
      obj.errLevel = "";
    }
  },
  "duration": function(obj) {
    if (obj.paymethod == "hour" && obj.duration == 0) {
      obj.errDuration = "请选择工作结束时间";
      return false;
    } else {
      obj.errDuration = "";
    }
  },
  "workload": function(obj) {
    if (obj.paymethod == "hour" && obj.workload == 0) {
      obj.errWorkload = "请选择工作投入时间";
      return false;
    } else {
      obj.errWorkload = "";
    }
  },
  "budget": function(obj) {
    if (obj.paymethod == "fixed" && obj.budget == 0) {
      obj.errBudget = "请输入项目预算";
      return false;
    } else {
      obj.errBudget = "";
    }
  }

};
var getValueByName = function(name) {
  var paramArr = location.search.substr(1).split('&'),
    parameter = {};
  for (var i = 0, len = paramArr.length; i < len; i++) {
    var param = paramArr[i].split('=');
    parameter[param[0]] = param[1];
  }
  return parameter[name] ? parameter[name] : ''
};
var job_uuid = getValueByName('q')
var project = new Vue({
  el: "#project-new",
  data: {
    job: "",
    cat_all: "",
    category: "",
    is_categoryone: true,
    categoryone: "",
    categorytwo: "",
    name: "",
    description: "",
    filename: "",
    attachment: "",
    hires1: "",
    hires1_num: 2,
    hires2: "",
    hires2_num: 2,
    skills: "",
    skills_other: "",
    isShowJobType: false,
    job_type: "",
    work_type: "",
    work_type2: [],
    //平台
    isShowPlatforms: false,
    ios: "",
    android: "",
    win: "",
    // project stage
    isShowStage: false,
    stage: "",
    isShowLanguage: false,
    languages: "",
    // api
    api: "",
    // pay method
    paymethod: "hour",
    // experience
    level: "",
    // work full time
    duration: 0,
    // work time per week
    workload: 0,
    budget: 0,

    show_category: 1,
    show_working: false,

    errRes: false,
    errCategory: "",
    errName: "",
    errDescription: "",
    errHires1: "",
    errHires2: "",
    errJobType: "",
    errWorkType: "",
    errWorkType2: "",
    errPlatform: "",
    errStage: "",
    errApi: "",
    errPaymethod: "",
    errLevel: "",
    errDuration: "",
    errWorkload: "",
    errBudget: "",
    errFile: "",
    //不同分类显示项目
    showItem: {}
  },
  ready: function() {
    var that = this;
    $.i18n().then(function(data) {
      window['CODE'] = data.CODE;
      window['COMMONS'] = data.COMMONS;
      get_category(that);

      // watch file upload
      that.watchFileInput();
      bind_skills(that);
      bind_skills_other(that);
      bind_languages(that);
      bind_frameworks(that);
      setTimeout(skills_init(that), 1000);
    });
    //this.initJob()
    this.project_init()

    // first load category

  },
  computed: {
    platforms: function() {
      var res = "";
      if (this.ios != '') {
        res += 'ios'
      }
      if (this.android != '') {
        if (res.length != 0) {
          res += ',android'
        } else {
          res += 'android'
        }
      }
      if (this.win != '') {
        if (res.length != 0) {
          res += ',win'
        } else {
          res += 'win'
        }
      }
      return res;
    },
    job_desc: function() {
      var res = '';
      if (this.job_type == 'once') {
        res = this.work_type;
      } else if (this.job_type == 'last') {
        res = this.work_type2.toString();
      } else {
        res = '';
      }
      return res;
    },
    hires: function() {
      var hires = "";
      if (this.show_category == 1) {
        if (this.hires1 == 2) {
          hires = this.hires1_num;
        } else {
          hires = this.hires1;
        }
      } else {
        if (this.hires2 == 2) {
          hires = this.hires2_num;
        } else {
          hires = this.hires2;
        }
      }
      return hires;
    }
  },
  watch: {
    skills: function(val) {},
    name: function(val, oldVal) {
      this.validate('name');
    },
    description: function(val, oldVal) {
      this.validate('description');
    },
    hires: function(val) {},
    hires1: function(val, oldVal) {
      this.validate('hires1');
    },
    hires1_num: function(val, oldVal) {
      this.validate('hires1');
    },
    hires2: function(val, oldVal) {
      this.validate('hires2');
    },
    hires2_num: function(val, oldVal) {
      this.validate('hires2');
    },
    work_type: function(val, oldVal) {
      this.validate('work_type');
    },
    work_type2: function(val, oldVal) {
      this.validate('work_type2');
    },
    platforms: function(val, oldVal) {
      this.validate('platforms');
    },
    stage: function(val, oldVal) {
      this.validate('stage');
    },
    api: function(val, oldVal) {
      this.validate('api');
    },
    paymethod: function(val, oldVal) {
      this.validate('paymethod');
    },
    level: function(val, oldVal) {
      this.validate('level');
    },
    duration: function(val, oldVal) {
      this.validate('duration');
    },
    workload: function(val, oldVal) {
      this.validate('workload');
    },
    budget: function(val, oldVal) {
      this.validate('budget');
    },
    // watch first category change
    is_categoryone: function(val, oldVal) {
      if (typeof(val) == 'undefined' || val == "none") {
        this.is_categoryone = 'none';
        this.category = '';
        $('#cat02').empty();
      } else {
        this.categorytwo = $.grep(this.cat_all, function(data) {
          return data.pid == val
        });
        $('#cat02').empty();
        for (var i = 0; i < this.categorytwo.length; i++) {
          $('#cat02').append($('<option>', {
            value: this.categorytwo[i].category_id,
            text: this.categorytwo[i].cn
          }))
        }
        this.category = this.categorytwo[0].category_id;
        var that = this;
      }
    },
    category: function(val) {
      val = val * 1;
      console.log(val, 'category id', $.inArray(val, is_show_job_type), is_show_job_type);
      this.get_show_item(val);
      if (typeof(val) != 'undefined' && $.inArray(val, is_show_job_type) != -1) {
        this.show_category = val;
      } else {
        this.show_category = 1
      }
      this.update_show_category();
    },
    job_type: function(val, oldVal) {
      if (val == 'once') {
        this.show_working = 31;
      } else if (val == 'last') {
        this.show_working = 32;
      } else {
        this.show_working = false;
      }
      this.validate('job_type');
    },
    job_desc: function(val) {
      if (this.show_working == 31) {
        this.validate('work_type');
      } else if (this.show_working == 31) {
        this.validate('work_type2');
      }
    }
  },
  methods: {
    check_cat01: function() {
      this.is_categoryone = $("input[name='cat01']").val();
    },
    initJob: function() {
      var params = location.search.substr(1);
      var reg = /id=(\w{16})/g;
      var pattern = reg.exec(params);
      var id = job_uuid;
      var that = this
      if (pattern) {
        id = pattern[1]
      }
      console.log(id, 'id');
      $.getJSON('/api/jobs', {
        job_id: id
      }, function(data) {
        if (data.error_code === 0) {
          console.log(data, 'data');
        }
        console.log('nothing');
      })

    },
    check_cat02: function() {
      this.category = $("input[name='cat02']").val();
    },
    watchFileInput: function() {
      $('#fileupload').change(this.notifyFileInput.bind(this));
    },
    notifyFileInput: function(event) {
      var file = event.target.files[0];
      if (file.size > 5 * 1024 * 1024) {
        this.errFile = "文件太大";
        return;
      } else {
        this.errFile = ""
      }
      var data = new FormData();
      var that = this;
      data.append('file', file);
      data.append('_xsrf', Cookies.get('_xsrf'));
      data.append('t', 'job')
      $.ajax({
        type: "POST",
        url: "/api/attachment",
        cache: false,
        dataType: "json",
        data: data,
        processData: false,
        contentType: false,
        error: function(xhr, textStatus) {},
        success: function(result) {
          if (result.error_code != 0) {
            that.attachment = "";
            that.filename = "";
            //that.errFile = result.msg;
            that.errRes = result.msg;
            $('#error').modal('show');
          } else {
            that.errFile = "";
            that.attachment = result.attachment_id;
            that.filename = file.name;
            result.errRes = "";
          }
        }
      });
    },
    change_obj_meta: function(obj, meta, el_value) {
      if (obj != "") {
        this[meta] = obj;
      } else {
        if (el_value) {
          this[meta] = el_value;
        } else {
          this[meta] = "";
        }
      }
    },
    change_platform: function(obj) {
      if (obj == 'ios') {
        if (this.ios == 'ios') {
          this.change_obj_meta("", "ios");
        } else {
          this.change_obj_meta(obj, "ios");
        }
      } else if (obj == 'android') {
        if (this.android == 'android') {
          this.change_obj_meta('', "android");
        } else {
          this.change_obj_meta(obj, "android");
        }
      } else if (obj == 'win') {
        if (this.win == 'win') {
          this.change_obj_meta('', "win");
        } else {
          this.change_obj_meta(obj, "win");
        }

      }

    },
    change_stage: function(obj) {
      this.change_obj_meta(obj, "stage");
    },
    change_api: function(obj) {
      this.change_obj_meta(obj, "api");
    },
    change_paymethod: function(obj) {
      this.change_obj_meta(obj, "paymethod");
    },
    change_level: function(obj) {
      this.change_obj_meta(obj, "level");
    },
    change_workload: function(obj) {
      this.change_obj_meta(obj, "workload");
    },
    change_duration: function(obj) {
      this.change_obj_meta(obj, "duration", 0);
    },
    update_show_category: function() {
      if ($.inArray(this.show_category, is_show_job_type) != -1) {
        this.isShowJobType = true;
      } else {
        this.isShowJobType = false;
        this.job_type = false;
      }
      if ($.inArray(this.show_category, is_show_platforms) != -1) {
        this.isShowPlatforms = true;
      } else {
        this.isShowPlatforms = false;
      }

      if ($.inArray(this.show_category, is_show_stage) != -1) {
        this.isShowStage = true;
      } else {
        this.isShowStage = false;
      }

      if ($.inArray(this.show_category, is_show_language) != -1) {
        this.isShowLanguage = true;
      } else {
        this.isShowLanguage = false;
      }
    },
    // 切换分类查询显示项目
    get_show_item: function(id) {
      var _self = this;
      if (!this.showItem[id]) {
        YWORK.getJson("/api/category/options", {
          category_id: id
        }).success(function(res) {
          if (res.error_code === 0) {
            _self.showItem[id] = res.options;
            _self.show_item(id)
          }
        })
      } else {
        this.show_item(id);
      }
    },
    //切换分类显示需要显示的item
    show_item: function(id) {
      var items = this.showItem[id];
      console.log(items);
      this.isShowLanguage = items.language;
      this.isShowLanguage = items.language;
      this.isShowPlatforms = items.platform;
      this.isShowStage = items.stage;
      this.isShowLanguage = items.language;
    },
    validate: function(item, event) {
      validict[item](this);
    },
    project_create: function(status, event) {
      var flag = true;
      for (var x in validict) {
        if (validict[x](this) == false) {
          flag = false;
        }
      }

      if (!flag) {
        return;
      }

      var that = this;

      var data = {
        status: status,
        _xsrf: Cookies.get("_xsrf"),
        name: that.name,
        category_id: that.category,
        skills: that.skills,
        skills_other: that.skills_other,
        duration: that.duration,
        workload: that.workload,
        level: that.level,
        hires: that.hires,
        attachment_id: that.attachment,
        job_type: that.job_type == false ? '' : that.job_type,
        job_desc: that.job_desc,
        description: that.description,
        stage: that.stage,
        budget: that.budget,
        paymethod: that.paymethod,
        platforms: that.platforms,
        api: that.api,
        languages: that.languages,
        frameworks: that.frameworks
      };

      $.ajax({
        type: "post",
        url: "/api/jobs",
        cache: false,
        dataType: "json",
        data: data,
        error: function(xhr, textStatus) {},
        success: function(result) {
          if (result.error_code != 0) {
            console.log(result.error_code);
            //that.errRes = CODE[result.error_code];
            that.errRes = result.msg;
            $('#error').modal('show');
          } else {
            if (status == "draft") {
              window.location.href = '/clients/jobs';
            } else {
              window.location.href = '/jobs/new/complete/' + result.job_id;
            }
          }
        }
      });
    },
    project_init: function() {
      var that = this;
      Service.get('Myproject').pro_details({
        job_id: job_uuid
      }).success(function(result) {
        if (result.job != null || result.job != undefined) {
          that.job = result.job
          that.name = result.job.name
          that.category_id = result.job.category
          that.skills = result.job.skills.join(',')
          that.skills_other = result.job.skills_other
          that.duration = result.job.duration
          that.workload = result.job.workload
          that.level = result.job.level
          that.hires = result.job.hires
          that.attachment_id = result.job.attachment
          if (result.job.attachment.name != undefined) {
            that.filename = result.job.attachment.name
            $("#collapseOne").show()
          }
          that.job_type = result.job.job_type
          that.job_desc = result.job.job_desc
          that.description = result.job.description
          that.stage = result.job.stage
          that.budget = result.job.budget
          that.paymethod = result.job.paymethod
          that.platforms = result.job.platforms
          that.api = result.job.api
          that.languages = result.job.languages
          that.frameworks = result.job.frameworks
        }
      });
    }
  }
});

function skills_init(obj) {
  $('.selectize-input').click()
  setTimeout(function() {
    obj.$data.skills.split(',').forEach(function(value) {
      var el = $(".selectize-dropdown-content div[data-value='" + value + "']")
      el.click()
    })
    $('.selectize-input input').blur()
  }, 300)
}

function bind_skills(obj) {
  var arr = $("#project-skills").val().split(",");
  var arr1 = [];
  for (var i = 0; i < arr.length; i++) {
    arr1.push({
      value: arr[i],
      text: arr[i]
    });
  }
  $('#select-skills').selectize({
    plugins: ['remove_button'],
    delimiter: ',',
    persist: false,
    maxItems: null,
    options: arr1,
    create: false
  });
}

function bind_skills_other(obj) {
  var arr = $("#project-skills-other").val().split(",");
  var arr1 = [];
  for (var i = 0; i < arr.length; i++) {
    arr1.push({
      value: arr[i],
      text: arr[i]
    });
  }
  $('#select-skills-other').selectize({
    plugins: ['remove_button'],
    delimiter: ',',
    persist: false,
    maxItems: null,
    options: arr1,
    create: false
  });
}

function bind_languages(obj) {
  var arr = $("#project-languages").val().split(",");
  var arr1 = [];
  for (var i = 0; i < arr.length; i++) {
    arr1.push({
      value: arr[i],
      text: arr[i]
    });
  }

  $('#select-languages').selectize({
    plugins: ['remove_button'],
    delimiter: ',',
    persist: false,
    maxItems: 2,
    options: arr1,
    create: false
  });
}

function bind_frameworks(obj) {
  var arr = $("#project-frameworks").val().split(",");
  var arr1 = [];
  for (var i = 0; i < arr.length; i++) {
    arr1.push({
      value: arr[i],
      text: arr[i]
    });
  }

  $('#select-frameworks').selectize({
    plugins: ['remove_button'],
    delimiter: ',',
    persist: false,
    //maxItems: 2,
    options: arr1,
    create: false
  });
}

function get_category(obj) {
  $.ajax({
    type: "post",
    url: "/api/category",
    cache: false,
    dataType: "json",
    data: {
      _xsrf: Cookies.get("_xsrf"),
      category_id: 0,
      t: 'all'
    },
    error: function(xhr, textStatus) {},
    success: function(result) {
      if (result.error_code != 0) {
        obj.errRes = result.msg;
        $('#error').modal('show');
      } else {
        //for(var i=0;i<result.categorys.length;i++){
        //  result.categorys[i].name = COMMONS[result.categorys[i].name];
        //}
        obj.cat_all = localized(result.categorys, 'name');
        obj.categoryone = $.grep(result.categorys, function(data) {
          return data.pid == 0;
        });
        $('#cat01').empty();
        $('#cat01').append($('<option>', {
          value: 'none',
          text: '--请选择--'
        }));
        for (var i = 0; i < obj.categoryone.length; i++) {
          $('#cat01').append($('<option>', {
            value: obj.categoryone[i].category_id,
            text: obj.categoryone[i].cn
          }))
        }
      }
    }
  });
}



function localized(input, localizedKey, key) {
  if (!COMMONS) {
    return;
  }
  var key = key ? key : 'cn';
  if ($.isArray(input)) {
    for (var i = 0; i < input.length; i++) {
      if (input[i][localizedKey]) {
        //input[i][key] = COMMONS[input[i][localizedKey]]
        input[i][key] = input[i][localizedKey]
      }
    }
  } else if ($.isPlainObject(input)) {
    if (input[localizedKey]) {
      //input[key] = COMMONS[input[localizedKey]]
      input[key] = input[localizedKey]
    }
  }
  return input
}