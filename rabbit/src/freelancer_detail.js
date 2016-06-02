import Vue from 'vue'
import util from './utils/url'
import $ from 'jquery'
import localize from './filters/localize'
import datetime from './filters/datetime'
import alert from './components/alert.vue'
import operate from './components/proposal/operate.vue'
import client from './components/proposal/client.vue'
import proposal_service from './service/proposal_service'
import contractService from './service/contract_service'
import strapAlert from './components/strap_alert.vue'

Vue.config.delimiters = ['{[', ']}']
Vue.use(localize)
Vue.use(datetime)

var vue = new Vue({
  el: 'body',
  data: {
    message: '',
    error_msg: '',
    alert: {
      msg: '',
      title: '',
      showType: 'danger',
      showAlert: false,
      cb: null
    }
  },
  ready () {
    let $this = this
    this.$set('id', util.getLastId())
    proposal_service.get_proposal_list({'proposal_id': this.id})
      .success($.proxy(this.handleData, $this))
    console.log(this.proposal)
  },
  methods: {
    handleData (data) {
      if (data.error_code === 0 && data.proposals) {
        this.$set('proposal', data.proposals[0])
      }
      if (this.proposal.status === 'hire' || this.proposal.status === 'interview') {
        this.get_message()
      }
    },
    get_message () {
      proposal_service.get_message_list({'proposal_id': this.id}).success((result) =>{
        if (result.error_code === 0 && result.messages) {
          this.$set('messages', result.messages)
        }
      })
    },
    send_message () {
      if ($.trim(this.message) === '') {
        return
      }
      contractService.send_message({proposal_id: this.id, content: this.message}).success((result) =>{
        if (result.error_code === 0) {
          this.get_message()
          this.message = ''
        } else {
          $('#alert').modal('show')
          this.error_msg = result.msg
        }
      })
    }
  },
  events: {
    show_alert (type, title, msg, cb) {
      console.log('show_alert')
      this.alert.title = title
      this.alert.msg = msg
      this.alert.showType = type
      this.alert.showAlert = true
      if (cb) {
        this.alert.cb = cb
      }
    }
  },
  components: {
    operate,
    client,
    alert,
    strapAlert
  }
})
vue.$set('test', 'hello')
