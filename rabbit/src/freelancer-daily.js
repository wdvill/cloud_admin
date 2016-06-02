import Vue from 'vue'
import $ from 'jquery'
import datetime from './filters/datetime'
import datetimeUtil from './utils/datetime'
import url from './utils/url'
import code from './utils/i18n'
import weekstoneService from './service/weekstone_service'
import contractService from './service/contract_service.js'
// 引用组件
import alertdiv from './components/alert.vue'
import workLog from './components/work-log.vue'
import noLog from './components/workLog/no-work-log.vue'
import remark from './components/workLog/remark.vue'
import modal from './components/common/modal.vue'
import mixin_modal from './mixins/modal.js'

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

code.i18n().then((configs) => {
  window['CODE'] = configs.CODE
  window['COMMONS'] = configs.COMMONS

  new Vue({
    el: '#freelance-daily',
    mixins: [mixin_modal],
    data: {
      error_msg: '',
      contract_id: '',
      contracts: [],
      contract: '',
      end_agree_time: '',
      weekstone_days: [],
      weekstone: '',
      weekstones: [],
      weekstone_id: '',
      weekstone_day: '',
      shots: '',
      t_date: new Date().getFullYear() + '-' + (new Date().getMonth() + 1) + '-' + new Date().getDate(),
      description: '',
      start_time: '',
      add_endtime: '',
      shot_ids: '',
      shot_times: '',
      is_delete: false,
      dis_btn: false
    },
    ready () {
      this.get_weekstone_contract_list()
    },
    components: {
      alertdiv,
      workLog,
      noLog,
      modal,
      remark
    },
    events: {
      select_time (length) {
        this.shot_times = length
      },
      get_screenshot_list () {
        weekstoneService.get_screenshot_list({contract_id: this.contract_id, shot_time: this.weekstone_day}).success((result) =>{
          if (result.error_code === 0) {
            this.shots = result.shots
            this.shot_times = 0
          }
        })
      }
    },
    methods: {
      get_weekstone_contract_list () {
        contractService.get_weekstone_contract_list().success((result) =>{
          if (result.error_code === 0 && result.contracts.length > 0) {
            this.contracts = result.contracts
            if (url.getValueByName('contract_id') !== '') {
              this.contract_id = url.getValueByName('contract_id')
            } else {
              this.contract_id = result.contracts[0].contract_id
            }
            this.select_contract()
          }
        })
      },
      select_contract (index) {
        for (let i = 0; i < this.contracts.length; i++) {
          if (this.contracts[i].contract_id === this.contract_id) {
            this.contract = this.contracts[i]
            this.weekstone_id = this.contracts[i].weekstones[0].weekstone_id
            this.weekstones = this.contracts[i].weekstones
            this.weekstone = this.contracts[i].weekstones[0]
            this.select_weekstone()
            let d = new Date()
            let today = new Date(d.getFullYear(), d.getMonth(), d.getDate())
            let day = new Date(this.weekstone_day.split('-')[0], this.weekstone_day.split('-')[1] - 1, this.weekstone_day.split('-')[2])
            if (this.weekstone.status === 'carry' && day <= today && this.contract.manual) {
              this.dis_btn = true
            } else {
              this.dis_btn = false
            }
            return
          }
        }
        this.contract_id = this.contracts[0].contract_id
        this.contract = this.contracts[0]
        this.weekstone_id = this.contracts[0].weekstones[0].weekstone_id
        this.weekstones = this.contracts[0].weekstones
        this.weekstone = this.contracts[0].weekstones[0]
        this.select_weekstone()
      },
      get_screenshot_list () {
        weekstoneService.get_screenshot_list({contract_id: this.contract_id, shot_time: this.weekstone_day}).success((result) =>{
          if (result.error_code === 0) {
            this.shots = result.shots
            this.shot_times = 0
          }
        })
      },
      select_weekstone_day (event) {
        $('.select-workday li').removeClass('active')
        if (event.target.nodeName === 'A') {
          $(event.target).parent().addClass('active')
          this.weekstone_day = $(event.target).attr('value')
          this.t_date = this.weekstone_day
          let d = new Date()
          let today = new Date(d.getFullYear(), d.getMonth(), d.getDate())
          let day = new Date(this.weekstone_day.split('-')[0], this.weekstone_day.split('-')[1] - 1, this.weekstone_day.split('-')[2])
          if (this.weekstone.status === 'carry' && day <= today && this.contract.manual) {
            this.dis_btn = true
          } else {
            this.dis_btn = false
          }
          this.get_screenshot_list()
        }
      },
      select_weekstone () {
        this.weekstone_days = []
        for (let i = 0; i < this.weekstones.length; i++) {
          if (this.weekstones[i].weekstone_id === parseInt(this.weekstone_id, 10)) {
            this.weekstone = this.weekstones[i]
            this.weekstone_day = this.weekstone.start_at.substring(0, 10)
            this.get_screenshot_list()
            this.calculate_day(this.weekstone.start_at, this.weekstone.end_at)
            return
          }
        }
      },
      get_weekstone_time () {
        weekstoneService.get_weekstone_time({contract_id: this.contract_id}).success((result) =>{
          if (result.error_code === 0) {
            this.weekstone = result.weekstone
            if (result.weekstone.start_at !== '' && result.weekstone.end_at !== '') {
              this.weekstone_days = []
              this.calculate_day(result.weekstone.start_at, result.weekstone.end_at)
            }
          } else {
            $('#alert').modal('show')
            this.error_msg = result.msg
          }
        })
      },
      calculate_day (date_a, date_b) {
        date_a = new Date(date_a.replace(/-/g, '/'))
        date_b = new Date(date_b.replace(/-/g, '/'))
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
      refresh_time () {
        location.reload()
      },
      add_time () {
        weekstoneService.add_screenshot({
          shot_time: this.start_time,
          description: this.description,
          activity: 0,
          keyboard: 0,
          mouse: 0,
          contract_id: this.contract_id,
          is_auto: 0
        }).success((result) =>{
          if (result.error_code === 0) {
            this.record = result.record
            this.start_time = ''
            this.end_time = ''
            this.description = ''
            this.get_screenshot_list()
          } else {
            this.start_time = ''
            this.end_time = ''
            this.description = ''
            $('#alert').modal('show')
            this.error_msg = window['CODE'][result.error_code]
          }
        })
      },
      save_continue () {
        this.add_time()
        this.start_time = ''
        this.end_time = ''
        this.description = ''
      },
      choose_addtime () {
        let o = this.start_time.substr(-8)
        let a = o.substr(0, 3)
        let b = (parseInt(o.charAt(3), 10) + 1).toString()
        let c = o.substr(-4)
        this.add_endtime = a + b + c
      },
      update_remark (type) {
        if ($('.log-list').find('.ico-checkbox-checked').length === 0) {
          return
        } else {
          let ids = []
          let list = $('.log-list').find('.ico-checkbox-checked')
          for (let i = 0; i < list.length; i++) {
            ids.push($(list[i]).attr('value'))
          }
          this.shot_ids = ids.join()
        }
        if (type === 'delete') {
          this.is_delete = true
        } else {
          this.is_delete = false
        }
        this.open('remark_modal')
      },
      cancel_remark () {
        if ($('.log-list').find('.ico-checkbox-checked').length === 0) {
          return
        } else {
          this.shot_times = 0
          $('.ico-checkbox-checked').removeClass('ico-checkbox-checked')
        }
      }
    }
  })

})
