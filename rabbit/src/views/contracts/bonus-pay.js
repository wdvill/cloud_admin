import Vue from 'vue'
import $ from 'jquery'
import YWORK from '../../utils/ywk.js'
import strapAlert from '../../components/strap_alert.vue'

require('../../assets/sass/views/contracts/pay.scss')
Vue.config.delimiters = ['{[', ']}']

new Vue({
  el: 'body',
  data: {
    paystatus: false,
    bonus: {},
    // 奖金支付交易号
    trade_no: '',
    margin: '',
    // 错误信息
    errMsg: '',
    // 是否显示提示
    showAlert: false
  },
  ready () {
    let pathname = location.pathname.split('/')
    this.contract_id = pathname[2]
    // 奖金支付
    if (pathname.length > 4) {
      this.trade_no = pathname[4]
      // 获取奖金支付参数
      YWORK.getJson('/api/contract/bonus', {trade_no: this.trade_no}, 'application/json').success((result) =>{
        if (result.error_code === 0) {
          this.bonus = result.bonus
          // 获取用户余额
          $.getJSON('/api/margin/basic', (data) => {
            if (data.error_code === 0) {
              this.margin = data.margin
              if (this.margin >= this.bonus.amount) {
                this.paystatus = false
              } else {
                this.paystatus = true
              }
            }
          })
        } else {
          this.errMsg = result.msg
          this.showAlert = true
        }
      })
    }
  },
  methods: {
    change_paymethod_true () {
      this.paystatus = true
    },
    change_paymethod_false () {
      if (this.margin >= this.bonus.amount) {
        this.paystatus = false
      }
    },
    pay_amount () {
      if (this.paystatus === false) {
        YWORK.postJson('/api/order/pay', {'contract_id': this.contract_id, 'trade_no': this.trade_no, 'ptype': 'bonus'}, 'application/json').success((data) => {
          console.log(data)
          if (data.error_code === 0) {
            console.log(data.error_code)
            window.location.href = '/freelancers/contracts/' + this.contract_id
          } else {
            this.errMsg = data.msg
            this.showAlert = true
          }
        })
      } else {
        YWORK.postJson('/api/margin/deposit', {'amount': this.bonus.amount, 'dtype': 'bonus', 'contract_id': this.contract_id, trade_no: this.trade_no}, 'application/json').success((data) => {
          if (data.error_code === 0) {
            console.log(data)
            window.location.href = data.url
          } else {
            this.errMsg = data.msg
            this.showAlert = true
          }
        })
      }
    }
  },
  components: {
    strapAlert
  }
})
