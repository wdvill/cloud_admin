import Vue from 'vue'
import $ from 'jquery'
import init from './page/init.js'
import userService from './service/user_service'

Vue.config.delimiters = ['{[', ']}']
Vue.use(init)
/* eslint-disable no-new */
new Vue({
  el: '#container',
  data: {
    rate: 'day'
  },
  ready () {
    userService.get_notify_setting().success((result) =>{
      if (result.error_code === 0 && result.data.length > 0) {
        for (let i = 0; i < result.data.length; i++) {
          if (result.data[i].mtype === 'recomm_rate' && result.data[i].rate !== '') {
            this.rate = result.data[i].rate
          }
          $('input[data-type=' + result.data[i].mtype + ']').attr('checked', result.data[i].is_send)
        }
      }
    })
  },
  methods: {
    notify_setting (event) {
      let flag = true
      if (!$(event.target).is(':checked')) {
        flag = false
      }
      let data = {
        mtype: $(event.target).attr('data-type'),
        is_send: flag,
        rate: this.rate
      }
      userService.add_notify_setting(data)
    },
    notify_setting_rate () {
      let is_send = true
      if (!$('input[data-type="recomm_rate"]').is(':checked')) {
        is_send = false
      }
      userService.add_notify_setting({mtype: 'recomm_rate', is_send: is_send, rate: this.rate})
    }
  }
})
