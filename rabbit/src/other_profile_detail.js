import Vue from 'vue'
import $ from 'jquery'
import init from './page/init.js'
import alert from './components/alert.vue'
import userService from './service/user_service'
import experience from './components/experience.vue'
import project_comment from './components/forms/project_comment.vue'
import project_detail from './components/forms/project_detail.vue'
import modal from './components/common/modal.vue'
import mixin_modal from './mixins/modal.js'
import job from './components/job.vue'
import edu from './components/edu.vue'
import work from './components/work.vue'
import lan from './filters/lan'
import star from './directives/star'
import jobService from './service/job_service'
import favoriteService from './service/favorite_service'
import datetime from './filters/datetime'

$.i18n().then((configs) => {
  window['CODE'] = configs.CODE
  window.COMMONS = configs.COMMONS
  Vue.config.delimiters = ['{[', ']}']
  Vue.use(init)
  Vue.use(lan)
  Vue.use(star)
  Vue.use(datetime)
  /* eslint-disable no-new */
  var vm = new Vue({
    el: 'body',
    mixins: [mixin_modal],
    data: {
      uuid: '',
      profile: '',
      jobs: [],
      portfolio: '',
      employment: '',
      education: '',
      works: [],
      error_msg: '',
      pagesize: 5,
      pagenum: 1,
      work_detail: {},
      project_detail: {},
      average_score: ''
    },
    ready () {
      this.uuid = location.href.split('/')[location.href.split('/').length - 1]
      this.add_discover()
      this.getProfile()
      this.getPortfolio()
      this.getEmployment()
      this.getEducation()
      this.getWorks()
      this.get_jobs()
    },
    components: {
      modal,
      project_comment,
      project_detail,
      experience,
      edu,
      job,
      work,
      alert
    },
    methods: {
      add_discover () {
        userService.add_discover({user_id: this.uuid})
      },
      getProfile () {
        userService.get_user_profile({uuid: this.uuid}).success((result) =>{
          if (result.error_code === 0) {
            this.profile = result.profile
          } else {
            $('#alert').modal('show')
            this.error_msg = result.msg
          }
        })
      },
      getPortfolio () {
        userService.get_user_portfolio({user_id: this.uuid}).success((result) =>{
          if (result.error_code === 0) {
            this.portfolio = result.portfolios
          } else {
            $('#alert').modal('show')
            this.error_msg = result.msg
          }
        })
      },
      getEmployment () {
        userService.get_user_employment({user_id: this.uuid}).success((result) =>{
          if (result.error_code === 0) {
            this.employment = result.employments
          } else {
            $('#alert').modal('show')
            this.error_msg = result.msg
          }
        })
      },
      getEducation () {
        userService.get_user_education({user_id: this.uuid}).success((result) =>{
          if (result.error_code === 0) {
            this.education = result.educations
          } else {
            $('#alert').modal('show')
            this.error_msg = result.msg
          }
        })
      },
      getWorks () {
        let data = {
          user_id: this.uuid,
          pagesize: this.pagesize,
          pagenum: this.pagenum
        }
        userService.get_user_work(data).success((result) =>{
          if (result.error_code === 0) {
            for (let i = 0; i < result.contracts.length; i++) {
              this.works.push(result.contracts[i])
            }
            this.pagenum = result.pagenum
            if (Math.ceil(result.count / this.pagesize) === this.pagenum) {
              $('.loadmore').hide()
            }
          } else {
            $('#alert').modal('show')
            this.error_msg = result.msg
          }
        })
      },
      loadmore_works () {
        this.pagenum += 1
        this.getWorks()
      },
      get_jobs () {
        jobService.get_jobs_my().success((result) =>{
          if (result.error_code === 0) {
            this.jobs = result.jobs
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
      add_favorite () {
        if (this.profile.favorite) {
          favoriteService.delete_favorite({target_id: this.uuid}).success((result) =>{
            if (result.error_code === 0) {
              this.profile.favorite = false
            }
          })
        } else {
          favoriteService.add_favorite({target_id: this.uuid}).success((result) =>{
            if (result.error_code === 0) {
              this.profile.favorite = true
            }
          })
        }
      }
    },
    events: {
      'contract_detail': function (work) {
        console.log(work)
        // 事件回调内的 `this` 自动绑定到注册它的实例上
        this.$set('work_detail', work)
        this.open('comment_modal')
      },
      'project_detail': function (project_detail) {
        this.$set('project_detail', project_detail)
        this.open('project_modal')
      }
    }
  })
  $(function () {
    $('#job-error').hide()
    $('#btn-hire').click(function () {
      let job_id = $('#job_id option:selected').val()
      let uuid = vm.$data.uuid
      if (job_id) {
        window.location.href = '/clients/offer/' + job_id + '/' + uuid + '/direct'
      } else {
        $('#job-error').show()
        return false
      }
    })
  })
})
