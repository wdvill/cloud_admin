import Vue from 'vue'
import $ from 'jquery'
import datetime from './filters/datetime'
import string from './filters/string'
import Cookies from 'js-cookie'
import reportService from './service/report_service'
import n from './utils/i18n'
import calendar from './components/calendar.vue'
import page from './directives/page.js'
Vue.config.delimiters = ['{[', ']}']
Vue.use(datetime)
Vue.use(page)
Vue.use(string)
n.i18n().success((data) => {
  window.comments = data.COMMONS._margin_type
})

$.ajaxPrefilter(function (options, originalOptions, jqXHR) {
  try {
    options.data = $.param($.extend(originalOptions.data, { '_xsrf': Cookies.get('_xsrf') }))
  } catch (e) {
    console.log(e)
  }
})

new Vue({
  el: '#body',
  data: {
    end_at: '',
    start_at: '',
    pageObject: {itemsCount: 0, pageNo: 1, pageSize: 10},
    rtype: ''
  },
  ready () {
    // 当前日期
    let now = new Date()
    let end_year = now.getFullYear()
    let end_month = now.getMonth() + 1
    let end_date = now.getDate()
    end_month = end_month < 10 ? '0' + end_month : end_month
    end_date = end_date < 10 ? '0' + end_date : end_date
    this.end_at = end_year + '年' + end_month + '月' + end_date + '日'
    // 今天本周的第几天
    let that_time = new Date(now.getTime() - (30 * 86400000))
    let start_year = that_time.getFullYear()
    let start_month = that_time.getMonth() + 1
    let start_date = that_time.getDate()
    start_month = start_month < 10 ? '0' + start_month : start_month
    start_date = start_date < 10 ? '0' + start_date : start_date
    this.start_at = start_year + '年' + start_month + '月' + start_date + '日'
    this.get_trades(this.start_at, this.end_at, this.rtype)
  },
  methods: {
    get_trades (start_time, end_time, rtype) {
      start_time = start_time.replace(/年|月/g, '-').replace(/日/g, '')
      end_time = end_time.replace(/年|月/g, '-').replace(/日/g, '')
      let data = {}
      if (rtype !== '') {
        data = {start_at: start_time, end_at: end_time, report: true, pagenum: this.pageObject.pageNo, pagesize: this.pageObject.pageSize, rtype: rtype}
      } else {
        data = {start_at: start_time, end_at: end_time, report: true, pagenum: this.pageObject.pageNo, pagesize: this.pageObject.pageSize}
      }
      reportService.get_client_trade(data).success((result) => {
        if (result.error_code === 0) {
          this.$set('records', result)
          result.records.forEach((value) => {
            value.record_type = window.comments[value.record_type]
          })
          this.pageObject = {itemsCount: result.count, pageNo: result.pagenum, pageSize: data.pagesize}
        }
      })
    },
    recored_list (rtype) {
      this.pageObject = {itemsCount: 0, pageNo: 1, pageSize: 10}
      this.rtype = rtype
      this.get_trades(this.start_at, this.end_at, this.rtype, this.pageObject.pageNo, this.pageObject.pageSize)
    },
    searchperson: function () {
      this.get_trades(this.start_at, this.end_at, this.rtype, this.pageObject.pageNo, this.pageObject.pageSize)
    }
  },
  components: {
    calendar
  },
  watch: {
    start_at (value) {
      this.pageObject = {itemsCount: 0, pageNo: 1, pageSize: 10}
      this.get_trades(value, this.end_at, this.rtype, this.pageObject.pageNo, this.pageObject.pageSize)
    },
    end_at (value) {
      this.pageObject = {itemsCount: 0, pageNo: 1, pageSize: 10}
      this.get_trades(this.start_at, value, this.rtype, this.pageObject.pageNo, this.pageObject.pageSize)
    }
  }
})
