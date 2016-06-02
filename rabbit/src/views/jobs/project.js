/**
 * 发布项目
 */
import Vue from 'vue'
import $ from 'jquery'
import _ from 'lodash'
import Simditor from 'simditor'
import YWORK from '../../utils/ywk.js'
import filter from '../../utils/filter.js'
import strapAlert from '../../components/strap_alert.vue'

Vue.config.delimiters = ['{[', ']}']

new Vue({
  el: '#project-new',
  data: {
    saveItem: {
      name: '',
      description: '',
      // 项目小分类
      category_id: '',
      hires: 1,
      level: '',
      paymethod: 'hour',
      duration: '',
      workload: '',
      attachment_id: '',
      api: '',
      platforms: '',
      frameworks: '',
      languages: '',
      skills: '',
      budget: '',
      stage: ''
    },
    // 默认展开上传附件操作
    expend: false,
    // 文件名称
    filename: '',
    job_id: '',
    // 雇佣项
    hiresIndex: 1,
    // 项目分类列表
    categorys: {},
    // 当前选中的项目大类
    categoryone: '',
    // 项目小分类
    category_id: 0,
    // 分类显示选项
    showItem: {},
    errCategory: '',
    // 选中适用平台集合
    platforms: [],
    // 选中的继承API集合
    apis: [],
    // 操作提示参数
    alert: {
      msg: '',
      title: '',
      showType: 'success',
      showAlert: false,
      cb: null
    },
    // 编辑器
    simditor: null,
    // 禁用按钮
    disableBtn: {
      normal: false,
      draft: false
    }
  },
  ready () {
    // 获取job_id,如果存在则代表修改
    let path = /\w{16}/g.exec(window.location.pathname)
    this.job_id = path && path.length > 0 ? path[0] : ''
    $.i18n().then((data) => {
      window.CODE = data.CODE
      window.COMMONS = data.COMMONS
      this.getCategory()
      // 初始化下拉数据
      this.$nextTick(() => {
        // 实例化编辑器
        this.simditor = new Simditor({
          textarea: $('#editor'),
          placeholder: '请输入工作描述',
          toolbarFloat: false,
          toolbarFloatOffset: 10,
          toolbar: ['title', 'bold', 'italic', 'underline', 'strikethrough', 'color', '|', 'ol', 'ul', 'blockquote', 'code', 'table', '|', 'link', 'image', '|', 'indent', 'outdent', 'alignment'],
          upload: {
            url: '/api/attachment',
            params: {t: 'article'},
            fileKey: 'file',
            connectionCount: 3,
            leaveConfirm: '正在上传文件'
          }
        })
        this.simditor.on('valuechanged', (e) => {
          this.saveItem.description = this.simditor.getValue()
          this.validate('description', 'errDescription', '请输入工作描述')
        })
        this.initSel('skills', 'select-skills')
        this.initSel('languages', 'select-languages')
        this.initSel('frameworks', 'select-frameworks')
      })
    })
    // 监听页面数据然后验证
    this.$watch('saveItem.level', (newVal, oldVal) => {
      this.validate('level', 'errLevel', '请选择服务方经验水平')
    })
    this.$watch('saveItem.skills', (newVal, oldVal) => {
      this.validate('skills', 'errSkill', '请选择技能')
    })
    this.$watch('saveItem.duration', (newVal, oldVal) => {
      this.validate('duration', 'errDuration', '请选择预计工作周期长度')
    })
    this.$watch('saveItem.workload', (newVal, oldVal) => {
      this.validate('workload', 'errWorkload', '请选择预计每周工作强度')
    })
  },
  methods: {
    /* 获取分类数据 */
    getCategory () {
      YWORK.postJson('/api/category', {
        category_id: 0,
        t: 'all'
      }).success((res) => {
        if (res.error_code === 0) {
          this.categorys = _.groupBy(res.categorys, 'pid')
        }
        // 如果存在项目id则查询项目数据
        if (this.job_id) {
          this.getJob()
        }
      })
    },
    /* 切换分类查询显示项目 */
    getShowItem (id) {
      if (!this.showItem[id]) {
        YWORK.getJson('/api/category/options', {
          category_id: id
        }).success((res) => {
          if (res.error_code === 0) {
            Vue.set(this.showItem, id, res.options)
          }
        })
      }
    },
    /* 绑定下拉列表数据 */
    initSel (data_id, id) {
      let datas = $('#' + data_id).val().split(',')
      let arr = datas.map((v) => {
        return {value: v, text: v}
      })
      $('#' + id).selectize({
        plugins: ['remove_button'],
        delimiter: ',',
        persist: false,
        maxItems: null,
        options: arr,
        create: false
      })
    },
    /* 查询项目信息 */
    getJob () {
      YWORK.getJson('/api/jobs', {job_id: this.job_id}).success((res) => {
        if (res.error_code === 0) {
          let job = res.job
          this.saveItem = job
          this.apis = job.api
          this.platforms = job.platforms
          this.categoryone = job.category.parent_id
          setTimeout(() => {
            this.saveItem.category_id = this.category_id = job.category.id
          }, 100)
          if (job.attachment.name) {
            this.expend = true
          }
          $('#select-skills').selectize()[0].selectize.setValue(this.saveItem.skills)
          $('#select-languages').selectize()[0].selectize.setValue(this.saveItem.languages)
          $('#select-frameworks').selectize()[0].selectize.setValue(this.saveItem.frameworks)
          this.simditor.setValue(filter.html_decode(this.saveItem.description))
        } else {
          this.showMAlert('错误提示', res.msg, 'danger', () => {
            setTimeout(() => {
              window.history.go(-1)
            }, 1500)
          })
        }
      })
    },
    /** 处理页面选中item */
    changeStatu (key, val) {
      let idx = this[key].indexOf(val)
      if (idx < 0) {
        this[key].push(val)
      } else {
        this[key].splice(idx, 1)
      }
    },
    /** 上传文件 */
    notifyFileInput (event) {
      let file = event.target.files[0]
      if (file.size > 5 * 1024 * 1024) {
        this.$set('errFile', '文件太大')
        return
      } else {
        this.errFile = ''
      }
      // 构建文件上传data
      let data = new FormData()
      data.append('file', file)
      data.append('t', 'job')
      YWORK.postFile('/api/attachment', data).success((res) => {
        this.errFile = ''
        if (res.error_code !== 0) {
          this.saveItem.attachment_id = ''
          this.filename = ''
          this.showMAlert('错误提示', res.msg, 'danger')
        } else {
          this.saveItem.attachment_id = res.attachment_id
          Vue.set(this.saveItem, 'attachment', res)
          this.filename = file.name
        }
      })
    },
    /** 显示操作提示内容 */
    showMAlert (title, msg, showType, cb) {
      this.alert.title = title
      this.alert.msg = msg
      this.alert.showType = showType
      this.alert.showAlert = true
      if (cb) {
        this.alert.cb = cb
      }
    },
    /** 生成保存的参数 */
    setSaveData () {
      this.saveItem.api = this.apis.join(',')
      this.saveItem.platforms = this.platforms.join(',')
      this.saveItem.description = this.simditor.getValue()
    },
    /** 检查页面必填参数是否完整 */
    ckForm () {
      let validates = [
        {key: 'category_id', errKey: 'errCategory', msg: '请选择分类'},
        {key: 'name', errKey: 'errName', msg: '请输入众包工作名称'},
        {key: 'description', errKey: 'errDescription', msg: '请输入工作描述'},
        {key: 'skills', errKey: 'errSkill', msg: '请选择技能'},
        {key: 'category_id', errKey: 'errCategory', msg: '请选择分类'},
        {key: 'level', errKey: 'errLevel', msg: '请选择服务方经验水平'}
      ]
      // 付款方式验证
      if (this.saveItem.paymethod === 'hour') {
        validates.push({key: 'duration', errKey: 'errDuration', msg: '请选择预计工作周期长度'})
        validates.push({key: 'workload', errKey: 'errWorkload', msg: '请选择预计每周工作强度'})
      } else {
        validates.push({key: 'budget', errKey: 'errBudget', msg: '请输入大于1的整数'})
      }
      if (this.category_id) {
        // 便利显示项目验证必填项
        var showD = this.showItem[this.category_id]
        // 判断所处阶段
        if (showD['stage'] && this.saveItem.stage === '') {
          validates.push({key: 'stage', errKey: 'errStage', msg: '请选择项目所处阶段'})
        }
        // 判断应用平台
        if (showD['platform'] !== '' && this.saveItem.platforms === '') {
          validates.push({key: 'platforms', errKey: 'errPlatform', msg: '请选择应用平台'})
        }
        // 判断集成API
        if (showD['api'] && this.saveItem.api === '') {
          validates.push({key: 'api', errKey: 'errApi', msg: '请选择集成API'})
        }
      }
      // 验证所有页面需要验证的元素
      let notVal = validates.filter((item) => {
        return !this.validate(item.key, item.errKey, item.msg)
      })
      console.log(notVal.length)
      if (notVal.length > 0) {
        return false
      }
      return true
    },
    /** 创建项目 */
    projectCreate (type) {
      this.setSaveData()
      // 检查页面参数
      if (!this.ckForm()) {
        return false
      }
      // 保存完的毁掉函数
      let cb = (res) => {
        console.log(res)
        if (res.error_code === 0) {
          this.showMAlert('操作提示', '恭喜你，项目发布成功!', 'success', () => {
            setTimeout(() => {
              if (type === 'draft') {
                window.location.href = '/clients/jobs'
              } else {
                window.location.href = '/jobs/new/complete/' + res.job_id
              }
            }, 1500)
          })
        } else {
          this.disableBtn[type] = false
          this.showMAlert('错误提示', res.msg, 'danger')
        }
      }
      // 保存操作
      this.disableBtn[type] = true
      if (!this.job_id) {
        YWORK.postJson('/api/jobs', this.saveItem).success((res) => {
          cb(res)
        })
      } else {
        Vue.set(this.saveItem, 'job_id', this.job_id)
        YWORK.putJson('/api/jobs', this.saveItem).success((res) => {
          cb(res)
        })
      }
      return false
    },
    /** 验证 */
    validate (key, errKey, msg) {
      // 处理编辑器
      if (key === 'description') {
        this.saveItem.description = this.simditor.getValue()
      }
      if ($.trim(this.saveItem[key]) === '') {
        this.$set(errKey, msg)
        return false
      } else {
        if (key === 'budget') {
          let reg = /^[1-9][0-9]*$/
          if (!reg.test(this.saveItem[key])) {
            this.$set(errKey, msg)
            return false
          } else {
            this[errKey] = ''
          }
        } else {
          this[errKey] = ''
        }
      }
      return true
    },
    /** 设置鼠标移入选择效果 */
    mouseoverItem (key) {
      this.$set('hover_' + key, true)
    },
    /* 设置鼠标移入选择效果 */
    mouseoutItem (key) {
      this['hover_' + key] = false
    }
  },
  watch: {
    /* 项目大类 */
    categoryone (val, oldval) {
      this.category_id = this.saveItem.category_id = this.categorys[this.categoryone] ? this.categorys[this.categoryone][0].category_id : ''
      this.validate('category_id', 'errCategory', '请选择分类')
    },
    /* 项目小分类 */
    category_id (val, oldval) {
      this.saveItem.category_id = val
      if (val) {
        this.getShowItem(val)
      }
    },
    /* 切换雇佣人数选择 */
    hiresIndex (val, oldval) {
      this.saveItem.hires = val
    }
  },
  components: {
    strapAlert
  }
})
