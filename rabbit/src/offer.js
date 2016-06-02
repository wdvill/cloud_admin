import Vue from 'vue'
import $ from 'jquery'
import datetime from './filters/datetime'
import Cookies from 'js-cookie'

Vue.config.delimiters = ['{[', ']}']
Vue.use(datetime)
$.ajaxPrefilter(function (options, originalOptions, jqXHR) {
  try {
    options.data = $.param($.extend(originalOptions.data, { '_xsrf': Cookies.get('_xsrf') }))
  } catch (e) {
    console.log(e)
  }
})

let contract_id = ''

var vue = new Vue({
  el: '#offer',
  data: {
    contracts: [],
    questions: [],
    revoke: []
  },
  ready () {
    contract_id = this.contract_id = location.href.split('/')[location.href.split('/').length - 1]

    let _self = this

    $.getJSON('/api/contract?timestamp=' + new Date().getTime(), {contract_id: _self.contract_id}, function (data) {
      if (data.error_code === 0) {
        let timeArr = data.contracts[0].create_at.split(' ')
        let d = timeArr[0].split('-')
        let t = timeArr[1].split(':')
        let deadline = new Date(d[0], (d[1] - 1), d[2], t[0], t[1], t[2])
        deadline = deadline.setTime(deadline.getTime() + 48 * 3600000)
        deadline = new Date(deadline)
        let year = deadline.getFullYear()
        let month = deadline.getMonth() + 1
        let date = deadline.getDate()
        let hour = deadline.getHours()
        let minute = deadline.getMinutes()
        let second = deadline.getSeconds()
        month = month < 10 ? '0' + month : month
        date = date < 10 ? '0' + date : date
        hour = hour < 10 ? '0' + hour : hour
        minute = minute < 10 ? '0' + minute : minute
        second = second < 10 ? '0' + second : second
        deadline = year + '-' + month + '-' + date + ' ' + hour + ':' + minute + ':' + second
        _self.$set('contract', data.contracts[0])
        _self.$set('deadline', deadline)
      }
    })
    $.getJSON('/api/question?timestamp=' + new Date().getTime(), {qtype: 'contract_refuse'}, function (data) {
      if (data.error_code === 0) {
        _self.$set('questions', data.questions)
      }
    })
    $.getJSON('/api/question?timestamp=' + new Date().getTime(), {qtype: 'contract_revoke'}, function (data) {
      if (data.error_code === 0) {
        _self.$set('revoke', data.questions)
      }
    })
  }
})

vue.$set('test', 'll')

$(function () {
  $('#accept-btn').click(function () {
    if ($('input[name="accept"]').is(':checked')) {
      $.ajax({
        method: 'put',
        url: '/api/contract',
        dataType: 'json',
        data: {
          contract_id: contract_id,
          status: 'accept',
          reason: $('#reason').val()
        }
      }).success((data) => {
        if (data.error_code === 0) {
          $('#accept').modal('hide')
          $('#tishi').modal('show')
        }
      })
    } else {
      console.log('no checked')
    }
  })
  $('#shut').click(function () {
    $('#tishi').modal('hide')
    window.location.reload()
  })
  $('#refuse-btn').click(function () {
    $.ajax({
      method: 'put',
      url: '/api/contract',
      dataType: 'json',
      data: {
        contract_id: contract_id,
        status: 'refuse',
        reason: $('#refuse-reason').val(),
        question_id: $('input[name="reason"]:checked').val()
      }
    }).success((data) => {
      if (data.error_code === 0) {
        $('#refuse').modal('hide')
        window.location.reload()
      } else {
        $('#refuse').modal('hide')
        alert(data.msg)
      }
    })
  })
  $('#revoke-btn').click(function () {
    $.ajax({
      method: 'put',
      url: '/api/contract',
      dataType: 'json',
      data: {
        contract_id: contract_id,
        status: 'revoke',
        reason: $('#revoke-reason').val(),
        question_id: $('input[name="reason"]:checked').val()
      }
    }).success((data) => {
      if (data.error_code === 0) {
        $('#cancel').modal('hide')
        window.location.reload()
      } else {
        $('#cancel').modal('hide')
        alert(data.msg)
      }
    })
  })
})
