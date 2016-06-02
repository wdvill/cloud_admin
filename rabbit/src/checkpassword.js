import Vue from 'vue'
import $ from 'jquery'
import validate from './utils/validate'
import alert from './components/alert.vue'
import error from './components/common/error_div.vue'
import commonService from './service/common_service'

Vue.config.delimiters = ['{[', ']}']
  /* eslint-disable no-new */
new Vue({
  el: 'body',
  data: {
    pwd: '',
    error_msg: ''
  },
  ready () {
    $('#left a').attr('href', 'javascript:;')
    validate.RegEventBlur($('#form-verify-pwd'))
  },
  components: {
    alert,
    error
  },
  methods: {
    checkpwd (type) {
      if (!validate.validateForm($('#form-verify-pwd'))) {
        return
      }
      commonService.checkpwd({
        password: this.pwd
      }).success((result) => {
        if (result.error_code === 0) {
          if (type === 'c') {
            window.location.href = '/clients/settings'
          } else {
            window.location.href = '/settings'
          }
        } else {
          $('#alert').modal('show')
          this.error_msg = '密码错误'
        }
      })
    }
  }
})
