import Vue from 'vue'
import $ from 'jquery'
import alert from './components/alert.vue'
import contractService from './service/contract_service'
import questionService from './service/question_service'

Vue.config.delimiters = ['{[', ']}']
/* eslint-disable no-new */
new Vue({
  el: '#container',
  data: {
    role: '',
    contract_id: '',
    contract: '',
    question: [],
    question_id: '',
    score: '',
    evaluate: [],
    content: '',
    error_msg: ''
  },
  ready () {
    let paramArr = location.pathname.split('/')
    this.contract_id = paramArr[paramArr.length - 2]
    this.select_contract()
  },
  components: {
    alert
  },
  methods: {
    select_contract () {
      contractService.select_contract({contract_id: this.contract_id}).success((result) =>{
        if (result.error_code === 0) {
          this.contract = result.contracts[0]
        }
      })
      let qtype = ''
      if (this.role === 'c') {
        qtype = 'contract_finish_c'
      } else {
        qtype = 'contract_finish_f'
      }
      questionService.get_question_list({qtype: qtype}).success((result) =>{
        if (result.error_code === 0 && result.questions.length > 0) {
          this.question = result.questions
          this.question_id = result.questions[0].question_id
        }
      })
    },
    finish_contract () {
      let data = {}
      this.evaluate = []
      $('.start_list li>input').each((index, item) =>{
        this.evaluate.push($(item).val())
      })
      console.log(this.evaluate)
      if (this.score === '' || this.evaluate.indexOf('') !== -1) {
        $('#alert').modal('show')
        this.error_msg = '请完成所有评分'
        return
      }
      if (this.content === '' || this.content.length > 500) {
        $('#alert').modal('show')
        this.error_msg = '请输入少于500字的感受'
        return
      }
      if (this.role === 'c') {
        data = {
          contract_id: this.contract_id,
          question_id: this.question_id,
          score: this.score,
          exchange: this.evaluate[0],
          punctual: this.evaluate[1],
          cooper: this.evaluate[2],
          quality: this.evaluate[3],
          skill: this.evaluate[4],
          content: this.content
        }
      } else {
        data = {
          contract_id: this.contract_id,
          question_id: this.question_id,
          score: this.score,
          exchange: this.evaluate[0],
          cooper: this.evaluate[1],
          quality: this.evaluate[2],
          skill: this.evaluate[3],
          avail: this.evaluate[4],
          deliver: this.evaluate[5],
          content: this.content
        }
      }
      contractService.add_evaluate(data).success((result) =>{
        if (result.error_code === 0) {
          window.location.href = '/contracts/' + this.contract_id + '/feedback'
        } else {
          $('#alert').modal('show')
          this.error_msg = result.msg
        }
      })
    },
    add_feedback () {
      if (this.score === '') {
        $('#alert').modal('show')
        this.error_msg = '请完成所有评分'
        return
      }
      if (this.content === '') {
        $('#alert').modal('show')
        this.error_msg = '请输入附言'
        return
      }
      contractService.add_feedback({t: 'suggest', score: this.score, content: this.content}).success((result) =>{
        if (result.error_code === 0) {
          window.location.href = '/freelancers/contracts/' + location.pathname.split('/')[2]
        } else {
          $('#alert').modal('show')
          this.error_msg = result.msg
        }
      })
    }
  }
})
