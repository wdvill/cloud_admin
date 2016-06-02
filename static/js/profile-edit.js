Vue.config.delimiters = ['{[', ']}'];

Vue.filter('date_to_str', function(value, f){
    return $.format.date(new Date(value * 1000), f);
  }
);

function get_default_data(){
  return {
    cat_all: [],
    add_all: [],
    errRes: "",
    // init list data
    employments: "",
    educations: "",
    projects: "",
    id_emp: "",
    id_edu: "",
    id_pro: "",
    // data for work company
    level: "",
    errLevel: "",

    is_address_state: true,
    address_state: "",
    address_city: "",
    company: "",
    city: "",
    title: "",
    role: "",
    working: false,
    detail: "",

    date01_year: "none",
    date01_month: "none",
    date02_year: "none",
    date02_month: "none",
    errCompany: "",
    errCity: "",
    errTitle: "",
    errRole: "",
    errDate: "",

    // data for education
    school: "",
    year_begin: "none",
    year_end: "none",
    degree: "",
    area: "",
    detail_edu: "",

    errSchool: "",
    errDateEdu: "",
    errDegree: "",
    errArea: "",
    errDetailEdu: "",

    // data for project
    pname: "",
    detail_pro: "",
    picture: "",
    picture_name: "",
    picture_path: "",
    category: "",
    is_categoryone: true,
    categoryone: "",
    categorytwo: "",
    address: "",
    end_pro: "",
    skills: "",
    errName: "",
    errDetailPro: "",
    errPicture: "",
    errCategory: "",
    errAddress: "",
    errEdnPro: "",
    errSkills: ""
  }
}

var p = new Vue({
  el: "#profile_edit",
  data: get_default_data(),
  created: function(){
    //bind_skills(this);
    bind_data_init(this);

    this.project_upload();

    get_category(this);

    get_address(this);

    this.employments = this.get_employments();
    this.educations = this.get_educations();
    this.projects = this.get_projects();

    $.i18n();

  },
  computed: {
    year_list: function(){
      return $.get_year_list();
    },
    month_list: function(){
      return $.get_month_list();
    },
    date01: function(){
      return this.date01_year + '-' + this.date01_month;
    },
    date02: function(){
      return this.date02_year + '-' + this.date02_month;
    }
  },
  watch: {
    // for work company
    company: function(val){
      if(this.company.length != 0){
        this.validate('company', 'company')
      }
    },
    city: function(val){
      if(this.city.length != 0){
        this.validate('city', 'company')
      }
    },
    title: function(val){
      if(this.title.length != 0){
        this.validate('title', 'company')
      }
    },
    date01: function(val){
      if(this.date01 != 'none-none'){
        this.validate('date', 'company')
      }
    },
    date02: function(val){
      if(this.date02 != 'none-none'){
        this.validate('date', 'company')
      }
    },
    // for eduction
    school: function(val){
      if(this.school.length != 0){
        this.validate('school', 'edu')
      }
    },
    degree: function(val){
      if(this.degree.length != 0){
        this.validate('degree', 'edu')
      }
    },
    area: function(val){
      if(this.area.length != 0){
        this.validate('area', 'edu')
      }
    },
    year_begin: function(val){
      if(this.year_begin != 'none'){
        this.validate('year_edu', 'edu')
      }
    },
    year_end: function(val){
      if(this.year_end != 'none'){
        this.validate('year_edu', 'edu')
      }
    },
    // for project
    pname: function(val){
      if(this.pname.length != 0){
        this.validate('pname', 'pro')
      }
    },
    detail_pro: function(val){
      if(this.detail_pro.length != 0){
        this.validate('detail_pro', 'pro')
      }
    },
    category: function(val){
      if(this.category != ""){
        this.validate('category', 'pro')
      }
    },
    is_categoryone: function(val){
      if(typeof(val) == 'undefined' || val == "none" || val == true){
        this.is_categoryone = 'none';
        this.category = '';
        $('#lb02').empty();
      }else{
        this.categorytwo = $.grep(this.cat_all, function(data){
          return data.pid == val
        });

        var data = [];
        for(var i=0; i<this.categorytwo.length; i++){
          data.push({value: this.categorytwo[i].category_id, text: this.categorytwo[i].name})
        }
        bind_select_list_option(this, 'lb02', data, 'category', false);

        this.category = this.categorytwo[0].category_id;
        this.set_select_value('lb02', this.categorytwo[0].category_id, this.categorytwo[0].name)
      }
    },
    is_address_state: function(val){
      if(typeof(val) == 'undefined' || val == "none" || val == true){
        this.is_address_state = 'none';
        this.city = '';
        $('#address_city').empty();
      }else{
        this.address_city = $.grep(this.add_all, function(data){
          return data.pid == val
        });

        var data = [];
        for(var i=0; i<this.address_city.length; i++){
          data.push({value: this.address_city[i].address_id, text: this.address_city[i].name})
        }
        bind_select_list_option(this, 'address_city', data, 'city', false);

        this.city = this.address_city[0].address_id;
        this.set_select_value('address_city', this.address_city[0].address_id, this.address_city[0].name)
      }
    },
  },
  methods: {
    formate_date: function(value, f){
      return $.format.date(new Date(value * 1000), f);
    },
    set_select_value: function(id, value, text){
      $("input[name='"+id+"']").val(value);
      $("#"+id+" >:input[class='select-button']").val(text);
    },
    check_input_val: function(id, key){
      this._data[key] = $("input[name='"+id+"']").val();
    },
    goback: function(event){
      window.location.href = "/users/profile/step/2"
    },
    save_and_countinue: function(event){
      if(this.level == ""){
        this.errLevel = "请选择等级";
        return;
      }else{
        this.errLevel = "";
      }
      var that = this;
      var data = new FormData();
      data.append('level', that.level);
      data.append('_xsrf', Cookies.get("_xsrf"));
      data.append('session_token', Cookies.get("session_token"));
      $.ajax({
        type: "POST",
        url: "/api/user/resume",
        cache: false,
        dataType: "json",
        data: data,
        processData: false,
        contentType: false,
        error: function (xhr, textStatus){
        },
        success: function (result){
          if(result.error_code != 0){
            that.errRes = result.msg;
            $('#error').modal('show');
          }else{
            window.location.href = "/users/profile/step/4";
          }
        }
      });
    },
    operate_common: function(flag, data, that, operate, status){
      var rdata = new FormData();
      $.each(data, function(key, value){
        rdata.append(key, value);
      });
      rdata.append('_xsrf', Cookies.get("_xsrf"));
      rdata.append('session_token', Cookies.get("session_token"));
      $.ajax({
        type: operate,
        url: "/api/"+ flag,
        cache: false,
        dataType: "json",
        data: rdata,
        processData: false,
        contentType: false,
        error: function (xhr, textStatus){
        },
        success: function (result){
          if(result.error_code != 0){
            if(flag == 'employment'){
              if(operate == 'GET'){
                that.employments = false;
              }
            }else if(flag == 'education'){
              if(operate == 'GET'){
                that.educations = false;
              }
            }else if(flag == 'portfolio'){
              if(operate == 'GET'){
                that.projects = false;
              }
            }
            that.errRes = result.msg;
            $('#error').modal('show');
          }else{
            if(flag == 'employment'){
              if(operate == 'GET'){
                if(result.employments.length > 0){
                  that._data.employments = result.employments;
                }else{
                  that._data.employments = false;
                }
              }else if(operate == 'DELETE'){
                that.employments = $.grep(that.employments, function(obj){
                  return obj.id != data.eid;
                });
              }else if(operate == 'POST'){
                that.reset_data();
                if(status == 'save'){
                  $('#work_company_close').click();
                }
                that.get_employments();
              }else if(operate == 'PUT'){
                that.reset_data();
                if(status == 'save'){
                  $('#work_company_close').click();
                }
                that.get_employments();
              }
            }else if(flag == 'education'){
              if(operate == 'GET'){
                if(result.educations.length > 0){
                  that.educations = result.educations;
                }else{
                  that.educations = false;
                }
              }else if(operate == 'DELETE'){
                that.educations = $.grep(that.educations, function(obj){
                  return obj.id != data.eid;
                });
              }else if(operate == 'POST'){
                that.reset_data();
                if(status == 'save'){
                  $('#education_close').click();
                }
                that.get_educations();
              }else if(operate == 'PUT'){
                that.reset_data();
                if(status == 'save'){
                  $('#education_close').click();
                }
                that.get_educations();
              }
            }else if(flag == 'portfolio'){
              if(operate == 'GET'){
                if(result.portfolios.length > 0){
                  that.projects = result.portfolios;
                }else{
                  that.projects = false;
                }
              }else if(operate == 'DELETE'){
                that.projects = $.grep(that.projects, function(obj){
                  return obj.id != data.pid;
                });
              }else if(operate == 'POST'){
                that.reset_data();
                if(status == 'save'){
                  $('#project_close').click();
                }
                that.get_projects();
              }else if(operate == 'PUT'){
                that.reset_data();
                if(status == 'save'){
                  $('#project_close').click();
                }
                that.get_projects();
              }
            }
          }
        }
      });
    },
    get_employments: function(eid){
      var data = {};
      if(eid){
        data.eid = eid;
      }
      this.operate_common('employment', data, this, 'GET');
    },
    get_educations: function(eid){
      var data = {};
      if(eid){
        data.eid = eid;
      }
      this.operate_common('education', data, this, 'GET')
    },
    get_projects: function(pid){
      var data = {};
      if(pid){
        data.pid = pid;
      }
      this.operate_common('portfolio', data, this, 'GET')
    },
    delete_object: function(flag, id, event){
      var data = {};
      if(flag == 'employment'){
        data.eid = id;
      }else if(flag == 'education'){
        data.eid = id;
      }else if(flag == 'portfolio'){
        data.pid = id;
      }
      this.operate_common(flag, data, this, 'DELETE');
    },
    add_employment: function(status, event){
      var flag = true;
      for(var x in work_company_validict){
        if(work_company_validict[x](this) == false){
          flag = false;
        }
      }
      if(!flag){
        return;
      }
      var that = this;
      var data = {};
      if(that.id_emp != ""){
        data.eid = that.id_emp;
      }
      data.company = that.company;
      data.city_id = that.city;
      data.title = that.title;
      data.role = that.role;
      data.start_at = that.date01;
      data.end_at = that.date02;
      data.working = that.working;
      data.detail = that.detail;
      if(that.id_emp != ""){
        this.operate_common('employment', data, that, 'PUT', status);
      }else{
        this.operate_common('employment', data, that, 'POST', status);
      }
    },
    add_education: function(status, event){
      var flag = true;
      for(var x in education_validict){
        if(education_validict[x](this) == false){
          flag = false;
        }
      }
      if(!flag){
        return;
      }
      var that = this;
      var data = {};
      if(that.id_edu != ""){
        data.eid = that.id_edu;
      }
      data.school = that.school;
      data.degree = that.degree;
      data.area = that.area;
      data.start_at = that.year_begin;
      data.end_at = that.year_end;
      data.detail = that.detail_edu;
      if(that.id_edu != ""){
        this.operate_common('education', data, that, 'PUT', status);
      }else{
        this.operate_common('education', data, that, 'POST', status);
      }

    },
    add_project: function(status, event){
      var flag = true;
      for(var x in project_validict){
        if(project_validict[x](this) == false){
          console.log('x', x);
          flag = false;
        }
      }

      if(!flag){
        return;
      }
      var that = this;
      var data = {};
      if(that.id_pro != ""){
        data.pid = that.id_pro;
      }
      data.name = that.pname;
      data.detail = that.detail_pro;
      data.picture_id = that.picture;
      data.category_id = that.category;
      data.link = that.address;
      data.end_at = that.end_pro;
      data.skills = that.skills;
      if(that.id_pro != ""){
        this.operate_common('portfolio', data, that, 'PUT', status);
      }else{
        this.operate_common('portfolio', data, that, 'POST', status);
      }

    },
    reset_data_filter: function(filter){
      var data_default = get_default_data();
      if(filter){
        data_default.cat_all = this.cat_all;
        data_default.add_all = this.add_all;
        data_default.employments = this.employments;
        data_default.educations = this.educations;
        data_default.projects = this.projects;
      }
      this.reset_select_list();
      this.$data = data_default;
    },
    reset_select_list: function(){
      var id_list = [
        'address_state', 'address_city', 'role', 'date01_year', 'date01_month', 'date02_year', 'date02_month',
        'school_begin', 'school_end', 'degree',
        'lb01', 'lb02', 'end_pro'
      ];
      for(var i=0; i<id_list.length; i++){
        this.set_select_value(id_list[i], 'none', '--请选择--')
      }

    },
    reset_data: function(){
      this.reset_data_filter(true);
    },
    validate: function(item, flag) {
      if(flag == 'company'){
        work_company_validict[item](this);
      }else if(flag == 'edu'){
        education_validict[item](this);
      }else if(flag == 'pro'){
        project_validict[item](this);
      }
    },
    change_level: function(obj){
      var level_array = ['entry', 'middle', 'expert'];
      if($.inArray(obj, level_array) != -1){
        this['level'] = obj;
      }else{
        this['level'] = "";
      }
    },
    project_upload: function(){
      $('#picture').change(this.picture_upload.bind(this));
    },
    picture_upload: function(event){
      var file = event.target.files[0];
      if(file.size > 5 * 1024 * 1024){
        this.errPicture = "图片太大";
        return;
      }else{
        this.errPicture = ""
      }
      var data = new FormData();
      var that = this;
      data.append('file', file);
      data.append('_xsrf', Cookies.get('_xsrf'));
      $.ajax({
        type: "POST",
        url: "/api/attachment",
        cache: false,
        dataType: "json",
        data: data,
        processData: false,
        contentType: false,
        error: function (xhr, textStatus) {
          console.log('xxx')
        },
        success: function (result) {
          if(result.error_code != 0){
            that.picture = "";
            that.errPicture = result.msg;
            that.errRes = result.msg;
            $('#error').modal('show');
          }else{
            that.picture = result.attachment_id;
            that.picture_name = result.name;
            that.picture_path = result.path;
            that.errPicture = "";
          }
        }
      });
    },
    edit_employment: function(id){
      var that = this;
      for(var i=0; i<that.employments.length; i++){
        if(that.employments[i].id == id){
          that.id_emp = id;
          that.company = that.employments[i].company;
          that.title = that.employments[i].title;

          that.is_address_state = that.employments[i].city.parent_id;
          that.set_select_value('address_state', that.employments[i].city.parent_id, that.employments[i].city.parent_name);

          that.city = that.employments[i].city.id;
          that.set_select_value('address_city', that.employments[i].city.id, that.employments[i].city.name);

          that.role = that.employments[i].role.key;
          that.set_select_value('role', that.employments[i].role.key, that.employments[i].role.value);

          that.date01_year = that.formate_date(that.employments[i].start_at, 'yyyy');
          that.set_select_value('date01_year', that.date01_year, that.date01_year);

          that.date01_month = that.formate_date(that.employments[i].start_at, 'MM');
          that.set_select_value('date01_month', that.date01_month, that.date01_month);

          that.date02_year = that.formate_date(that.employments[i].end_at, 'yyyy');
          that.set_select_value('date02_year', that.date02_year, that.date02_year);

          that.date02_month = that.formate_date(that.employments[i].end_at, 'MM');
          that.set_select_value('date02_month', that.date02_month, that.date02_month);

          that.working = that.employments[i].working;
          that.detail = that.employments[i].detail;
        }
      }
    },
    edit_education: function(id){
      var that = this;
      for(var i=0; i<that.educations.length; i++){
        if(that.educations[i].id == id){
          that.id_edu = id;
          that.school = that.educations[i].school;
          that.year_begin = that.formate_date(that.educations[i].start_at, 'yyyy');
          that.set_select_value('school_begin', that.year_begin, that.year_begin);

          that.year_end = that.formate_date(that.educations[i].end_at, 'yyyy');
          that.set_select_value('school_end', that.year_end, that.year_end);

          that.degree = that.educations[i].degree.key;
          console.log('degree', that.educations[i].degree.key, that.educations[i].degree.value);
          that.set_select_value('degree', that.educations[i].degree.key, that.educations[i].degree.value);

          that.area = that.educations[i].area;
          that.detail_edu = that.educations[i].detail;
        }
      }
    },
    edit_project: function(id){
      var that = this;
      for(var i=0; i<that.projects.length; i++){
        if(that.projects[i].id == id){
          that.id_pro = id;
          that.pname = that.projects[i].name;
          that.detail_pro = that.projects[i].detail;
          that.picture = that.projects[i].picture.id;
          that.picture_name = that.projects[i].picture.name;
          that.picture_path = that.projects[i].picture.path;
          that.is_categoryone = that.projects[i].category.parent_id;

          that.category = that.projects[i].category.id;
          that.set_select_value('lb01', that.projects[i].category.parent_id, that.projects[i].category.parent_name);
          that.set_select_value('lb02', that.projects[i].category.id, that.projects[i].category.name);
          that.address = that.projects[i].link;
          that.end_pro = that.formate_date(that.projects[i].end_at, 'yyyy');
          that.set_select_value('end_pro', that.end_pro, that.end_pro);
          var tmp = that.projects[i].skills;
          var sk = $('#select-skills')[0].selectize;
          for(var j=0; j<tmp.length; j++){
            sk.addItem(tmp[j]);
          }
        }
      }
    },
  }
});

var work_company_validict = {
  "company": function(obj){
    if(obj.company.length > 50 || obj.company.length == 0){
      obj.errCompany = "公司名称为1～50个字符";
      return false;
    }else{
      obj.errCompany = "";
    }
  },
  "city": function(obj){
    if(obj.city == ""){
      obj.errCity = "必须选择城市";
      return false;
    }else{
      obj.errCity = "";
    }
  },
  "title": function(obj){
    if(obj.title.length > 50 || obj.title.length == 0){
      obj.errTitle = "职位为1～50个字符";
      return false;
    }else{
      obj.errTitle = "";
    }
  },
  "date": function(obj){
    var d1 = obj.date01.split("-");
    var d2 = obj.date02.split("-");
    var year_value_list = get_list_dict_value(obj.year_list);
    var month_value_list = get_list_dict_value(obj.month_list);

    if($.inArray(d1[0], year_value_list) == -1 || $.inArray(d1[1], month_value_list) == -1
      || $.inArray(d2[0], year_value_list) == -1 || $.inArray(d2[1], month_value_list) == -1){
      obj.errDate = "请选择完整合法日期";
      return false;
    }else{
      obj.errDate = "";
    }
  }
};

var education_validict = {
  "school": function(obj){
    if(obj.school.length > 50 || obj.school.length == 0){
      obj.errSchool = "学校名称为1～50个字符";
      return false;
    }else {
      obj.errSchool = "";
    }
  },
  "degree": function(obj){
    if(obj.degree.length > 50 || obj.degree.length == 0){
      obj.errDegree = "学历为1～50个字符";
      return false;
    }else{
      obj.errDegree = "";
    }
  },
  "area": function(obj){
    if(obj.area.length > 50 || obj.area.length == 0){
      obj.errArea = "专业为1～50个字符";
      return false;
    }else{
      obj.errArea = "";
    }
  },
  "year_edu": function(obj){
    var year_value_list = get_list_dict_value(obj.year_list);
    if($.inArray(obj.year_begin, year_value_list) == -1 || $.inArray(obj.year_end, year_value_list) == -1){
      obj.errDateEdu = "请选择完整合法日期";
      return false;
    }else{
      obj.errDateEdu = ""
    }
  }
};

var project_validict = {
  "pname": function(obj){
    if(obj.pname.length > 50 || obj.pname.length == 0){
      obj.errName = "项目名称为1～50个字符";
      return false;
    }else {
      obj.errName = "";
    }
  },
  "detail_pro": function(obj){
    if(obj.detail_pro.length == 0){
      obj.errDetailPro = "项目描述必输";
      return false;
    }else{
      obj.errDetailPro = "";
    }
  },
  "category": function(obj){
    if(obj.category == ""){
      obj.errCategory = "必须选择分类";
      return false;
    }else{
      obj.errCategory = "";
    }
  }

};
function get_list_dict_value(obj){
  var res = [];
  for(var i=0; i<obj.length; i++){
    res.push(obj[i].value)
  }
  return res;
}

function bind_select_list_option(obj, id, data, vue_meta, please){
  $('#' + id).empty();
  $('#' + id).append('<option value="none" selected>--请选择--</option>');
  //if(please){
  //  //$('#' + id).append($('<option>', {value: 'none', text: '--请选择--'}));
  //  $('#' + id).append('<option value="none" selected>--请选择--</option>');
  //}
  for(var i=0; i<data.length; i++){
    $('#' + id).append($('<option>', {value: data[i].value, text: data[i].text}))
  }
  bind_select_list(obj, id, vue_meta);
}

function bind_select_list(obj, id, vue_meta){
  $(function(){
    $('#' + id).selectlist({
      zIndex: 10,
      onChange: function(){
        obj.check_input_val(id, vue_meta);
      }
    });
  });
}

function bind_data_init(obj){
  bind_select_list_option(obj, 'date01_year', obj.year_list, 'date01_year', true);
  bind_select_list_option(obj, 'date01_month', obj.month_list, 'date01_month', true);
  bind_select_list_option(obj, 'date02_year', obj.year_list, 'date02_year', true);
  bind_select_list_option(obj, 'date02_month', obj.month_list, 'date02_month', true);

  bind_select_list(obj, 'role', 'role');
  // education school
  bind_select_list_option(obj, 'school_begin', obj.year_list, 'year_begin', true);
  bind_select_list_option(obj, 'school_end', obj.year_list, 'year_end', true);
  bind_select_list(obj, 'degree', 'degree');
  // portfolio
  bind_select_list_option(obj, 'end_pro', obj.year_list, 'end_pro', true);
}


function get_category(obj){
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
    error: function (xhr, textStatus) {
    },
    success: function (result) {
      if(result.error_code != 0){
        obj.errRes = result.msg;
        $('#error').modal('show');
      }else{
        obj.cat_all = result.categorys;
        obj.categoryone = $.grep(result.categorys, function(data){
          return data.pid == 0;
        });

        var data = [];
        for(var i=0; i<obj.categoryone.length; i++){
          data.push({value: obj.categoryone[i].category_id, text: obj.categoryone[i].name})
        }
        bind_select_list_option(obj, 'lb01', data, 'is_categoryone', true);
      }
    }
  });
}

function get_address(obj){
  $.ajax({
    type: "GET",
    url: "/api/address",
    cache: false,
    dataType: "json",
    data: {
      _xsrf: Cookies.get("_xsrf"),
      address_id: 0,
      t: 'all',
      cid: 1
    },
    error: function (xhr, textStatus) {
    },
    success: function (result) {
      if(result.error_code != 0){
        obj.errRes = result.msg;
        $('#error').modal('show');
      }else{
        obj.add_all = result.addresses;
        obj.address_state = $.grep(obj.add_all, function(data){
          return data.pid == 1;
        });

        var data = [];
        for(var i=0; i<obj.address_state.length; i++){
          data.push({value: obj.address_state[i].address_id, text: obj.address_state[i].name})
        }
        bind_select_list_option(obj, 'address_state', data, 'is_address_state', true);

      }
    }
  });
}

function bind_skills(obj){
  var arr = $("#project-skills").val().split(",");
  var arr1 = [];
  for(var i=0;i<arr.length;i++){
    arr1.push({value: arr[i], text:arr[i]});
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
