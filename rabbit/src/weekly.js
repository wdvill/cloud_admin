import Vue from 'vue'
import $ from 'jquery'
import datetime from './filters/datetime'
import string from './filters/string'
import Cookies from 'js-cookie'
import reportService from './service/report_service'
import calendar from './components/calendar.vue'
Vue.config.delimiters = ['{[', ']}']
Vue.use(datetime)
Vue.use(string)
$.ajaxPrefilter(function (options, originalOptions, jqXHR) {
  try {
    options.data = $.param($.extend(originalOptions.data, { '_xsrf': Cookies.get('_xsrf') }))
  } catch (e) {
    console.log(e)
  }
})

var vue = new Vue({
  el: '#body',
  data: {
    start_at: '',
    end_at: ''
  },
  ready () {
    // 当前日期
    let now = new Date()
    // 开始时间
    let start_time = new Date(now.getTime() - ((now.getDay() - 1) * 86400000))
    let start_year = start_time.getFullYear()
    let start_month = start_time.getMonth() + 1
    let start_date = start_time.getDate()
    start_month = start_month < 10 ? '0' + start_month : start_month
    start_date = start_date < 10 ? '0' + start_date : start_date
    this.start_at = start_year + '年' + start_month + '月' + start_date + '日'
    // 结束时间
    let end_time = new Date(now.getTime() + ((7 - now.getDay()) * 86400000))
    let end_year = end_time.getFullYear()
    let end_month = end_time.getMonth() + 1
    let end_date = end_time.getDate()
    end_month = end_month < 10 ? '0' + end_month : end_month
    end_date = end_date < 10 ? '0' + end_date : end_date
    this.end_at = end_year + '年' + end_month + '月' + end_date + '日'
    this.get_report_weekly(this.start_at, this.end_at)
  },
  methods: {
    get_report_weekly (start_time, end_time) {
      start_time = start_time.replace(/年|月/g, '-').replace(/日/g, '')
      end_time = end_time.replace(/年|月/g, '-').replace(/日/g, '')
      reportService.get_client_weekly({start_at: start_time, end_at: end_time}).success((result) =>{
        if (result.error_code === 0) {
          let milestones_amounts = 0
          let weekstones_amounts = 0
          let work_hours = 0
          if (result.weekstones.length > 0) {
            result.weekstones.forEach((value) => {
              weekstones_amounts += value.actual_amount
              work_hours += value.shot_times
            })
          }
          if (result.milestones.length > 0) {
            result.milestones.forEach((value) => {
              milestones_amounts += value.actual_amount
            })
          }
          this.$set('work_hours', work_hours)
          this.$set('weekstones_amounts', weekstones_amounts)
          this.$set('milestones_amounts', milestones_amounts)
          this.$set('aggregate_amount', weekstones_amounts + milestones_amounts + result.bonus)
          this.$set('weekly_report', result)
        }
      })
    }
  },
  components: {
    calendar
  },
  watch: {
    start_at (value) {
      this.get_report_weekly(value, this.end_at)
    }
  }
})

vue.$set('test', 'll')
