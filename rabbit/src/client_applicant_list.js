import Vue from 'vue'
import $ from 'jquery'
import url from './utils/url'
import code from './utils/i18n'
import proposal_detail from './components/proposal/proposal_detail_modal.vue'
import error from './components/common/error_div.vue'
import commonService from './service/common_service'
import proposalService from './service/proposal_service'
import contractService from './service/contract_service'
import jobService from './service/job_service'
import sendMessage from './components/common/send_message.vue'
import YWORK from './utils/ywk'
import confirm from './components/confirm.vue'
import strapAlert from './components/strap_alert.vue'

Vue.config.delimiters = ['{[', ']}']

/* eslint-disable no-new */
new Vue({
  el: '#body',
  data: {
    show_page: {
      recommend: false,
      appli: true,
      msg: false,
      hire: false,
      archive: false
    },
    operate: 'active',
    job_id: '',
    location: '',
    pagesize: 5,
    pagenum: 1,
    counts: {
      active: 0,
      interview: 0,
      hire: 0,
      archive: 0
    },
    recommands: [],
    freelancers: [],
    archive_people: [],
    job_name: '',
    refuse_questions: [],
    archive_questions: [],
    archive_question: '',
    refuse_question: '',
    reason: '',
    proposal_id: '',
    proposal_detail: {},
    message: '',
    messages: '',
    invitee: '',
    invitee_name: '',
    favorite_target: '',
    favorite_message: '',
    confirm: {
      title: '关闭项目',
      msg: '是否确定关闭该项目?',
      okFn: null
    },
    alert: {
      msg: '',
      title: '',
      showType: 'danger',
      showAlert: false,
      callback: null
    }
  },
  ready () {
    let $this = this
    let $$location = location.href.split('/')[location.href.split('/').length - 1]
    $this.job_id = $$location.split('#')[0]
    $this.location = $$location.split('#')[1]
    $this.get_recommands()
    $this.select_count()
    $this.change_page($this.location)
    commonService.question({qtype: 'proposal_refuse_c'}).success((result) =>{
      if (result.error_code === 0) {
        $this.refuse_questions = result.questions
      }
    })
    commonService.question({qtype: 'proposal_archive'}).success((result) =>{
      if (result.error_code === 0) {
        $this.archive_questions = result.questions
      }
    })
    this.confirm.okFn = this.close_pro
  },
  components: {
    proposal_detail,
    error,
    sendMessage,
    strapAlert,
    confirm
  },
  methods: {
    get_recommands () {
      jobService.get_jobs_recommand({job_id: url.getLastId()}).success((result) =>{
        if (result.error_code === 0) {
          this.recommands = result.users
        }
      })
    },
    select_count () {
      contractService.select_bid({job_id: this.job_id, operate: 'active', pagesize: this.pagesize, pagenum: this.pagenum}).success((result) =>{
        this.counts.active = result.count
      })
      contractService.select_bid({job_id: this.job_id, operate: 'interview', pagesize: this.pagesize, pagenum: this.pagenum}).success((result) =>{
        this.counts.interview = result.count
      })
      contractService.select_bid({job_id: this.job_id, operate: 'hire', pagesize: this.pagesize, pagenum: this.pagenum}).success((result) =>{
        this.counts.hire = result.count
      })
      contractService.select_bid({job_id: this.job_id, operate: 'archive', pagesize: this.pagesize, pagenum: this.pagenum}).success((result) =>{
        this.counts.archive = result.count
      })
    },
    load (more) {
      let $this = this
      let datas = {
        job_id: $this.job_id,
        operate: $this.operate,
        pagesize: $this.pagesize,
        pagenum: $this.pagenum
      }
      code.i18n().then((data) =>{
        window['CODE'] = data.CODE
        window['COMMONS'] = data.COMMONS
        contractService.select_bid(datas).success((result) =>{
          if (result.error_code === 0 && result.proposals.length > 0) {
            if (!more) {
              if ($this.operate === 'archive') {
                $this.archive_people = []
              } else {
                $this.freelancers = []
              }
            }
            for (let i = 0;i < result.proposals.length;i++) {
              result.proposals[i].user.freelancer.status = result.proposals[i].status
              result.proposals[i].user.freelancer.status = result.proposals[i].status
              result.proposals[i].user.freelancer.contract_status = result.proposals[i].contract_status
              result.proposals[i].user.freelancer.ptype = result.proposals[i].ptype
              result.proposals[i].user.freelancer.archive = result.proposals[i].archive
              result.proposals[i].user.freelancer.proposal_id = result.proposals[i].proposal_id
              result.proposals[i].user.freelancer.price = result.proposals[i].price
              result.proposals[i].user.freelancer.message = result.proposals[i].message
              result.proposals[i].user.freelancer.duration = result.proposals[i].duration
              result.proposals[i].user.freelancer.attachment = result.proposals[i].attachment
              result.proposals[i].user.freelancer.paymethod = result.proposals[i].job.paymethod
              result.proposals[i].user.freelancer.contract_id = result.proposals[i].contract_id
              if ($this.operate === 'archive') {
                $this.archive_people.push(result.proposals[i].user.freelancer)
              } else {
                $this.freelancers.push(result.proposals[i].user.freelancer)
              }
            }
            $this.job_name = result.proposals[0].job.name
            $this.job_id = result.proposals[0].job.id
            $this.pagenum = result.pagenum
            if ($this.pagenum === Math.ceil(result.count / $this.pagesize)) {
              $('.loadMore').hide()
            }
          } else {
            $('.loadMore').hide()
            if (this.operate === 'active') {
              this.freelancers = []
            } else if (this.operate === 'archive') {
              this.archive_people = []
            }
          }
        })
      })
    },
    loadMore () {
      this.pagenum += 1
      this.load(true)
    },
    showBtns (event) {
      let $this
      if (event.target.nodeName === 'SPAN') {
        $this = $(event.target)
      } else if (event.target.nodeName === 'I') {
        $this = $(event.target).parent()
      } else {
        return
      }
      if ($this.hasClass('btn-arrow-down')) {
        $this.next().show()
        $this.removeClass('btn-arrow-down')
        $this.addClass('btn-arrow-up')
      } else {
        $this.next().hide()
        $this.removeClass('btn-arrow-up')
        $this.addClass('btn-arrow-down')
      }
    },
    hideList () {
      $('.operates').hide()
      $('.operates').prev().removeClass('btn-arrow-up')
      $('.operates').prev().addClass('btn-arrow-down')
    },
    send_message () {
      if (this.message === '') {
        return
      }
      contractService.send_message({proposal_id: this.proposal_id, content: this.message}).success((result) =>{
        if (result.error_code === 0) {
          $('.modal').modal('hide')
          this.freelancers = []
          this.load()
          this.select_count()
        }
      })
    },
    sendOffer (id) {
      window.location.href = '/clients/proposal/' + id + '/offer'
    },
    modalShow (name, id, person_name) {
      this.proposal_id = id
      $('#' + name).modal('show')
      if (name === 'send_invite') {
        this.invitee = id
        this.invitee_name = person_name
      }
      if (name === 'favorite') {
        this.favorite_message = ''
        $('.error-div').hide()
        this.favorite_target = id
      }
    },
    updateOffer (data) {
      let $this = this
      $this.freelancers = []
      contractService.update_bid(data).success((result) =>{
        $('.modal').modal('hide')
        if (result.error_code === 0) {
          $this.load()
          $('.alert').html('发送成功啦！').show()
          $('.alert').removeClass('alert-danger')
          $('.alert').addClass('alert-success')
          $('.alert').delay(3000).hide(0)
        } else {
          $('.alert').html('发送失败了，再试一次吧！').show()
          $('.alert').removeClass('alert-success')
          $('.alert').addClass('alert-danger')
          $('.alert').delay(3000).hide(0)
        }
      })
      this.select_count()
    },
    refuseOffer () {
      if (this.refuse_question === '') {
        return
      }
      let data = {
        proposal_id: this.proposal_id,
        operate: 'refuse',
        question_id: this.refuse_question,
        message: this.reason
      }
      this.updateOffer(data)
    },
    archiveOffer () {
      if (this.archive_question === '') {
        return
      }
      let data = {
        proposal_id: this.proposal_id,
        operate: 'archive',
        question_id: this.archive_question
      }
      this.updateOffer(data)
    },
    unfreezeOffer (id) {
      let data = {
        proposal_id: id,
        operate: 'unfreeze'
      }
      this.archive_people = []
      this.updateOffer(data)
    },
    select_detail (item) {
      this.proposal_detail = item
      $('#proposal_detail').modal('show')
      contractService.get_message_list({'proposal_id': item.proposal_id}).success((result) =>{
        if (result.error_code === 0 && result.messages) {
          this.$set('messages', result.messages)
        }
      })
    },
    change_page (type) {
      if (type !== '' && type !== undefined) {
        this.operate = type
      }
      if (type === 'recommend') {
        this.show_page.recommend = true
        this.show_page.appli = false
        this.show_page.archive = false
        this.show_page.msg = false
        this.show_page.hire = false
        return
      } else if (type === 'interview') {
        this.show_page.recommend = false
        this.show_page.appli = false
        this.show_page.archive = false
        this.show_page.msg = true
        this.show_page.hire = false
        this.freelancers = []
      } else if (type === 'hire') {
        this.show_page.recommend = false
        this.show_page.appli = false
        this.show_page.msg = false
        this.show_page.archive = false
        this.show_page.hire = true
        this.freelancers = []
      } else if (type === 'archive') {
        this.show_page.recommend = false
        this.show_page.appli = false
        this.show_page.msg = false
        this.show_page.archive = true
        this.show_page.hire = false
        this.archive_people = []
      } else {
        this.show_page.recommend = false
        this.show_page.appli = true
        this.show_page.archive = false
        this.show_page.msg = false
        this.show_page.hire = false
        this.operate = 'active'
        this.freelancers = []
      }
      this.load()
      if (this.operate === 'archive' || this.operate === 'interview' || this.operate === 'hire') {
        setTimeout(() =>{
          $('.archive-ul').each((index, item) =>{
            if ($(item).find('li').length > 0) {
              $(item).prev().removeClass('archive-class-down')
              $(item).prev().addClass('archive-class-up')
            }
          })
        }, 500)
      }
    },
    show_archive_class (event) {
      let $this
      if (event.target.nodeName === 'DIV') {
        $this = $(event.target)
      } else if (event.target.nodeName === 'I') {
        $this = $(event.target).parent()
      } else {
        return
      }
      if ($this.hasClass('archive-class-up')) {
        $this.removeClass('archive-class-up')
        $this.addClass('archive-class-down')
        $this.next().hide()
      } else {
        $this.removeClass('archive-class-down')
        $this.addClass('archive-class-up')
        $this.next().show()
      }
    },
    inviteOffer () {
      let data = {
        job_id: this.job_id,
        user_id: this.invitee,
        message: '你好！我想邀请你来申请我的项目，如果可以请认真阅读工作描述。'
      }
      proposalService.add_proposal(data).success((result) =>{
        if (result.error_code === 0) {
          this.get_recommands()
        }
        $('.modal').modal('hide')
      })
    },
    add_favorite () {
      if (this.favorite_message.length > 200) {
        $('.error-div .errorMsg').html('您输入的字数太多啦，精简一下吧！')
        $('.error-div').show()
        return
      }
      contractService.add_favorite({target_id: this.favorite_target, memo: this.favorite_message}).success((result) =>{
        if (result.error_code === 0) {
          if (this.operate === 'recommend') {
            this.get_recommands()
          } else {
            this.change_page(this.operate)
          }
          $('.modal').modal('hide')
        } else {
          $('.error-div .errorMsg').html('很遗憾备注失败了！')
          $('.error-div').show()
        }
      })
    },
    /* 关闭项目 */
    close_pro () {
      YWORK.putJson('/api/jobs/status', {job_id: this.job_id, status: 'close'}).success((result) => {
        if (result.error_code === 0) {
          this.show_alert('操作提示', '恭喜你，关闭项目成功!', 'success', () => {
            setTimeout(() => {
              window.location.href = '/clients/jobs/list'
            }, 2000)
          })
        } else {
          this.show_alert('错误提示', result.msg, 'danger')
        }
      })
    },
    /* 显示提示 */
    show_alert (title, msg, type, cb) {
      this.alert.title = title
      this.alert.msg = msg
      this.alert.showType = type
      this.alert.showAlert = true
      if (cb) {
        this.alert.callback = cb
      }
    }
  }
})
