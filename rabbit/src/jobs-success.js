import Vue from 'vue'
import $ from 'jquery'

var uuid = window.location.pathname.split('/')[3]
var mid = parseInt(window.location.pathname.split('/')[4], 10)
console.log(uuid, mid)
Vue.config.delimiters = ['{[', ']}']
var vue = new Vue({
  el: '#my-submit',
  data: {
    stone: {},
    uuid: uuid
  },
  methods: {
    getStone (id) {
      var that = this
      that.stones.forEach((value)=>{
        if (value.id === id) {
          that.$set('nowStone', value)
        }
      })
    },
    getRecords () {
      var that = this
      let message = []
      let attachments = []
      this.stone.records.forEach((value)=>{
        if (value.message !== '' && value.reason !== '') {
          message.push({time: value.audit_at, content: that.contract.user.client.name + '：' + value.reason})
          message.push({time: value.create_at, content: that.contract.user.freelancer.name + '：' + value.message})
        } else if (value.message !== '' && value.reason === '') {
          message.push({time: value.create_at, content: that.contract.user.freelancer.name + '：' + value.message})
        }
      })
      this.stone.records.forEach((value)=>{
        if (value.attachment.name !== undefined && value.audit_attachment.name !== undefined) {
          attachments.push({name: value.attachment.name, path: value.attachment.path})
          attachments.push({name: value.audit_attachment.name, path: value.audit_attachment.path})
        } else if (value.attachment.name !== undefined && value.audit_attachment.name === undefined) {
          attachments.push({name: value.attachment.name, path: value.attachment.path})
        } else if (value.attachment.name === undefined && value.audit_attachment.name !== undefined) {
          attachments.push({name: value.audit_attachment.name, path: value.audit_attachment.path})
        }
      })
      that.$set('message', message)
      that.$set('attachments', attachments)
    },
    getAttachs (attachments) {
      var that = this
      this.stone.records.forEach((value)=>{
        if (value.attachment.name !== undefined) {
          let attach = {}
          attach.name = value.attachment.name
          attach.path = value.attachment.path
          attachments.push(attach)
        }
      })
      that.$set('attachs', attachments)
    }
  }
})

$.getJSON('/api/milestone', {timestamp: new Date().getTime(), contract_id: uuid, milestone_id: mid}, function (data) {
  if (data.error_code === 0) {
    console.log(data)
    let attachments = []
    vue.$set('stone', data.milestones[0])
    vue.getAttachs(attachments)
    console.log(vue.$data.attachs, 'attachments')
  }
})
$.getJSON('/api/contract', {timestamp: new Date().getTime(), contract_id: uuid}, function (data) {
  if (data.error_code === 0) {
    console.log(data, 'contract')
    vue.$set('contract', data.contracts[0])
    vue.getRecords()
  }
})
