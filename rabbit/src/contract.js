import Vue from 'vue'
import $ from 'jquery'
import Cookies from 'js-cookie'
import fileService from './service/file_service'
import n from './utils/i18n'
Vue.config.delimiters = ['{[', ']}']

n.i18n().success((data) => {
  window.code = data.CODE
})

$.ajaxPrefilter(function (options, originalOptions, jqXHR) {
  try {
    options.data = $.param($.extend(originalOptions.data, { '_xsrf': Cookies.get('_xsrf') }))
  } catch (e) {
    console.log(e)
  }
})

var vue = new Vue({
  el: '#contract-create',
  data: {
    deposit_type: 'fixed', // fixed or milestone
    pay_type: 'hour', // hourly or fixed
    job_id: '',
    advanced: 0,
    milestones: [{}, {}],
    message: '',
    name_edited: false,
    hourly_edited: false,
    end_at: '',
    amount: 300,
    agree: 0,
    a: 1,
    b: 0,
    manual: false,
    avatar: 'http://7xr5pf.com1.z0.glb.clouddn.com/avatar-f4be93b3-8058-40ee-91b8-8b9948c9aede-1458708185.png',
    attachment: '',
    attachment_id: '',
    contract: {
      name: '',
      hourly: 50,
      workload: 1
    }
  },
  watch: {
    deposit_type (value, origin) {
      console.log(value)
    }
  },
  methods: {
    init (proposal) {
      this.$set('contract.name', proposal.job.name)
      this.$set('pay_type', proposal.job.paymethod)
      this.$set('job_id', proposal.job.id)
      this.$set('amount', proposal.price)
      this.$set('proposal', proposal)
      this.$set('avatar', proposal.user.freelancer.avatar)
      this.$set('name', proposal.user.freelancer.name)
      if (this.proposal.price) {
        this.contract.hourly = this.proposal.price
      }
    },
    show_v () {
      console.log(this.deposit_type, 'naa')
    },
    advanced_toggle () {
      console.log('hello', 'advanced')
      if (this.advanced) {
        this.advanced = 0
      } else {
        this.advanced = 1
      }
    },
    delRow (index) {
      this.milestones.splice(index, 1)
    },
    addRow () {
      this.milestones.push({})
    },
    onload_file () {
      let formData = new FormData()
      let f = $('#files')[0].files[0]
      formData.append('file', f)
      let params = '?t=contract'
      params += '&_xsrf=' + Cookies.get('_xsrf')
      fileService.upload(params, formData).success((result) =>{
        if (result.error_code === 0) {
          this.attachment_id = result.attachment_id
          this.attachment = result.name
        }
      })
    },
    save () {

      if (this.agree === 0) {
        alert('请同意各种协议')
        return
      }

      if (this.pay_type === 'hour') {

        if (this.contract.hourly === undefined || this.contract.hourly === '' || this.contract.hourly === '0') {
          alert('请填写时薪')
          return
        }

        if (this.contract.workload === undefined || this.contract.workload === '' || this.contract.workload === '0') {
          alert('请填写工作时长')
          return
        }

        if (this.start_at === undefined || this.start_at === '') {
          alert('请填写开始时间')
          return
        }

      } else {

        if (this.deposit_type === 'fixed') {

          if (this.amount === undefined || this.amount === '' || this.amount === '0') {
            alert('请填写项目预算')
            return
          }

          if (this.end_at === undefined || this.end_at === '') {
            alert('请填写项目结束时间')
            return
          }

        } else {

          for (let i = 0; i < this.milestones.length; i++) {
            let ms = this.milestones[i]
            let end_time = new Date(ms.end_at)
            if (end_time <= new Date().getTime()) {
              alert('里程碑项目结束时间不能为过去时间')
              return
            }
            let project_before = i
            let project_after = i + 1
            if (i > 0) {
              if (new Date(this.milestones[i - 1].end_at).getTime() >= new Date(ms.end_at).getTime()) {
                alert('里程碑' + project_after + '项目结束时间不能小于等于里程碑' + project_before + '项目结束时间')
                return
              }
            }
            if (ms.name === undefined || ms.name === '') {
              alert('请填写里程碑名称')
              return
            }

            if (ms.amount === undefined || ms.amount === '' || ms.amount === '0') {
              alert('请填写里程碑金额')
              return
            }

            if (ms.end_at === undefined || ms.end_at === '') {
              alert('请填写里程碑结束时间')
              return
            }

          }
        }
      }

      let offer = this.buildCommon()
      if (this.pay_type === 'hour') {
        $.extend(offer, this.buildHourData())
      } else {
        $.extend(offer, this.buildFixData())
        if (this.deposit_type === 'milestone') {
          $.extend(offer, this.buildMilestone())
        }
      }

      $.extend(offer, {'attachment_id': this.attachment_id})
      $.post('/api/contract', offer, function (data) {
        if (data.error_code === 0) {
          window.location.href = '/contracts/' + data.contract_id + '/' + data.ptype + '/' + data.trade_no
        } else {
          alert(window.code[data.error_code])
        }
      }, 'json')
    },
    editName () {
      this.name_edited = true
    },
    editHourly () {
      this.hourly_edited = true
    },
    milestoneAmount () {
      let amount = 0
      for (let i = 0; i < this.milestones.length; i++) {
        amount += this.milestones[i].amount * 1
      }

      return amount
    },
    buildCommon () {
      let offer = {}
      offer.user_id = this.proposal.user.freelancer.id
      offer.job_id = this.proposal.job.id
      offer.name = this.contract.name
      offer.message = this.message
      return offer
    },
    buildHourData () {
      return {
        hourly: this.contract.hourly,
        workload: this.contract.workload,
        start_at: this.start_at,
        manual: this.manual
      }
    },
    buildFixData () {
      if (this.end_at === '') {
        this.end_at = this.milestones[this.milestones.length - 1].end_at
      }
      return {
        end_at: this.end_at,
        amount: this.amount
      }
    },
    buildMilestone () {
      return {
        milestones: JSON.stringify(this.milestones),
        amount: this.milestoneAmount()
      }
    }
  }
})

$(function () {
  let init = function () {
    let path = location.pathname
    let regex = /clients.proposal.(\d+).offer/g
    let pattern = regex.exec(path)

    let proposal_id = pattern[1]

    initData(proposal_id)
  }

  let initData = function (proposal_id) {
    $.getJSON('/api/proposal', {proposal_id: proposal_id}, function (data) {
      if (data.error_code === 0) {
        let proposal = data.proposals[0]
        vue.init(proposal)
      }
    })
  }

  init()
})
