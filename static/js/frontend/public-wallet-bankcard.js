Vue.config.delimiters = ['{[', ']}'];

Vue.filter('formatAccount', YWORK.formatBank)

var walletBankcard = new Vue({
  el: "#body",
  data: {
    addid: true,
    BankType: [],
    cards: [],
  },
  ready: function() {
    YWORK.RegEventBlur($("#add-bankcard"));
    var that = this;
    var addid = true;

    $.i18n().then(function(data) {
      window['CODE'] = data.CODE;
      window['COMMONS'] = data.COMMONS;
      Service.get('UserService').bank_type().success(function(result) {
        that.BankType = result.banks
      });
      Service.get('UserService').bank_list().success(function(result) {
        that.cards = result.cards;
      });
    })
    console.log(addid);
  },

  methods: {
    add_bankcard: function() {
      $("#add-bankcard").modal('show');
    },
    save_bankcard: function() {
      if (!YWORK.Validator.validateForm($("#add-bankcard"))) {
        return;
      }
      var that = this;
      var data = {
        code: that.code,
        card_no: that.card_no
      }
      Service.get('UserService').save_card(data).success(function(result) {
        if (result.error_code == 0) {
          $("#add-bankcard").modal('hide');
          location.reload();
        }
      });
    },
    del_item: function(index, arr) {
      this.origin_arr = arr;
      this.index = index;
      $("#card_del").modal('show');
    },
    do_del_item: function(card_id) {
      Service.get("UserService").delete_card({
        card_id: card_id
      }).success(function(result) {
        if (result.error_code == 0) {
          location.reload();
        }
      });
    }

  }
})