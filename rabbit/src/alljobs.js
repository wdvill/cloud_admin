import Vue from 'vue'
import $ from 'jquery'
import alert from './components/alert.vue'
import page from './directives/page.js'
import datetime from './filters/datetime'
import jobService from './service/job_service'

Vue.config.delimiters = ['{[', ']}']

Vue.use(datetime)
Vue.use(page)

/* eslint-disable no-new */
new Vue({
  el: '#container',
  data: {
    jobs: [],
    status: 'all',
    pageObject: {itemsCount: 0, pageNo: 1, pageSize: 10},
    error_msg: ''
  },
  ready () {
    this.get_job_list()
  },
  components: {
    alert
  },
  methods: {
    get_job_list () {
      let data = {
        status: this.status,
        pagenum: this.pageObject.pageNo,
        pagesize: this.pageObject.pageSize
      }
      jobService.get_jobs_my(data).success((result) =>{
        if (result.error_code === 0) {
          this.jobs = result.jobs
          this.pageObject = {itemsCount: result.count, pageNo: data.pagenum, pageSize: data.pagesize}
        } else {
          $('#alert').modal('show')
          this.error_msg = result.msg
        }
      })
    }
  }
})
