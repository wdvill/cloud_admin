import Vue from 'vue'
import code from './utils/i18n'
import localize from './filters/localize'
import date from './filters/datetime'
import contract_service from './service/contract_service'

Vue.config.delimiters = ['{[', ']}']
Vue.use(localize)
Vue.use(date)

var vue = new Vue({
  el: '#contract',
  data: {
    contracts: []
  },
  ready () {
    let _self = this
    code.i18n().then((data) =>{
      window['CODE'] = data.CODE
      window['COMMONS'] = data.COMMONS._contract_status
      contract_service.select_contract({status: 'all'}).success((data) => {
        if (data.error_code === 0) {
          for (let i = 0; i < data.contracts.length; i++) {
            data.contracts[i].status_e = data.contracts[i].status
            data.contracts[i].status = window['COMMONS'][data.contracts[i].status]
          }
          _self.$set('contracts', data.contracts)
        }
      })
    })
  }
})
vue.$set('test', 'hello')
