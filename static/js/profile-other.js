Vue.config.delimiters = ['{[', ']}'];

function Profile() {
  this.con = null;
  this.get_address();
}


Profile.prototype.get_address = function(){
  var that = this;
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
        that.con.allData = result.addresses;
        var states = $.grep(that.con.allData, function(data){
          return data.pid == 1;
        });


        $('#country').empty();
        $('#country').append('<option value="" >--请选择--</option>');

        for(var i=0; i<states.length; i++){
          $('#country').append($('<option>', {value: states[i].address_id, text: states[i].name}))
        }
      }
      that.init();
    }
  });
}

Profile.prototype.init = function() {
  var that = this;
  $('#country').selectlist({
    zIndex: 10,
    onChange: function() {
      that.check_country();
    }
  });
};

Profile.prototype.check_country = function() {
  this.con.country = $("input[name='country']").val();
  this.bind_city(this.con.country);
  validict['country'](this.con);
};

Profile.prototype.bind_city = function(countryId) {
  var data = this.con.citys = $.grep(this.con.allData, function(data){
    return data.pid == countryId;
  });

  $('#city').empty();
  $('#city').append('<option value="">--请选择--</option>');
  for(var i=0; i<data.length; i++){
    $('#city').append($('<option>', {value: data[i].address_id, text: data[i].name}))
  }
  $('#city').selectlist({
    zIndex: 9,
  });
};

Profile.prototype.create_other = function() {
  var that = this;
  var con = this.con;
  var flag = true;
  for(var x in validict){
    if(validict[x](con) == false){
      flag = false;
    }
  }
  if(!flag){
    return;
  }
  $.ajax({
    type: "post",
    url: "/api/user/other/create",
    cache: false,
    dataType: "json",
    data: {
      address: con.address,
      city: con.city,
      country: con.country,
      postcode: con.postcode,
      amount: con.amount,
      _xsrf: Cookies.get("_xsrf")
    },
    error: function (xhr, textStatus) {
    },
    success: function (json) {
      if(json.error_code != 0){
        alert(CODE[json.error_code]);
      }else{
        location.href="/users/profile/step/complete";
      }
    }
  });
};

var profile = new Profile();

var v = new Vue({
  el: "#body",
  data: {
    amount: "",
    actual_amount: "",
    address: "",
    city: "",
    country: "",
    postcode: "",

    allData:[],
    citys:[],

    errAddress: "",
    errCity: "",
    errCountry: "",
    errPostcode: "",
    errPhone: "",
    errAmount: "",
    errActualAmount: ""
  },
  ready: function() {
    $.i18n();
  },
  created: function() {
    profile.con = this;
  },
  methods: {
    save_go_on: function() {
      profile.create_other();
    },
    prev_step: function() {
      location.href="/users/profile/step/3";
    },
    validate: function(val) {
      validict[val](this);
    }
  },
  watch: {
    amount: function(val, old) {
      var v = filterFloat(val);
      if(v == false){
        this.errAmount = "请输入正确金额";
      }else{
        this.actual_amount = (v * 0.9).toFixed(2);
        this.errAmount = "";
      }
    },
    actual_amount: function(val, old) {
      var v = filterFloat(val);
      if(v == false){
        this.errActualAmount = "请输入正确金额";
      }else{
        this.amount = (v / 0.9).toFixed(2);
        this.errActualAmount = "";
      }
    }
  }
});

function filterFloat(value){
  if(/^(\-|\+)?([0-9]+(\.[0-9]+)?|Infinity)$/.test(value)){
    return Number(value);
  }
  return false;
}

var validict = {
  "country": function(con) {
    if(con.country == "none" || con.country == ""){
      con.errCountry = "请选择国家";
      return false;
    }else{
      con.errCountry = "";
    }
  },
  "address": function(con) {
    if(con.address == ""){
      con.errAddress = "请输入地址";
      return false;
    }else if(con.address.length > 90){
      con.errAddress = "地址在90个字以内";
      return false;
    }else{
      con.errAddress = "";
    }
  },
  "city": function(con) {
    if(con.city == "none" || con.city == ""){
      con.errCity = "请选择城市";
      return false;
    }else{
      con.errCity = "";
    }
  },
  "postcode": function(con) {
    var num = /^\d*$/;
    if(con.postcode == ""){
      con.errPostcode = "此字段不能为空";
      return false;
    }
    if(!num.test(con.postcode)){
      con.errPostcode = "请输入数字";
      return false;
    }else{
      con.errPostcode = "";
    }
  },
  "amount": function(con) {
    if(con.amount == ""){
      con.errAmount = "此字段不能为空";
      return false;
    }
    var v = filterFloat(con.amount);
    if(v == false){
      con.errAmount = "请输入正确金额";
    }else{
      con.actual_amount = (v / 0.9).toFixed(2);
      con.errAmount = "";
    }
  },
  "actual_amount": function(con) {
    if(con.actual_amount == ""){
      con.errActualAmount = "此字段不能为空";
      return false;
    }
    var v = filterFloat(con.actual_amount);
    if(v == false){
      con.errActualAmount = "请输入正确金额";
    }else{
      con.amount = (v / 0.9).toFixed(2);
      con.errActualAmount = "";
    }
  }
};
