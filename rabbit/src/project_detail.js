import Vue from 'vue'
import job_service from './service/job_service'
import favorite_service from './service/favorite_service'
import localize from './filters/localize'
import datetime from './filters/datetime'
import client from './components/proposal/client.vue'
import detail from './components/job/detail.vue'
import alert_modal from './components/alert.vue'
import strapAlert from './components/strap_alert.vue'
import YWORK from './utils/ywk.js'
import filter from './utils/filter.js'
import $ from 'jquery'

require('./assets/sass/views/project/project-detail.scss')

Vue.config.delimiters = ['{[', ']}']
Vue.filter('html_decode', filter.html_decode)
Vue.use(localize)
Vue.use(datetime)

new Vue({
  el: '#project-detail',
  data: {
    job_id: '',
    job: {},
    other: {},
    unit: '元',
    proposal: {
      showDetail: false,
      list: [],
      maxPrice: 0,
      avgPrice: 0,
      minPrice: 0
    },
    alert: {
      title: '操作提示',
      msg: '',
      showType: 'danger',
      showAlert: false
    }
  },
  ready () {
    this.job_id = window.location.pathname.substr(-16, 16)
    this.select_job()
    this.get_proposal()
  },
  methods: {
    select_job () {
      let data = {job_id: window.location.pathname.substr(-16, 16)}
      job_service.get_job(data).success((result) => {
        this.job = result.job
        if (result.job.paymethod === 'hour') {
          this.unit = '元/时'
        }
        this.other = result.other
      })
    },
    get_proposal () {
      YWORK.getJson('/api/proposal', {job_id: this.job_id, operate: 'active', timestamp: (new Date()).getTime()}).success((result) =>{
        if (result.error_code === 0) {
          let allPrice = 0
          let prices = []
          this.proposal.list = []
          if (result.proposals.length > 0) {
            // 获取申请人列表数据
            result.proposals.forEach((item) => {
              allPrice += item.price
              prices.push(item.price)
              this.proposal.list.push({name: item.user.freelancer.name, time: item.create_at, price: item.price, userId: item.user.freelancer.id})
            })
            // 对价格排序
            prices = prices.sort((a, b) => a - b)
            // 处理招标范围
            this.proposal.minPrice = prices[0]
            this.proposal.maxPrice = prices[prices.length - 1]
            this.proposal.avgPrice = (allPrice / prices.length).toFixed(0)
            console.log(this.proposal)
          }
        }
      })
    },
    collect () {
      let data = {target_id: this.job.id}
      let _self = this
      if (this.job.favorite) {
        favorite_service.delete_favorite(data).success((result) => {
          if (result.error_code === 0) {
            this.show_alert('操作提示', '恭喜你，取消收藏成功！', 'success')
            _self.$set('job.favorite', false)
          } else {
            this.show_alert('错误提示', result.msg, 'danger')
          }
        })
      } else {
        favorite_service.add_favorite(data).success((result) => {
          if (result.error_code === 0) {
            this.show_alert('操作提示', '恭喜你，收藏成功！', 'success')
            _self.$set('job.favorite', true)
          } else {
            this.show_alert('错误提示', result.msg, 'danger')
          }
        })
      }
    },
    update_pro (type) {
      job_service.update_job({job_id: this.job.id, status: type}).success((result) => {
        let _html = ''
        if (type === 'normal') {
          _html = '成功！公开状态服务方可以搜索到您的项目了，邀请合适的服务方可以更快的把项目众包出去喔！'
        } else if (type === 'private') {
          _html = '成功！私有状态您要主动查找联系服务方才可以喔，但是已经收到的申请还会保存在列表里。'
        }
        if (result.error_code === 0) {
          if (type === 'close') {
            window.location.href = '/clients/jobs/list'
            return
          }
          $('#success_div').html(_html).show()
          setTimeout(() =>{
            $('#success_div').hide()
            this.select_job()
          }, 5000)
        } else {
          $('#fail_div').html('哎呀，失败了，再试一次吧！').show()
          setTimeout(() =>{
            $('#fail_div').hide()
          }, 5000)
        }
      })
    },
    /** 消息提示 */
    show_alert (title, msg, type) {
      this.alert.title = title
      this.alert.msg = msg
      this.alert.showType = type
      this.alert.showAlert = true
    }
  },
  components: {
    client,
    alert_modal,
    detail,
    strapAlert
  }
})
