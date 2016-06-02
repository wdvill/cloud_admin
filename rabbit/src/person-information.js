import Vue from 'vue'
import $ from 'jquery'
import alert from './components/alert.vue'
import validate from './utils/validate'
import userService from './service/user_service'
import commonService from './service/common_service'

Vue.config.delimiters = ['{[', ']}']
/* eslint-disable no-new */
new Vue({
  el: '#layout',
  data: {
    unedit: true,
    unedit2: true,
    profile: {},
    pemail: '',
    pname: '',
    prarent_address: [],
    child_address: [],
    address_pid: '',
    location_id: ''
  },
  ready () {
    this.get_profile()
    this.get_address()
  },
  components: {
    alert
  },
  methods: {
    get_profile () {
      userService.get_user_profile().success((result) =>{
        if (result.error_code === 0) {
          this.profile = result.profile
          if (this.profile.logo === '') {
            this.profile.logo = '/static/images/default-img03.png'
          }
        }
      })
    },
    edit (profile) {
      this.unedit = false
    },
    update_ca () {
      if (!validate.validateForm($('#form-client-info'))) {
        return
      }
      let data = {
        name: this.pname,
        email: this.pemail
      }
      userService.update_user_profile(data).success((result) =>{
        if (result.error_code === 0) {
          this.profile = result.profile
          this.unedit = true
          this.get_profile()
        }
      })
    },
    edit2 (profile) {
      this.unedit2 = false
    },
    get_address () {
      let $this = this
      commonService.address({address_id: 1}).success((result) =>{
        if (result.error_code === 0) {
          $this.prarent_address = result.addresses
        }
      })
    },
    select_child_address () {
      let $this = this
      commonService.address({address_id: $this.address_pid}).success((result) =>{
        if (result.error_code === 0) {
          $this.child_address = result.addresses
        }
      })
    },
    update_contact () {
      if (!validate.validateForm($('#form-client-info'))) {
        return
      }
      let data = {
        location_id: this.location_id,
        address: this.t_address,
        postcode: this.t_postcode
      }
      userService.update_user_profile(data).success((result) =>{
        if (result.error_code === 0) {
          this.unedit2 = true
          this.profile = result.profile
          this.get_profile()
        }
      })
    }
  }
})
