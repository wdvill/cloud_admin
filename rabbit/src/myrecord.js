import $ from 'jquery'
import Vue from 'vue'
import datetime from './filters/datetime'
import lan from './filters/lan'
import Cookies from 'js-cookie'
import VueValidator from 'vue-validator'
import edit from './components/edit.vue'
import experience from './components/experience.vue'
import job from './components/job.vue'
import edu from './components/edu.vue'
import strapAlert from './components/strap_alert.vue'
import YWORK from './utils/ywk.js'
import confirm from './components/confirm.vue'

Vue.use(VueValidator)
Vue.use(datetime)
Vue.use(lan)
Vue.config.delimiters = ['{[', ']}']

$.ajaxPrefilter(function (options, originalOptions, jqXHR) {
  try {
    options.data = $.param($.extend(originalOptions.data, { '_xsrf': Cookies.get('_xsrf') }))
  } catch (e) {
    console.log(e)
  }
})

$.i18n().then((configs) => {
  window['CODE'] = configs.CODE
  window['COMMONS'] = configs.COMMONS

  var vue = new Vue({
    el: 'body',
    data: {
      items: [],
      jobs: [],
      errMsg: '',
      showType: 'danger',
      curLanguage: {},
      showAlert: false,
      profile: {},
      start_skills: []
    },
    methods: {
      addProject () {
        this.$refs.profile.test({}, 'item')
      },
      addJob () {
        this.$refs.profile.test({}, 'job')
      },
      addEdu () {
        this.$refs.profile.test({}, 'edu')
      },
      addLanguage () {
        this.$refs.profile.test({}, 'language')
      },
      editWorkload () {
        this.profile.workload = this.profile.available ? this.profile.workload : '0'
        this.$refs.profile.test(this.profile.workload, 'workload')
      },
      editDetail () {
        this.$refs.profile.test(this.profile.overview, 'detail')
      },
      editSkills () {
        this.$refs.profile.test(this.profile.skills, 'skills')
      },
      editLanguage (language) {
        this.$refs.profile.test(language, 'language')
      },
      selectLanguage (language) {
        this.curLanguage = language
        $('#lanModal').modal('show')
      },
      /* 删除语言 */
      deleteLanguage () {
        for (let i = 0; i < this.profile.languages.length; i++) {
          if (this.profile.languages[i].name === this.curLanguage.name) {
            this.profile.languages.splice(i, 1)
            break
          }
        }
        delete this.profile.other[this.curLanguage.name]
        this.updateProfile()
      },
      editHourly () {
        this.$refs.profile.test(this.profile.hourly, 'hourly')
      },
      editBase () {
        this.$refs.profile.test({title: this.profile.title, location: this.profile.location}, 'base')
      },
      updateProfile (dataClone) {
        let formData = {}
        let profile = dataClone ? $.extend({}, dataClone) : $.extend({}, this.profile)
        profile.skills = profile.skills.join()
        for (let key in profile) {
          if (profile.hasOwnProperty(key)) {
            formData[key] = profile[key]
          }
        }
        formData.other = JSON.stringify(this.profile.other)
        $.ajax({
          url: '/api/user/profile',
          method: 'put',
          dataType: 'json',
          data: formData
        }).success((data) => {
          if (data.error_code === 0) {
            this.$set('start_skills', this.profile.skills)
          } else {
            alert(data.msg)
          }
        })
      },
      /* 提示信息 */
      showSAlert (msg, showType = 'danger') {
        this.errMsg = msg
        this.showType = showType
        this.showAlert = true
      },
      /** 删除公用方法
       * 删除公用方法
       * @params {
       *   key[String] 需要请求的接口对象
       *   item[Object] 当前删除项
       *   itemArr[Array] 被删除的对象数组
       * }
       */
      delFn (key, item, itemArr) {
        // 调用api删除
        YWORK.deleteJson(`/api/${key}`, {eid: item.id}, 'application/json')
        .success((res) => {
          if (res.error_code === 0) {
            // 删除页面展示的当前项
            for (let i = 0; i < itemArr.length; i++) {
              if (itemArr[i].id === item.id) {
                itemArr.splice(i, 1)
                break
              }
            }
          } else {
            this.errMsg = '删除失败，请再试一次！'
            this.showAlert = true
          }
        })
      }
    },
    components: {
      experience,
      edit,
      edu,
      job,
      strapAlert,
      confirm
    },
    events: {
      edit (dataModel, type) {
        this.$refs.profile.test(dataModel, type)
      },
      add_project (item) {
        this.items.push(item)
      },
      add_job (job) {
        this.jobs.push(job)
      },
      add_edu (job) {
        job.degreename = window['COMMONS']._degree[job.degree]
        this.edus.push(job)
      },
      add_language (row) {
        for (let key in row) {
          if (this.profile.other[key]) {
            for (let i = 0; i < this.profile.languages.length; i++) {
              if (this.profile.languages[i].name === key) {
                this.profile.languages[i].level = row[key]
                break
              }
            }
            this.profile.other[key] = row.level
          } else {
            this.profile.languages.push({
              name: key,
              level: row[key]
            })
          }
          this.profile.other = $.extend(this.profile.other, row)
        }
        this.updateProfile()
      },
      delete_project (item) {
        for (let i = 0; i < this.items.length; i++) {
          if (this.items[i].id === item.id) {
            this.items.splice(i, 1)
            break
          }
        }
      },
      /* 删除工作经历 */
      delete_job (job) {
        this.delFn('employment', job, this.jobs)
      },
      update_workload (workload) {
        if (workload === '0') {
          this.profile.available = false
          // 没有为0的状态，默认给1
          // this.profile.workload = 1
        } else {
          this.profile.available = true
          this.profile.workload = workload
        }
        this.updateProfile()
      },
      update_detail (overview) {
        this.profile.overview = overview
        this.updateProfile()
      },
      update_skills (skills) {
        console.log(skills, 'skill')
        this.profile.skills = skills
        this.updateProfile()
      },
      update_hourly (hourly) {
        this.profile.hourly = hourly
        this.updateProfile()
      },
      update_base (base) {
        this.profile.title = base.title
        this.profile.location = base.location
        let formData = $.extend({}, this.profile)
        formData.location = this.profile.location.location_id
        console.log('update base', formData)
        this.updateProfile(formData)
      },
      /* 删除教育经历 */
      delete_edu (edu) {
        this.delFn('education', edu, this.edus)
      },
      update_project (item) {
        for (let i = 0; i < this.items.length; i++) {
          if (this.items[i].id === item.id) {
            this.items.splice(i, 1, item)
            break
          }
        }
      },
      /* 提示信息 */
      show_alert (msg, showType = 'danger') {
        this.errMsg = msg
        this.showType = showType
        this.showAlert = true
      }
    }
  })
  // 时间戳
  let time = +new Date()
  $.getJSON('/api/portfolio', (data) => {
    vue.$set('items', data.portfolios)
  })
  $.getJSON('/api/employment?time=' + time).success((data) => {
    vue.$set('jobs', data.employments)
  })
  $.getJSON('/api/education?time=' + time).success((data) => {
    for (let i = 0; i < data.educations.length; i++) {
      data.educations[i].degreename = window['COMMONS']._degree[data.educations[i].degree]
    }
    vue.$set('edus', data.educations)
  })
  $.getJSON('/api/user/profile?time=' + time).success((data) => {
    data.profile.other = {}
    if (data.profile.languages) {
      for (let i = 0; i < data.profile.languages.length; i++) {
        data.profile.other[data.profile.languages[i].name] = data.profile.languages[i].level
      }
    }
    vue.$set('profile', data.profile)
    vue.$set('start_skills', new Array(...data.profile.skills))
  })
})

