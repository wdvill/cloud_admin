import Vue from 'vue'
import $ from 'jquery'
import Cookies from 'js-cookie'
import validate from './utils/validate'
import alert from './components/alert.vue'
import commonService from './service/common_service'
import userService from './service/user_service'
import fileService from './service/file_service'

Vue.config.delimiters = ['{[', ']}']
// 链接加http
Vue.filter('formatLink', (val) => {
  // 返回处理后的值
  if (val) {
    val = val.indexOf('http://') >= 0 ? val : 'http://' + val
  }
  return val
})
/* eslint-disable no-new */
new Vue({
  el: '#body',
  data: {
    show_info: true,
    show_ca: true,
    show_contact: true,
    profile: {},
    pname: '',
    cname: '',
    link: '',
    overview: '',
    prarent_address: [],
    child_address: [],
    address_pid: '',
    location_id: '',
    t_address: '',
    t_email: '',
    t_phone: '',
    error_msg: ''
  },
  ready () {
    validate.RegEventBlur($('#form-client-info'))
    validate.RegEventBlur($('#form-client-ca'))
    validate.RegEventBlur($('#form-client-contact'))
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
    edit_info (s) {
      if (s === 'show_info') {
        this.show_info = false
      }else if (s === 'show_ca') {
        this.show_ca = false
      } else {
        this.show_contact = false
      }
    },
    onload_file (type) {
      let $this = this
      let formData = new FormData()
      let f = $('#photo')[0].files[0]
      if (type === 'logo') {
        f = $('#logo')[0].files[0]
      }
      formData.append('file', f)
      let params = '?t=' + type + '&x=0&y=0&w=180&h=200&boundx=0&boundy=0'
      params += '&_xsrf=' + Cookies.get('_xsrf')
      fileService.upload(params, formData).success((result) =>{
        if (result.error_code === 0) {
          if (type === 'logo') {
            $this.profile.logo = result.avatar
          } else {
            $this.profile.freelancer.avatar = result.avatar
          }
        }
      })
    },
    update_profile (data, s) {
      userService.update_user_profile(data).success((result) =>{
        if (result.error_code !== 0) {
          $('#alert').modal('show')
          this.error_msg = result.msg
        } else {
          if (s === 'show_info') {
            this.show_info = true
          }else if (s === 'show_ca') {
            this.show_ca = true
          } else {
            this.show_contact = true
          }
          this.get_profile()
        }
      })
    },
    update_info () {
      if (!validate.validateForm($('#form-client-info'))) {
        return
      }
      this.update_profile({name: this.pname}, 'show_info')
    },
    update_ca () {
      if (!validate.validateForm($('#form-client-ca'))) {
        return
      }
      let data = {
        client_name: this.cname,
        link: this.link,
        overview: this.overview
      }
      this.update_profile(data, 'show_ca')
    },
    update_contact () {
      if (!validate.validateForm($('#form-client-contact'))) {
        return
      }
      let data = {
        location_id: this.location_id,
        address: this.t_address,
        email: this.t_email,
        phone: this.t_phone
      }
      this.update_profile(data, 'show_contact')
    }
  }
})
