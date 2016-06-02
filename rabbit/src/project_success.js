import $ from 'jquery'
import Vue from 'vue'
import url from './utils/url'
import work from './components/work.vue'
import employ from './components/job/employ.vue'
import userService from './service/user_service'
import jobService from './service/job_service'
import datetime from './filters/datetime'

Vue.config.delimiters = ['{[', ']}']
Vue.use(datetime)
new Vue({
  el: '#body',
  data: {
    users: [],
    jobs: [],
    works: [],
    uuid: '',
    choose_one: {}
  },
  ready () {
    this.$set('job_id', location.pathname.split('/')[4])
    this.get_recommands()
  },
  components: {
    work,
    employ
  },
  methods: {
    get_recommands () {
      jobService.get_jobs_recommand({job_id: url.getLastId()}).success((result) =>{
        if (result.error_code === 0) {
          if (result.users.length > 0) {
            for (let i = 0; i < result.users.length; i++) {
              if (result.users[i].name.length > 5) {
                result.users[i].nametip = result.users[i].name.substr(0, 5) + '...'
              } else {
                result.users[i].nametip = result.users[i].name
              }
            }
            this.users = result.users
            this.select_user(result.users[0].id)
          }
        }
      })
    },
    select_user (id) {
      userService.get_user_profile({uuid: id}).success((result) =>{
        if (result.error_code === 0) {
          this.choose_one = result.profile
          this.getWorks()
        }
      })
    },
    getWorks () {
      userService.get_user_work({user_id: this.choose_one.id}).success((result) =>{
        if (result.error_code === 0) {
          if (result.contracts.length < 3) {
            $('.loadmore').hide()
          }
          this.works = result.contracts
        }
      })
    },
    employ () {
      this.uuid = this.choose_one.id
    }
  }
})
