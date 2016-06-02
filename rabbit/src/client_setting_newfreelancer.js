import Vue from 'vue'
import $ from 'jquery'
import alert from './components/alert.vue'
import userService from './service/user_service'

Vue.config.delimiters = ['{[', ']}']
/* eslint-disable no-new */
new Vue({
  el: '#body',
  data: {
    error_msg: ''
  },
  components: {
    alert
  },
  methods: {
    commit () {
      userService.add_freelancer().success((result) =>{
        if (result.error_code === 0) {
          window.location.href = '/find-work-home'
        } else {
          $('#alert').modal('show')
          this.error_msg = result.msg
        }
      })
    }
  }
})
