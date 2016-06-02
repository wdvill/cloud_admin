//设置时薪 邮编
Vue.config.delimiters = ['{[', ']}'];

var t = new Vue({
  el: "#body",
  data:{
    profile:{},
    amount:"",
    address_id:"",
    address_pid:"",
    prarent_address:[],//地址列表china    Service.get('CommonService')
    child_address:[],//
  },
  ready: function() {
    var that = this;
    $.i18n().then(function(data){
      window['CODE'] = data.CODE;
      window['COMMONS'] = data.COMMONS;
  	  YWORK.RegEventBlur($("#form-other"));
      Service.get('CommonService').address({address_id:1}).success(function(result){
          that.prarent_address = result.addresses;
      });
      Service.get('ResumeService').get_profile().success(function(result){
            that.profile = result.profile;
            if(result.profile.hourly!='' && result.profile.hourly!='0.0'){
              that.amount = result.profile.hourly;
            }
            if(result.profile.location){
              that.address_id = result.profile.location.location_id;
              that.address_pid = result.profile.location.parent_id;
              Service.get('CommonService').address({address_id:result.profile.location.parent_id}).success(function(result){
                  that.child_address = result.addresses;
              })
            }
        });
    })
  },
  created: function(){

  },
  computed: {
    // 一个计算属性的 getter
    actual_amount: function () {
      // `this` 指向 vm 实例
      if (this.amount!=''){
        return (this.amount * 0.9).toFixed(2);
      } else {
        return ''
      }
    }
  },
  methods:{
    select_child_address:function(){
      var that = this;
      Service.get('CommonService').address({address_id:that.address_pid}).success(function(result){
          that.child_address = result.addresses;
      })
    },
    prev_step:function(){
        window.location.href="/users/profile/step/3";
    },
    setNum: function() {
      this.amount = Math.round(this.amount * 100) / 100;
    },
    save_other_profile:function(){
      if(!YWORK.Validator.validateForm($("#form-other"))){
        return ;
      }
      var that = this;
        var data={
            amount:that.amount,
            location:that.address_id,
            address:that.profile.address,
            postcode:that.profile.postcode
        };
        Service.get('ResumeService').post_other_profile(data).success(function(result){
              if(result.error_code == 0){
                  window.location.href="/find-work-home";
              }
        });
    }
  }
})
