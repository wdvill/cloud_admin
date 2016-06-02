$.i18n().then(function(data){
  window['CODE'] = data.CODE;
  window['COMMONS'] = data.COMMONS;

  var findcontract_list =new Vue({
    el:"#body",
    data:{
      contracts:[],
      teams:[],
    },
    ready:function(){
      var that = this;
      var contract = [];
      Service.get('Myproject').pro_contract({status:"all"}).success(function(result){
        for (var i = 0; i < result.contracts.length; i++) {
            if(result.contracts[i].status=='carry'||result.contracts[i].status=='dispute'||result.contracts[i].status=='finish'||result.contracts[i].status=='service'||result.contracts[i].status=='carry' || result.contracts[i].status=='pause'){
              result.contracts[i].status_value = window['COMMONS']._contract_status[result.contracts[i].status]
              contract.push(result.contracts[i])
            }
            
          }
        that.contracts = contract;
      });
      Service.get('ContractService').team_contract().success(function(result){
        that.teams = result.teams;
      });
    },
    methods:{
      searchcontract:function(){
        if(KeyCode = 13){
          var that = this;
          that.contracts = [];
          Service.get('Myproject').pro_contract({status:"all",}).success(function(result){
            for(var i = 0; i<result.contracts.length;i++){
              if(result.contracts[i].name == that.keyword){
                  that.contracts.push(result.contracts[i]);
              }
            };
            if(that.keyword == ''){
              alert();
            };
          });
        }
      },
      teatcontract:function(){
        var that = this;
        Service.get('ContractService').team_contract({team_id:this.team_id}).success(function(result){
            that.roles = result.roles;
        });
      },
    },
  })
})