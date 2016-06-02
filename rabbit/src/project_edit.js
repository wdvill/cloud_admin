import Vue from 'vue'
import job_service from './service/job_service'
// import $ from 'jquery'

Vue.config.delimiters = ['{[', ']}']
/* eslint-disable no-new */
new Vue({
  el: '#project-edit',
  data: {
    job: {},
    other: {}
  },
  methods: {
    select_job () {
      let that = this
      let data = {job_id: /\w{16}/g.exec(window.location.pathname)[0]}
      job_service.get_job(data).success((result) => {
        that.job = result.job
        console.log(that.job)
      })
    }
  },
  ready () {
    this.select_job()
  }
})
