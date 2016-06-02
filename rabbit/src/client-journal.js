import Vue from 'vue'
import $ from 'jquery'
import urlUtil from './utils/url'
import datetime from './filters/datetime'
import datetimeUtil from './utils/datetime'
import alert from './components/alert.vue'
import weekstone_agree from './components/forms/weekstone_agree.vue'
import modal from './components/common/modal.vue'
import mixin_modal from './mixins/modal.js'
import workLog from './components/work-log.vue'
import weekstoneService from './service/weekstone_service'

Vue.config.delimiters = ['{[', ']}']
Vue.use(datetime)

// 自定义过滤器：格式化时间
Vue.filter('formatTime', val => val.slice(-8, -3))

// 自定义过滤器：24小时转12小时
Vue.filter('ampm', val => {
  let st = '<br/>'
  st = val < 12 ? `${st}am` : `${st}pm`
  return val > 12 ? `${val - 12}${st}` : `${val}${st}`
})

/* eslint-disable no-new */
new Vue({
  el: '#container',
  mixins: [mixin_modal],
  data: {
    contract_id: '',
    weekstone: '',
    weekstone_days: [],
    weekstone_day: '',
    shots: '',
    is_agree: 'accept',
    error_msg: '',
    end_agree_time: ''
  },
  ready () {
    this.contract_id = urlUtil.getLastTwoId()
    this.get_weekstone_pay()
    if (this.weekstone.create_at !== '') {
      setInterval(() =>{this.calculate_time(this.weekstone.create_at)}, 1000)
    }
  },
  components: {
    alert,
    modal,
    weekstone_agree,
    workLog
  },
  methods: {
    get_weekstone_pay () {
      weekstoneService.get_weekstone_pay({contract_id: this.contract_id}).success((result) =>{
        if (result.error_code === 0) {
          this.weekstone = result.weekstone
          if (result.weekstone.start_at !== '' && result.weekstone.end_at !== '') {
            this.calculate_day(result.weekstone.start_at, result.weekstone.end_at)
            this.weekstone_day = this.weekstone.start_at.substring(0, 10)
            this.get_screenshot_list()
          }
          if (result.weekstone.create_at !== '') {
            this.calculate_time(result.weekstone.create_at)
          }
        } else {
          $('#alert').modal('show')
          this.error_msg = result.msg
        }
      })
    },
    select_weekstone_day (event) {
      $('.select-workday li').removeClass('active')
      if (event.target.nodeName === 'A') {
        $(event.target).parent().addClass('active')
        this.weekstone_day = $(event.target).attr('value')
        this.get_screenshot_list()
      }
    },
    get_screenshot_list () {
      weekstoneService.get_screenshot_list({contract_id: this.contract_id, shot_time: this.weekstone_day}).success((result) =>{
        if (result.error_code === 0) {
          this.shots = result.shots
        }
      })
    },
    calculate_day (date_a, date_b) {
      date_a = new Date(date_a.replace(/-/g, '/'))
      date_b = new Date(date_b.replace(/-/g, '/'))
      this.weekstone_days = []
      this.weekstone_days.push({c: date_a.getMonth() + 1 + '月' + date_a.getDate() + '日', e: date_a.getFullYear() + '-' + (date_a.getMonth() + 1) + '-' + date_a.getDate()})
      while (!(date_a.getFullYear() === date_b.getFullYear() && date_a.getMonth() === date_b.getMonth() && date_a.getDate() === date_b.getDate())) {
        let data_new = new Date(date_a.setDate(date_a.getDate() + 1))
        this.weekstone_days.push({c: data_new.getMonth() + 1 + '月' + data_new.getDate() + '日', e: data_new.getFullYear() + '-' + (data_new.getMonth() + 1) + '-' + data_new.getDate()})
      }
    },
    calculate_time (create_time) {
      create_time = new Date(create_time.replace(/-/g, '/'))
      let end_time = new Date(create_time.setDate(create_time.getDate() + 2))
      this.end_agree_time = datetimeUtil.getDiff(new Date(), end_time)
    },
    agree (type) {
      this.is_agree = type
      this.open('weekstone_agree_modal')
    }
  }
})
