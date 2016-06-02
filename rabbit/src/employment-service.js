import Vue from 'vue'
import $ from 'jquery'
import alertdiv from './components/alert.vue'
import page from './directives/page.js'
import favoriteService from './service/favorite_service'

Vue.config.delimiters = ['{[', ']}']
Vue.use(page)

/* eslint-disable no-new */
new Vue({
  el: '#layout',
  data: {
    favorites: [],
    error_msg: '',
    pageObject: {itemsCount: 0, pageNo: 1, pageSize: 10}
  },
  ready () {
    this.employment_list_page()
  },
  components: {
    alertdiv
  },
  methods: {
    employment_list_page () {
      let data = {
        pagenum: this.pageObject.pageNo,
        pagesize: this.pageObject.pageSize
      }
      favoriteService.get_favorite_list(data).success((result) =>{
        if (result.error_code === 0) {
          this.favorites = result.favorites
          this.pageObject = {itemsCount: result.count, pageNo: data.pagenum, pageSize: data.pagesize}
        } else {
          $('#alert').modal('show')
          this.error_msg = result.msg
        }
      })
    }
  }
})
