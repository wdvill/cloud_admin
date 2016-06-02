 $.i18n().then(function(data){
  window['CODE'] = data.CODE;
  window['COMMONS'] = data.COMMONS;

  var creatClient = new Vue({
    el:"#body",
    data:{
      global:{},
      clientName:"",
    },
    methods:{
      creatClient:function(){
        var clientName = this.clientName;
        if(clientName==""){return;}
        var error_code;
          Service.get('client').creat_client({name:clientName}).success(function(result){
              if(result.error_code != 0){
                alert("需求者已创建!");
              }else{
                window.location.href="/clients/jobs";
              }
          });
      }
    }
  })

})