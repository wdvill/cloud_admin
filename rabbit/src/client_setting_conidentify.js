import Vue from 'vue'
import $ from 'jquery'
import Cookies from 'js-cookie'
import validate from './utils/validate'
import alert from './components/alert.vue'
import error from './components/common/error_div.vue'
import userService from './service/user_service'
import fileService from './service/file_service'

Vue.config.delimiters = ['{[', ']}']

var msgConfig = {
  'uncheck': {
    style: 'alert-info',
    msg: '您还没有完成公司认证。'
  },
  'pass': {
    style: 'alert-warning',
    msg: '您已经完成了公司认证。'
  },
  'checking': {
    style: 'alert-warning',
    msg: '您的公司认证正在审核中，我们将会在24小时内完成审核，审核结果请留意系统消息。'
  },
  'unpass': {
    style: 'alert-warning',
    msg (reason) {
      return `您的公司认证没有通过，原因：“${reason}”，请重新提交申请`
    }
  }
}

new Vue({
  el: '#body',
  data: {
    profile: '',
    permit_number: '',
    org_number: '',
    company_name: '',
    name: '',
    phone: '',
    permit_id: '',
    org_id: '',
    error_msg: ''
  },
  ready () {
    validate.RegEventBlur($('#form-verify'))
    this.get_profile()
  },
  computed: {
    checkStatus () {
      let check = this.profile.company_verify.is_verify
      let reason = this.profile.company_verify.reason
      return {
        style: msgConfig[check].style,
        msg: check === 'unpass' ? msgConfig[check].msg(reason) : msgConfig[check].msg
      }
    }
  },
  components: {
    alert,
    error
  },
  methods: {
    get_profile () {
      userService.get_user_profile().success((result) =>{
        if (result.error_code === 0) {
          this.profile = result.profile
          this.permit_number = result.profile.permit_number
          this.org_number = result.profile.org_number
          this.company_name = result.profile.company_name
          this.name = result.profile.contact
          this.phone = result.profile.contact_phone
        }
      })
    },
    onload_file (type) {
      let formData = new FormData()
      let f = $('#permit')[0].files[0]
      if (type === 'org') {
        f = $('#org')[0].files[0]
      }
      formData.append('file', f)
      let params = '?t=company&x=0&y=0&w=180&h=200&boundx=0&boundy=0'
      params += '&_xsrf=' + Cookies.get('_xsrf')
      fileService.upload(params, formData).success((result) =>{
        if (result.error_code === 0) {
          if (type === 'org') {
            this.profile.org_img = result.path
            this.org_id = result.attachment_id
          } else {
            this.profile.permit_img = result.path
            this.permit_id = result.attachment_id
          }
        }
      })
    },
    verify () {
      if (!validate.validateForm($('#form-verify'))) {
        return
      }
      let data = {
        company_name: this.company_name,
        permit_number: this.permit_number,
        org_number: this.org_number,
        name: this.name,
        phone: this.phone,
        permit_id: this.permit_id,
        org_id: this.org_id
      }
      userService.add_client_verify(data).success((result) =>{
        if (result.error_code === 0) {
          window.location.reload()
        } else {
          $('#alert').modal('show')
          this.error_msg = result.msg
        }
      })
    }
  }
})
