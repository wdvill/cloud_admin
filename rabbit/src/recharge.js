import Vue from 'vue'
import $ from 'jquery'
import validate from './utils/validate'
import accountService from './service/account_service'

Vue.config.delimiters = ['{[', ']}']
/* eslint-disable no-new */
new Vue({
  el: 'body',
  data: {
    accounts: [],
    price: ''
  },
  ready () {
    let $this = this
    validate.RegEventBlur($('#form-recharge'))
    accountService.get_account_list().success((result) =>{
      if (result.error_code === 0) {
        $this.accounts = result.accounts
      }
    })
  },
  methods: {
    checkType (event) {
      $('.recharge-box').removeClass('active')
      $(event.target).parent().addClass('active')
      $(event.target).parent().parent().addClass('active')
    },
    recharge () {
      if (!validate.validateForm($('#form-recharge'))) {
        return
      }
      if (isNaN(this.price) || this.price.split('.').length > 2 || this.price.indexOf('-') > 0) {
        $('div[data-name = "price"]').find('.errorMsg').html('充值金额不正确')
        $('div[data-name = "price"]').show()
      }
      let data = {
        amount: this.price
      }
      accountService.update_account_recharge(data).success((result) =>{
        if (result.error_code === 0) {
          window.location.href = result.url
        }
      })
    }
  }
})
