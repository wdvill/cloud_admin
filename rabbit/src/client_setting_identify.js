import Vue from 'vue'
import $ from 'jquery'
import validate from './utils/validate'
import alert from './components/alert.vue'
import userService from './service/user_service'

Vue.config.delimiters = ['{[', ']}']
/* eslint-disable no-new */
new Vue({
  el: '#body',
  data: {
    name: '',
    id_number: '',
    error_msg: ''
  },
  ready () {
    validate.RegEventBlur($('#form-verify'))
  },
  components: {
    alert
  },
  methods: {
    verify () {
      if (!validate.validateForm($('#form-verify'))) {
        return
      }
      let data = {
        name: this.name,
        id_number: this.id_number
      }
      userService.add_user_verify(data).success((result) =>{
        if (result.error_code === 0) {
          window.location.href = '/freelancers/settings/identity'
        } else {
          $('#alert').modal('show')
          this.error_msg = result.msg
        }
      })
    }
  }
})
