$.i18n().then(function(data){
  window['CODE'] = data.CODE;
  window['COMMONS'] = data.COMMONS;

  var pro_detail = new Vue({
    el:"#body",
    data:{
      global:{},
      job:{},
      other:[],
      show_alert:false,
    },
    ready:function(){
      var that = this;
      var data={job_id:window.location.pathname.substr(-16,16)};
      that.global  = COMMONS;
      Service.get('Myproject').pro_details(data).success(function(result){
            that.job = result.job;
            that.other = result.other;
      });
    },
    methods:{
      collect:function(){
        Service.get('Myproject').pro_details({
          job_id:this.job.id}).success(function(result){
          alert('已收藏');
        });
      },
    }
  })
})