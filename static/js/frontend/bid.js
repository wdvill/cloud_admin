Vue.config.delimiters = ['{[', ']}'];
var ve = new Vue({
  el: "#body",
  data: {
    jobId:"",
    options:[
      {"val":5,"txt":"一周以内"},{"val":4,"txt":"一个月以内"},{"val":3,"txt":"1到3个月"},
      {"val":2,"txt":"3到6个月"},{"val":1,"txt":"6个月以上"}
    ],
    bidPrice:"",
    calculatePrice:"",
    bidMessage:"",
    bidEndTime:"",
    bidAttachment:"未选择任何文件。",
    attachmentId:""
  },
  ready: function() {
    YWORK.RegEventBlur($("#form-bid"));
  },
  methods: {
    calculate:function(){
      if(!isNaN(this.bidPrice) && this.bidPrice.split(".").length<3 && this.bidPrice.indexOf("-")==-1){
        this.calculatePrice = (this.bidPrice * 0.9).toFixed(2);
        $("div[data-name='bidPrice']").hide();
      }else{
        $("div[data-name='bidPrice']").show().find(".errorMsg").html("请输入正确的报价");
        this.calculatePrice = "";
      }    
    },
    attachment:function(){
      var $this = this;
      var formData = new FormData();
      var f = $("#files")[0].files[0];
      if(f.size > 1024 * 1024 * 5){
        alert("附件大小不超过5M");
        return;
      }
      formData.append('file', f);
      formData.append('_xsrf', Cookies.get("_xsrf"));
      formData.append('t', "proposal");
      $.ajax({
        url: "/api/attachment",
        type: 'post',
        dataType: 'json',
        data:formData,
        processData: false,
        contentType: false,
        success:(function(json){
          if(json.error_code==0){
            $this.attachmentId = json.attachment_id;
            $this.bidAttachment = json.name;
          }          
        })
      });
    },
    checkSelect:function(){
      if(this.bidEndTime == ""){
        $("div[data-name='bidEndTime']").show().find(".errorMsg").html("请选择预计完成时间");
        return false;
      }else{
        $("div[data-name='bidEndTime']").hide().find(".errorMsg").html("");
        return true;
      }
    },
    showDialog:function(){
      if(YWORK.Validator.validateForm($("#form-bid"))){
        $('#myModal').modal('show');
      }
    },
    commitBid:function(type){
      if(type=='fixed' && !$("#commitCheck").is(':checked')){
        return ;
      }
      if(!YWORK.Validator.validateForm($("#form-bid"))){
        return ;
      }
      var data = {
        job_id:this.jobId,
        amount:this.bidPrice,
        duration:this.bidEndTime,
        message:this.bidMessage,
        attachment_id:this.attachmentId
      };
      Service.get("BidService").bid(data).success(function(result){
        if(result.error_code==0){
          location.href="/freelancers/proposal";
        }else{
          alert(result.msg);
        } 
      });
    }
  }
});