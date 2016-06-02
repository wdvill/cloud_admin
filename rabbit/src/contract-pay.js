import Vue from 'vue'
import $ from 'jquery'
import datetime from './filters/datetime'
import Cookies from 'js-cookie'

Vue.config.delimiters = ['{[', ']}']
Vue.use(datetime)

$.ajaxPrefilter(function (options, originalOptions, jqXHR) {
  try {
    options.data = $.param($.extend(originalOptions.data, { '_xsrf': Cookies.get('_xsrf') }))
  } catch (e) {
    console.log(e)
  }
})

var vue = new Vue({
  el: '#contract-pay',
  data: {
    contract_id: '',
    ptype: '',
    trade_no: '',
    paystatus: false,
    contract: {},
    records: [],
    margin: ''
  },
  ready () {
    this.contract_id = location.pathname.split('/')[2]
    this.ptype = location.pathname.split('/')[3]
    this.trade_no = location.pathname.split('/')[4]
    let that = this
    $.getJSON('/api/order/pay', {'contract_id': this.contract_id, 'ptype': this.ptype, 'trade_no': this.trade_no}, function (data) {
      if (data.error_code === 0) {
        that.contract = data.contracts
        that.records = data.records
        $.getJSON('/api/margin/basic', function (data) {
          if (data.error_code === 0) {
            that.margin = data.margin
            if (that.margin >= that.contract.amount) {
              that.paystatus = false
            } else {
              that.paystatus = true
            }
          }
        })
      }
    })
  },
  methods: {
    change_paymethod_true: function () {
      this.paystatus = true
    },
    change_paymethod_false: function () {
      if (this.margin >= this.contract.amount) {
        this.paystatus = false
      }
    },
    pay_amount: function () {
      if (this.paystatus === false) {
        $.post('/api/order/pay', {'contract_id': this.contract_id, 'ptype': this.ptype, 'trade_no': this.trade_no}, function (data) {
          if (data.error_code === 0) {
            window.location.href = '/clients/jobs/' + data.job_id + '#hire'
          } else {
            alert(data.msg)
          }
        }, 'json')
      } else {
        $.post('/api/margin/deposit', {'amount': this.contract.amount, 'dtype': 'contract', 'contract_id': this.contract.id, 'trade_no': this.trade_no}, function (data) {
          if (data.error_code === 0) {
            window.location.href = data.url
          } else {
            alert(data.msg)
          }
        }, 'json')
      }
    }
  }
})

vue.$set('test', 'll')
