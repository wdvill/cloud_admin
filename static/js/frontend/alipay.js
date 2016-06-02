Vue.config.delimiters = ['{[', ']}'];
var ve = new Vue({
  el: "#body",
  data: {
    name: "",
    alipay_number: "", //支付宝账号
    id_number: "" //身份证号
  },
  ready: function() {
    this.getProfile();
  },
  methods: {
    getProfile: function() {
      var $this = this;
      Service.get("ResumeService").get_profile().success(function(result) {
        $this.name = result.profile.name || result.profile.freelancer.name;
        if (result.profile.alipay) {
          $this.alipay_number = YWORK.formatAccount(result.profile.alipay);
        }
        $this.id_number = result.profile.id_number;
      });
    },
    createAlipay: function() {
      var $this = this;
      var data = {
        "alipay": $("#alipay").val()
      };
      Service.get("UserService").create_alipay(data).success(function(result) {
        if (result.error_code == 0) {
          $(".modal-backdrop").remove();
          $("#add-alipay").hide();
          $this.getProfile();
        } else {
          YWORK.alert('danger', '错误提示', result.msg);
        }
      });
    },
    /* 添加时清空之前的记录 */
    addNew: function() {
      $("#alipay").val('');
    },
    /*删除绑定的支付宝*/
    do_del_item: function() {
      Service.get("UserService").delete_alipay().success(function(result) {
        if (result.error_code == 0) {
          location.reload();
        }
      });
    }
  }
});