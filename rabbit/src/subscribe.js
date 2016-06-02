import Vue from 'vue'
import $ from 'jquery'
import localize from './filters/localize'
import string from './filters/string'
import job_service from './service/job_service.js'
import subscribe_service from './service/subscribe_service.js'
import favoriteService from './service/favorite_service.js'
import user_service from './service/user_service.js'
import init from './page/init.js'
import categories from './components/forms/categories.vue'
import _ from 'underscore'
import modal from './components/common/modal.vue'
import fixed from './components/job/fixed.vue'
import hour from './components/job/hour.vue'
import star from './components/job/star.vue'
import confirm from './components/confirm.vue'
import mixin_modal from './mixins/modal.js'

Vue.config.delimiters = ['{[', ']}']
Vue.use(localize)
Vue.use(string)
Vue.use(init)

var vue = new Vue({
  mixins: [mixin_modal],
  el: '#body',
  ready () {
    let _self = this
    subscribe_service.get_subscribe_list().success((data) => {
      if (data.error_code === 0) {
        _self.$set('subscriptions', data.subscribes)
      }
    })
    this.job_list()
    this.category_list()
    this.user_info()
  },
  data: {
    subscriptions: [ ],
    cursub: {},
    keyword: '',
    job_type: 'job',
    title: '为我推荐',
    histories: [],
    num: 0,
    subscription: '',
    curSub: {},
    confirm: {
      title: '删除订阅',
      msg: '确定要删除这个订阅吗？',
      okFn: null
    }
  },
  methods: {
    user_info () {
      let _self = this
      user_service.get_user_profile().success((data) => {
        if (data.error_code === 0) {
          _self.$set('profile', data.profile)
          this.set_user_status()
        }
      })
    },
    set_user_status () {
      if (this.profile.available) {
        $('input[name="work"][value="' + this.profile.workload + '"]').attr('checked', 'checked')
      } else {
        $('input[name="work"][value="0"]').attr('checked', 'checked')
      }
    },
    setStatus () {
      let data = {}
      let _self = this
      if ($('input[name="work"]:checked').val() === '0') {
        data.available = false
        _self.profile.available = false
        _self.profile.workload = 0
      } else {
        data.available = true
        data.workload = $('input[name="work"]:checked').val()
        _self.profile.available = true
        _self.profile.workload = $('input[name="work"]:checked').val()
      }
      user_service.update_user_profile(data).success((data) => {
        if (data.error_code === 0) {
          $('.workstate').modal('hide')
        } else {
          alert(data.msg)
        }
      })
    },
    job_list () {
      this.subscription = ''
      let _self = this
      job_service.get_job_list().success((data) => {
        if (data.error_code === 0) {
          _self.$set('jobs', data.jobs)
          _self.$set('jobs_count', data.count)
          _self.$set('page_num', data.pagenum)
        } else {
          console.log('data job list', data)
        }
      })
    },
    more () {
      let _self = this
      if (this.subscription !== '') {
        this.subscription.pagenum = ++this.page_num
        job_service.search(this.subscription)
        .success((data) => {
          if (data.error_code === 0) {
            _self.$set('jobs', _self.jobs.concat(data.jobs))
            _self.$set('jobs_count', data.count)
            _self.$set('page_num', data.pagenum)
          } else {
            console.log('data job list', data)
          }
        })
      } else {
        job_service.get_job_list({pagenum: ++this.page_num}).success((data) => {
          if (data.error_code === 0) {
            _self.$set('jobs', _self.jobs.concat(data.jobs))
          } else {
            console.log('no-more')
          }
        })
      }
    },
    category_list () {
      let _self = this
      user_service.get_category_list()
        .success((data) => {
          if (data.error_code === 0) {
            _self.$set('categories', data.categorys)
          }
        })
    },
    /* 删除订阅触发 */
    unsub (subscription) {
      console.log('confirm')
      this.curSub = subscription
      this.confirm.okFn = this.unsubscribe
    },
    /* 删除订阅函数 */
    unsubscribe () {
      console.log('unsubscribe')
      subscribe_service.unsubscribe({subscribe_id: this.curSub.id})
        .success((data) => {
          if (data.error_code === 0) {
            this.subscriptions.splice(_.findIndex(this.subscriptions, this.curSub), 1)
          }
        })
    },
    focus (element) {
      let row = $(element).parents('.subscibe')
      $('.subscibe').removeClass('getfocus')
      row.addClass('getfocus')
    },
    find_job () {
      if ($.trim(this.keyword) === '') {
        return
      }
      location.href = '/jobs/find?q=' + this.keyword
    },
    recommend (event) {
      this.focus(event.target)
      this.job_list()
      this.job_type = 'job'
      this.title = '为我推荐'
    },
    search (subscription, event) {
      let _self = this
      _self.focus(event.target)
      this.job_type = 'job'
      this.title = subscription.name
      subscription.keyword = subscription.name
      this.subscription = subscription
      job_service.search(subscription)
        .success((data) => {
          if (data.error_code === 0) {
            _self.$set('jobs', data.jobs)
            _self.$set('jobs_count', data.count)
            _self.$set('page_num', data.pagenum)
          } else {
            console.log('data job list', data)
          }
        })
    },
    enter (subscription, event) {
      if (event.keyCode === 13) {
        this.find_job()
      }
    },
    add_favorite (item) {
      if (item.favorite) {
        favoriteService.delete_favorite({target_id: item.id}).success((result) =>{
          if (result.error_code === 0) {
            item.favorite = false
          }
        })
      } else {
        favoriteService.add_favorite({target_id: item.id}).success((result) =>{
          if (result.error_code === 0) {
            item.favorite = true
          }
        })
      }
    },
    watch: {
      job_type (value) {
        console.log(value, 'watch')
        if (value === 'job') {
          this.title = '我的订阅'
        } else {
          this.title = '为我推荐'
        }
      }
    },
    edit_category () {
      this.open('categories_modal')
    },
    mysubscribe (event) {
      this.job_type = 'subscribe'
      this.title = '我的订阅'
      this.focus(event.target)
    }
  },
  components: {
    categories,
    modal,
    fixed,
    hour,
    star,
    confirm
  },
  events: {
    categories (categories) {
      if (localStorage) {
        let histories = localStorage.getItem('search_keywords')
        if (histories) {
          this.$set('histories', histories.split(',').reverse())
        }
      }
    }
  }
})

vue.$set('test', 'tao')
