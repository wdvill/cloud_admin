import Vue from 'vue'
import $ from 'jquery'
import code from './utils/i18n'
import init from './page/init.js'
import validate from './utils/validate'
import alert from './components/alert.vue'
import error from './components/common/error_div.vue'
import proposalService from './service/proposal_service'
import categoryService from './service/category_service'
import jobService from './service/job_service'

Vue.config.delimiters = ['{[', ']}']
Vue.use(init)
/* eslint-disable no-new */
new Vue({
  el: '#body',
  data: {
    newproject: false,
    fixed: false,
    jobs: [],
    job_id: '',
    user_id: '',
    message: '',
    cat_all: '',
    category: '',
    children_category: '',
    categoryone: '',
    categorytwo: '',
    paymethod: 'hour',
    duration: '1',
    workload: '1',
    budget: '',
    error_msg: '',
    offerUrl: ''
  },
  ready () {
    validate.RegEventBlur($('#form-invite'))
    this.user_id = location.href.split('/')[location.href.split('/').length - 2]
    this.get_jobs()
    this.get_category()
  },
  components: {
    alert,
    error
  },
  watch: {
    categoryone: function (val) {
      this.children_category = $.grep(this.cat_all, function (data, index) {
        return data.pid === parseInt(val, 10)
      })
    }
  },
  methods: {
    change_project (f) {
      this.newproject = f
    },
    changepay (f) {
      this.fixed = f
    },
    get_jobs () {
      jobService.get_job_proposal().success((result) =>{
        if (result.error_code === 0) {
          this.jobs = result.jobs
          this.job_id = this.jobs[0].id
        } else {
          $('#alert').modal('show')
          this.error_msg = result.msg
        }
      })
    },
    change_jobs () {
      for (let i = 0; i < this.jobs.length; i++) {
        if (this.jobs[i].id === this.job_id) {
          $('#project_description').html(this.jobs[i].description)
        }
      }
    },
    get_category () {
      code.i18n().then((data) =>{
        window['CODE'] = data.CODE
        window['COMMONS'] = data.COMMONS
        categoryService.get_category_list({category_id: 0, t: 'all'}).success((result) =>{
          if (result.error_code === 0) {
            for (let i = 0; i < result.categorys.length; i++) {
              result.categorys[i].name = window['COMMONS'][result.categorys[i].name]
            }
            this.cat_all = result.categorys
            this.category = $.grep(result.categorys, function (data) {
              return data.pid === 0
            })
          }
        })
      })
    },
    new_job () {
      let data = {
        name: this.job_id,
        description: this.user_id,
        category_id: this.message,
        paymethod: this.paymethod,
        duration: this.duration,
        workload: this.workload
      }
      jobService.add_job(data).success((result) =>{
        if (result.error_code === 0) {
          this.invite()
        } else {
          $('#alert').modal('show')
          this.error_msg = result.msg
        }
      })
    },
    invite () {
      if (!validate.validateForm($('#form-invite'))) {
        return
      }
      let data = {
        job_id: this.job_id,
        user_id: this.user_id,
        message: this.message
      }
      proposalService.add_proposal(data).success((result) =>{
        if (result.error_code === 0) {
          location.href = '/clients/jobs'
        } else {
          $('#alert').modal('show')
          this.error_msg = result.msg
        }
      })
    }
  }
})
