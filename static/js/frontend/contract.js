Vue.config.delimiters = ['{[', ']}'];
var ve = new Vue({
  el: "body",
  data: {
    contract_id:"",
    contract:{},
    job:{},
    stones:[],
    freelancer:{},
    client:{},
    questions:[],
    question_id:"",
    reason:""
  },
  ready: function() {
    var $this = this;
    $this.contract_id = location.href.split("/")[location.href.split("/").length-1];
    var data = {
      contract_id:$this.contract_id
    };
    Service.get("ContractService").select_contract(data).success(function(result){
      if(result.error_code==0){
        if(result.contracts.length>0){
          $this.contract = result.contracts[0];
          $this.contract.start_at = $this.contract.start_at.substring(0,11);
          $this.contract.create_at = $this.contract.create_at.substring(0,11);
          $this.job = result.contracts[0].job;
          $this.stones = result.contracts[0].stones;
          for(var i=0;i<$this.stones.length;i++){
            $this.stones[i].end_at = $this.stones[i].end_at.substring(0,11);
          }
          $this.freelancer = result.contracts[0].user.freelancer;
          $this.client = result.contracts[0].user.client;
        }
      }else{
        alert(result.msg);
      }
    });
    Service.get("CommonService").question({qtype:"contract_revoke"}).success(function(result){
      if(result.error_code==0){
        $this.questions = result.questions;
      }
    });
  },
  methods: {
    revoke:function(){
      if(this.question_id==""){
        return;
      }
      var data={
        contract_id:this.contract_id,
        status:"revoke",
        question_id:this.question_id,
        reason:this.reason
      };
      Service.get("ContractService").update_contract(data).success(function(result){
        if(result.error_code==0){

        }else{
          alert(result.msg);
        }
      });
    }
  }
});