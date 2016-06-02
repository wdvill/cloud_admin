import Vue from 'vue'
import $ from 'jquery'
import validate from './utils/validate'
import commonService from './service/common_service'
import accountService from './service/account_service'

Vue.config.delimiters = ['{[', ']}']
/* eslint-disable no-new */
new Vue({
  el: 'body',
  data: {
    accounts: [],
    wait: 60,
    interval: '',
    account: '',
    price: '',
    phone: '',
    code: '',
    type: ''
  },
  ready () {
    let $this = this
    validate.RegEventBlur($('#form-withdrawals'))
    accountService.get_account_list().success((result) =>{
      if (result.error_code === 0) {
        for (let i = 0; i < result.accounts.length; i++) {
          if (result.accounts[i].bank === 'alipay') {
            result.accounts[i].bank = '支付宝'
          }
        }
        $this.accounts = result.accounts
      }
    })
  },
  methods: {
    timeClock () {
      $('span[vcode = clock-vcode]').html(this.wait + '秒后重新发送')
      this.wait--
      if (this.wait === 0) {
        this.wait = 60
        clearInterval(this.interval)
        $('span[vcode = clock-vcode]').removeClass('btn-gray')
        $('span[vcode = clock-vcode]').addClass('btn-primary')
        $('span[vcode = clock-vcode]').html('重新发送')
      }
    },
    sendvcode () {
      let $this = this
      if ($this.wait < 60) {
        return
      }
      commonService.verifycode({register: 'true'}).success((result) =>{
        if (result.error_code === 0) {
          $this.code = result.vcode
          $this.interval = setInterval($this.timeClock, 1000)
          $('span[vcode = clock-vcode]').removeClass('btn-primary')
          $('span[vcode = clock-vcode]').addClass('btn-gray')
        }
      })
    },
    withdraw () {
      if (this.account === '') {
        $('div[data-name = "account"]').find('.errorMsg').html('请选择提现账户')
        $('div[data-name = "account"]').show()
      }
      if (!validate.validateForm($('#form-withdrawals'))) {
        return
      }
      if (isNaN(this.price) || this.price.split('.').length > 2 || this.price.indexOf('-') > 0 || this.price < 100) {
        $('div[data-name = "price"]').find('.errorMsg').html('提现金额不能低于100')
        $('div[data-name = "price"]').show()
        return
      }
      if (Number($('input[name = "code"]').val()) !== this.code) {
        $('div[data-name = "code"]').find('.errorMsg').html('验证码不正确')
        $('div[data-name = "code"]').show()
        return
      }

      if ($('select option:selected').text() === 'alipay') {
        this.type = 'alipay'
      } else {
        this.type = 'bank'
      }
      let data = {
        amount: this.price,
        account: this.account,
        type: this.type,
        code: this.code
      }
      accountService.update_account_withdraw(data).success((result) =>{
        if (result.error_code !== 0) {
          alert(result.msg)
        } else {
          let htmlTpl = `
            <div class="col-xs-3 clear-left yzj-top-distance50 recharge-success"></div>
            <div class="col-xs-9 yzj-top-distance70 yzj-size-16">
              <h4 class="text-muted yzj-height30">您的提现申请已提交，将在3个工作日内到账。届时会有消息通知，请耐心等待</h4>
              <p class="yzj-top-distance15">提现金额 : ${result.amount}元 </p>
              <p class="yzj-top-distance15">当前余额 : <span class="text-warning">${result.balance}</span>元</p>
              <div class="yzj-top-distance40">
                <div class="col-xs-4 clear-left">
                  <a href="/freelancers/settings/account" class="btn btn-default btn-block">查看账户信息</a>
                </div>
                <div class="col-xs-4 clear-left">
                  <a href="/freelancers/settings/withdrawal" class="btn btn-primary btn-block">继续提现</a>
                </div>
              </div>
            </div>
            <div class="clearfix"></div>`
          $('.yzj-box').html(htmlTpl)
        }
      })
    }
  }
})
