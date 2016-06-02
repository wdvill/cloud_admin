import Vue from 'vue'
import $ from 'jquery'
import star from './components/job/star.vue'
import YWORK from './utils/ywk.js'

$.i18n().then((data) => {
  window['CODE'] = data.CODE
  let COMMONS = data.COMMONS
  new Vue({
    el: 'body',
    data: {
      globel: {},
      works: [],
      noPage: false,
      pageObject: {
        itemsCount: 0,
        pageNo: 1,
        pageSize: 10
      }
    },
    ready () {
      this.globel = COMMONS
      this.query_work_list()
    },
    methods: {
      query_work_list (pageNo) {
        let data = {
          pagesize: 10,
          pagenum: this.pageObject.pageNo
        }
        if (pageNo) {
          data.pagenum = pageNo
        }
        YWORK.getJson('/api/favorite', data, 'application/json').success((result) => {
          if (result.favorites.length < data.pagesize) {
            this.noPage = true
          }
          this.pageObject = {
            itemsCount: result.count,
            pageNo: result.pagenum,
            pageSize: data.pagesize
          }
          for (let i = 0; i < result.favorites.length; i++) {
            result.favorites[i].job.show = true
            this.works.push(result.favorites[i].job)
          }
        })
      },
      del_collect (item) {
        let data = {
          target_id: item.id
        }
        if (item.show) {
          YWORK.deleteJson('/api/favorite', data, 'application/json').success((result) => {
            if (result.error_code === 0) {
              item.show = false
            }
          })
        } else {
          YWORK.postJson('/api/favorite', data, 'application/json').success((result) => {
            if (result.error_code === 0) {
              item.show = true
            }
          })
        }
      }
    },
    components: {
      star
    }
  })
})
