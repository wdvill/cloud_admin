import Vue from 'vue'
import commonService from './service/common_service'

Vue.config.delimiters = ['{[', ']}']
/* eslint-disable no-new */
new Vue({
  el: 'body',
  data: {
    freelancers: ''
  },
  ready () {
    this.recommend()
  },
  methods: {
    recommend () {
      commonService.recommend_freelancers().success((result) =>{
        if (result.error_code === 0) {
          this.freelancers = result.freelancers
        }
      })
    }
  }
})
