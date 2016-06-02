import Vue from 'vue'
import $ from 'jquery'
import proposal_service from './service/proposal_service'
import mixin from './mixins/freelancer_proposal'
import datetime from './filters/datetime'

Vue.config.delimiters = ['{[', ']}']
Vue.use(datetime)

var vue = new Vue({
  el: '#proposals',
  mixins: [mixin],
  ready () {
    this.setData()
  },
  data: { },
  methods: {
    setData () {
      proposal_service.get_proposal_list({operate: 'interview'})
        .success($.proxy(this.handleData, this, 'interview'))
      proposal_service.get_proposal_list({operate: 'invite'})
        .success($.proxy(this.handleData, this, 'invite'))
      proposal_service.get_proposal_list({operate: 'active'})
        .success($.proxy(this.handleData, this, 'active'))
      proposal_service.get_proposal_list({operate: 'freeze'})
        .success($.proxy(this.handleData, this, 'freeze'))
    },
    unfreeze (id) {
      proposal_service.update_proposal({'proposal_id': id, 'operate': 'unfreeze'}).success((result) =>{
        if (result.error_code === 0) {
          $('.alert').html('激活成功')
          $('.alert').show()
          setTimeout(() =>{
            location.reload()
          }, 1000)
        }
      })
    }
  },
  computed: {
    is_null () {
      return !this.invite_list.length && !this.interview_list.length && !this.active_list.length && !this.freeze_list.length
    }
  }
})

vue.$set('name', 'hetao')
