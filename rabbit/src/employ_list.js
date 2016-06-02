import Vue from 'vue'
import $ from 'jquery'
import alertdiv from './components/alert.vue'
import page from './directives/page.js'
import contractService from './service/contract_service'

Vue.config.delimiters = ['{[', ']}']
Vue.use(page)

/* eslint-disable no-new */
new Vue({
  el: '#layout',
  data: {
    freelancers: [],
    error_msg: '',
    lookContract: [],
    choose_contract: ''
  },
  ready () {
    this.employ_list()
  },
  components: {
    alertdiv
  },
  methods: {
    employ_list () {
      let data = {
        utype: 'hire'
      }
      contractService.contract_freelancers_list(data).success((result) =>{
        if (result.error_code === 0) {
          this.freelancers = result.freelancers
        } else {
          $('#alert').modal('show')
          this.error_msg = result.msg
        }
      })
    },
    look_contract (data) {
      this.lookContract = this.freelancers[data].contracts
    },
    select_contract () {
      contractService.contract_freelancers_list().success((result) =>{
        if (this.choose_contract !== 'none') {
          window.location = '/freelancers/contracts/' + this.choose_contract
        } else {
          alert('请选择合同')
        }
      })
    }
  }
})
