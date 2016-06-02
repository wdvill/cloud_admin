import Vue from 'vue'
import $ from 'jquery'
import datetime from './filters/datetime'
import datetimeUtil from './utils/datetime'
import alert from './components/alert.vue'
import weekstone_agree from './components/forms/weekstone_agree.vue'
import modal from './components/common/modal.vue'
import mixin_modal from './mixins/modal.js'
import workLog from './components/work-log.vue'
import contractService from './service/contract_service'
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

new Vue({
  el: '#container',
  mixins: [mixin_modal],
  data: {
    contracts: [],
    contract: '',
    contract_id: '',
    can_check: false,
    weekstone: '',
    weekstones: [],
    weekstone_id: '',
    weekstone_days: [],
    weekstone_day: '',
    is_agree: 'accept',
    error_msg: '',
    end_agree_time: '',
    shots: ''
  },
  ready () {
    this.get_weekstone_contract_list()
  },
  components: {
    alert,
    modal,
    weekstone_agree,
    workLog
  },
  methods: {
    get_weekstone_contract_list () {
      contractService.get_weekstone_contract_list().success((result) =>{
        if (result.error_code === 0 && result.contracts.length > 0) {
          this.contracts = result.contracts
          let r = location.search
          if (r && r.split('?')[1].split('=')[0] === 'contract_id') {
            this.contract_id = r.split('=')[1]
          } else {
            this.contract_id = result.contracts[0].contract_id
          }
          this.select_contract()
        }
      })
    },
    get_screenshot_list () {
      weekstoneService.get_screenshot_list({contract_id: this.contract_id, shot_time: this.weekstone_day}).success((result) =>{
        if (result.error_code === 0) {
          this.shots = result.shots
        }
      })
    },
    select_contract () {
      for (let i = 0; i < this.contracts.length; i++) {
        if (this.contracts[i].contract_id === this.contract_id) {
          this.contract = this.contracts[i]
          this.weekstone_id = this.contracts[i].weekstones[0].weekstone_id
          this.weekstones = this.contracts[i].weekstones
          this.weekstone = this.contracts[i].weekstones[0]
          this.select_weekstone('')
          return
        }
      }
      this.contract_id = this.contracts[0].contract_id
      this.contract = this.contracts[0]
      this.weekstone_id = this.contracts[0].weekstones[0].weekstone_id
      this.weekstones = this.contracts[0].weekstones
      this.weekstone = this.contracts[0].weekstones[0]
      this.select_weekstone('')
    },
    select_weekstone_day (event) {
      $('.select-workday li').removeClass('active')
      if (event.target.nodeName === 'A') {
        $(event.target).parent().addClass('active')
        this.weekstone_day = $(event.target).attr('value')
        this.get_screenshot_list()
      }
    },
    select_weekstone (type) {
      for (let i = 0; i < this.weekstones.length; i++) {
        if (this.weekstones[i].weekstone_id === this.weekstone_id) {
          if (type === 'next' && this.weekstones[i + 1]) {
            this.weekstone_id = this.weekstones[i + 1].weekstone_id
            this.weekstone = this.weekstones[i + 1]
          } else if (type === 'pre' && this.weekstones[i + 1]) {
            this.weekstone_id = this.weekstones[i - 1].weekstone_id
            this.weekstone = this.weekstones[i - 1]
          } else if (type !== '') {
            return
          } else {
            this.weekstone = this.weekstones[i]
          }
          this.weekstone_day = this.weekstone.start_at.substring(0, 10)
          this.get_screenshot_list()
          this.calculate_day(this.weekstone.start_at, this.weekstone.end_at)
          if (this.weekstone.status === 'carry_pay' && this.contract.contract_status === 'carry') {
            this.can_check = true
            if (this.weekstone.create_at !== '') {
              setInterval(() =>{this.calculate_time(this.weekstone.create_at)}, 1000)
            }
          } else {
            this.can_check = false
          }
          return
        }
      }
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
