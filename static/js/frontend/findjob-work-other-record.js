 $.i18n().then(function(data){
    window['CODE'] = data.CODE;
    window['COMMONS'] = data.COMMONS;
    var ProfileEdit = new Vue({
      el: "#body",
      data:{
          profile:{},
          global:{},
          portfolios:[],
          employments:[],
          educations:[],
      },
      ready:function(){
        var that  = this;
        that.global = COMMONS;
        Service.get('ResumeService').get_profile().success(function(result){
              that.profile = result.profile;
          });
        Service.get('ResumeService').get_employment().success(function(result){
              that.employments = result.employments;
        })
        Service.get('ResumeService').get_portfolio().success(function(result){
                that.portfolios = result.portfolios;
        });
        Service.get('ResumeService').get_education().success(function(result){
                that.educations = result.educations;
        });
      }
    })
})