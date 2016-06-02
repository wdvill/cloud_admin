import $ from 'jquery'
import star from './components/job/star.vue'
import YWORK from './utils/ywk.js'
import _ from 'underscore'
import Vue from 'vue'

require('./assets/sass/views/jobs/find.scss')

let getValueByName = (name) => {
  let paramArr = location.search.substr(1).split('&')
  let parameter = {}
  for (let i = 0, len = paramArr.length; i < len; i++) {
    let param = paramArr[i].split('=')
    parameter[param[0]] = param[1]
  }
  return parameter[name] ? parameter[name] : ''
}

let employHistory = {
  level1: '没雇佣过',
  level2: '1-9人',
  level3: '10人以上'
}

var VM
$.i18n().then((data) => {
  window['CODE'] = data.CODE
  let COMMONS = data.COMMONS
  VM = new Vue({
    el: 'body',
    data: {
      globel: {},
      categories: [], // 项目父分类
      child_categories: [], // 项目子分类
      category_ids: [],
      current_parent: '',
      current_child: '',
      paymethods: [],
      levels: [],
      durations: [],
      workloads: [],
      works: [],
      keyword: '',
      pageObject: {
        itemsCount: 0,
        pageNo: 1,
        pageSize: 10
      },
      subscribes: [],
      time_sort: 'up',
      budget: {
        isHandle: false,
        starPoint: 0,
        min: {
          posx: -10,
          val: 0
        },
        max: {
          posx: 300,
          val: 200000
        }
      }
    },
    watch: {
      'category_ids' (val, oldVal) {
        this.query_work_list()
      },
      'paymethods' (val, oldVal) {
        this.query_work_list()
      },
      'levels' (val, oldVal) {
        this.query_work_list()
      },
      'durations' (val, oldVal) {
        this.query_work_list()
      },
      'workloads' (val, oldVal) {
        this.query_work_list()
      }
    },
    computed: {
      isShowHourOptions () {
        if (!this.paymethods.length) {
          return true
        }
        let str = this.paymethods.join()
        return str.indexOf('hour') > -1
      }
    },
    ready () {
      this.globel = COMMONS
      this.globel.level_price = {
        'entry': '<100元/小时',
        'middle': '100元-300元/小时',
        'expert': '>300元/小时'
      }
      this.globel.employHistory = employHistory
      YWORK.postJson('/api/category', {category_id: 0}).success((result) => {
        this.categories = result.categorys
      })

      this.keyword = decodeURI(getValueByName('q'))
      let pid = decodeURI(getValueByName('pid'))
      if (pid) {
        this.category_pid = pid
        this.select_child_category()
      }
      let cid = decodeURI(getValueByName('cid'))
      if (cid) {
        this.category_ids = [cid * 1]
      }
      this.query_work_list()
      this.subscribe_works()
    },
    methods: {
      query_work_list () {
        let data = {
          workload: this.workloads.join(','),
          duration: this.durations.join(','),
          level: this.levels.join(','),
          paymethod: this.paymethods.join(','),
          categorys: this.category_ids.join(','),
          pagesize: 10,
          keyword: this.keyword,
          pagenum: this.pageObject.pageNo
        }

        // 过滤当单独选择工作类型，对应其他筛选条件不生效
        if (this.paymethods.length === 1) {
          if (this.paymethods[0] === 'fixed') {
            data.workload = ''
          }
        }

        YWORK.postJson('/api/jobs/search', data, 'application/json').success((result) => {
          this.pageObject = {
            itemsCount: result.count,
            pageNo: result.pagenum,
            pageSize: data.pagesize
          }
          this.works = result.jobs
          _.sortBy(this.works, 'create_at')
        })
        this.remeber()
      },
      remeber () {
        if (localStorage) {
          let old = localStorage.getItem('search_keywords')
          let current = []
          if (old && this.keyword) {
            old = old.split(',')
            old.push(this.keyword)
            current = $.unique(old)
            if (current.length > 5) {
              current = current.splice(current.length - 5, 5)
            }
            localStorage.setItem('search_keywords', current)
          } else if (this.keyword) {
            localStorage.setItem('search_keywords', this.keyword)
          }

        }
      },
      sortByTime () {
        if (this.time_sort === 'up') {
          this.time_sort = 'down'
          this.works.reverse()
        } else {
          this.time_sort = 'up'
          this.works.reverse()
        }
      },
      select_child_category () {
        console.log(this.category_pid)
        if (!this.category_pid) {
          return
        }
        YWORK.postJson('/api/category', {category_id: this.category_pid}).success((result) => {
          this.child_categories = result.categorys
          if (_.findIndex(this.child_categories, {category_id: this.category_ids[0] * 1}) < 0) {
            this.category_ids = []
          }
        })
      },
      search () {
        this.query_work_list()
        $('#addSubscribe').attr('disabled', false)
        $('#addSubscribe').html('+  添加到我的订阅')
      },
      enter (event) {
        if (event.keyCode === 13) {
          event.stopPropagation()
          event.preventDefault()
          this.query_work_list()
          $('#addSubscribe').attr('disabled', false)
          $('#addSubscribe').html('+  添加到我的订阅')
        }
      },
      collect (item) {
        data = {
          target_id: item.id
        }
        if (item.favorite) {
          YWORK.deleteJson('/api/favorite', data, 'application/json').success((result) => {
            if (result.error_code === 0) {
              item.favorite = false
            }
          })
        } else {
          YWORK.postJson('/api/favorite', data, 'application/json').success((result) => {
            if (result.error_code === 0) {
              item.favorite = true
            }
          })
        }
      },
      subscribe_works () {
        YWORK.getJson('/api/subscribe', {}, 'application/json')
          .success((result) => {
            if (result.error_code === 0) {
              this.subscribes = result.subscribes
            }
          })
      },
      /* 添加订阅 */
      subscribe () {
        if (this.keyword === '') {
          return
        }
        for (let i = 0; i < this.subscribes.length; i++) {
          if (this.subscribes[i].name === this.keyword) {
            return
          }
        }
        let data = {
          name: this.keyword,
          duration: this.durations.join(),
          workload: this.workloads.join(),
          paymethod: this.paymethods.join(),
          level: this.levels.join(),
          keyword: this.keyword
        }
        YWORK.postJson('/api/subscribe', data, 'application/json')
          .success((result) => {
            if (result.error_code !== 0) {
              alert(result.msg)
            } else {
              $('#addSubscribe').attr('disabled', true)
              $('#addSubscribe').html('已添加')
            }
          })
      },
      starHandle (e) {
        this.budget.isHandle = true
        this.budget.starPoint = e.clientX
        console.log(this.budget.isHandle)
      },
      moveHandle (e) {
        if (this.budget.isHandle) {
          let range = e.clientX - this.budget.starPoint
          let posx = this.budget.min.posx
          console.log(range, range)
          this.budget.min.posx = posx + range
        }
      },
      endHandle () {
        this.budget.isHandle = false
        console.log(this.budget.isHandle)
      }
    },
    components: {
      star
    }
  })
})

var $document = $(document)

$document.on('mousedown', '.min-handle', (e) => {
  VM.budget.isHandle = true
  VM.budget.starPoint = e.clientX
  console.log(e.clientX)
})
$document.on('mousemove', (e) => {
  if (VM.budget.isHandle) {
    let starPoint = VM.budget.starPoint
    let range = e.clientX - starPoint
    VM.budget.min.posx = range
    console.log(range)
  }
})
$document.on('mouseup', (e) => {
  VM.budget.isHandle = false
  console.info(e.clientX)
})
