import Vue from 'vue'
import $ from 'jquery'
import alertdiv from './components/alert.vue'
import page from './directives/page.js'
import contractService from './service/contract_service'

Vue.config.delimiters = ['{[', ']}']
Vue.use(page)

/* eslint-disable no-new */
new Vue({
  el: '#body',
  data: {
    contracts: '',
    error_msg: '',
    pageObject: {itemsCount: 0, pageNo: 1, pageSize: 10},
    status: ''
  },
  ready () {
    this.sign_contract_list()
  },
  components: {
    alertdiv
  },
  methods: {
    sign_contract_list () {
      let data = {
        status: 'paid',
        pagenum: this.pageObject.pageNo,
        pagesize: this.pageObject.pageSize
      }
      contractService.select_contract(data).success((result) =>{
        if (result.error_code === 0) {
          let self = this
          let list = result.contracts

          for (let i = 0; i < list.length; i++) {
            let newDate = new Date((list[i].create_at).replace(/-/g, '/'))
            list[i].pass_time = new Date(newDate.setDate(newDate.getDate() + 2))
            list[i].sec_time = ''
          }

          this.contracts = list
          this.pageObject = {
            itemsCount: result.count,
            pageNo: data.pagenum,
            pageSize: data.pagesize
          }

          setInterval(self.calculate_time, 1000)

        } else {
          $('#alert').modal('show')
          this.error_msg = result.msg
        }
      })
    },
    calculate_time () {
      let list = this.contracts
      for (let i = 0; i < list.length; i++) {
        let difference = list[i].pass_time.getTime() - new Date().getTime()
        if (difference > 0) {
          let hour = difference / (1000 * 60 * 60)
          let minute = (difference % (1000 * 60 * 60)) / (1000 * 60)
          let second = (difference % (1000 * 60 * 60)) % (1000 * 60) / 1000
          list[i].sec_time = parseInt(hour, 10) + ':' + parseInt(minute, 10) + ':' + parseInt(second, 10)
        }
      }
      this.contracts = list
    }
  }
})
