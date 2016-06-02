Vue.config.delimiters = ['{[', ']}'];
var ve = new Vue({
  el: "#layout",
  data: {
    records:[],
    count:2,
    pageObject:{itemsCount:0,pageNo:1,pageSize:10},
    cards:"",
    alipay:"",
    id_num:"",
    margin:0,
    withdraw:0
  },
  ready: function() {
    var that = this;
    that.query_work_list();
    Service.get('accountService').get_account_basic().success(function(result){
      that.margin = result.margin;
      that.withdraw = result.withdraw;
    });
    Service.get('UserService').bank_list().success(function(result){
      that.cards = result.cards.length;
    });
    Service.get("ResumeService").get_profile().success(function(result){
      that.id_num = result.profile.id_number;
      if(result.profile.alipay!=""){
        that.alipay = "已绑定";
      }else{
        that.alipay = "未绑定";
      }
    });
  },
  methods: {
    withdrawal:function(){
      if(this.id_num == ""){
        $(".modal").modal("show");
      }else{
        window.location.href = "/freelancers/settings/withdrawal";
      }
    },
    query_work_list:function(){
      var that = this;
      var data={
        pagenum:that.pageObject.pageNo,
        pagesize:that.pageObject.pageSize,
      }
      Service.get('UserService').account_records(data).success(function(result){
        /*for(var i=0;i<result.records.length;i++){
          result.records[i].create_at = new Date((result.records[i].create_at)*1000).format('yyyy-MM-dd hh:mm:ss');
        }*/
        that.records = result.records;
        that.pageObject = {itemsCount:result.count,pageNo:data.pagenum,pageSize:data.pagesize}
      });
    },
  }
});

Date.prototype.format = function(format){
  /*
  * format="yyyy-MM-dd hh:mm:ss";
  */
  var o = {
    "M+" : this.getMonth() + 1,
    "d+" : this.getDate(),
    "h+" : this.getHours(),
    "m+" : this.getMinutes(),
    "s+" : this.getSeconds(),
    "q+" : Math.floor((this.getMonth() + 3) / 3),
    "S" : this.getMilliseconds()
  }
   
  if (/(y+)/.test(format)){
    format = format.replace(RegExp.$1, (this.getFullYear() + "").substr(4- RegExp.$1.length));
  }
   
  for (var k in o){
    if (new RegExp("(" + k + ")").test(format)){
      format = format.replace(RegExp.$1, RegExp.$1.length == 1? o[k]: ("00" + o[k]).substr(("" + o[k]).length));
    }
  }
  return format;
}