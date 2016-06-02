import Vue from 'vue'
import url from '../../utils/url.js'
import weekstoneService from '../../service/weekstone_service.js'

require('../../assets/sass/components/work-log.scss')
Vue.config.delimiters = ['{[', ']}']

new Vue({
  el: 'body',
  data: {
    contract_id: '',
    shot_id: '',
    shot: ''
  },
  ready () {
    this.contract_id = window.location.pathname.split('/')[2]
    this.shot_id = url.getLastId()
    this.get_screenshot()
  },
  methods: {
    get_screenshot () {
      weekstoneService.get_screenshot_list({contract_id: this.contract_id, shot_id: this.shot_id}).success((result) =>{
        if (result.error_code === 0) {
          this.shot = result.shot
        }
      })
    }
  }
})
