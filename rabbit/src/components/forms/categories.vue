<template>
<h3 class="modal-title text-info text-center" id="myModalLabel">选择适合你的信息</h3>
<p class="yzj-size-14 yzj-top-distance10 text-center">最多选择10个你擅长的工作类别，认真地选择将大大增加需求方发现您的机会</p>
<p class="yzj-size-14 yzj-top-distance10 text-center">您已经选择了<span class="text-warning">{[ids.length]}</span>个分类，还可以选择<span class="text-warning">{[10-ids.length]}</span>个分类</p>
<form id="job-list" class="form-horizontal yzj-top-distance50 col-xs-11 col-xs-offset-1">
  <p class="yzj-size-16">选择类别：</p>
  <div class="col-xs-4 clear-both yzj-top-distance30 yzj-size-14" v-for="category in list">
    <h4 class="text-muted">
      <strong>{[category.category.name]}</strong>
    </h4>
    <p class="yzj-top-distance15" v-for="subcate in category.children">
    <input type="checkbox" id="cate-{[subcate.category_id]}" name="cate-{[subcate.category_id]}" v-bind:value="subcate.category_id" v-model="ids"/>{[subcate.name]}
    </p>
    <div class="clearfix"></div>
  </div>
  <div class="clearfix"></div>
  <div class="yzj-top-distance70 text-center">
    <button type="button" class="btn btn-primary btn-lg yzj-right-distance15" v-on:click="update_user_category()">保存</button>
    <button type="button" class="btn btn-default btn-lg yzj-right-distance15" v-on:click="close()">取消</button>
  </div>
  <div class="yzj-top-distance70"></div>
</form>
</template>

<script>
  import category_service from '../../service/category_service'
  import $ from 'jquery'
  import _ from 'underscore'
  export default {
    data () {
      return {
        list: [],
        ids: []
      }
    },
    created () {
      let _self = this
      category_service.get_category_list({category_id: 0, t: 'all'}).success((data) => {
        console.log(_self.categories, 'callback')
        let categories = data.categorys
        let result = {}
        for (let i = 0; i < categories.length; i++) {
          if (categories[i].pid === 0) {
            result[categories[i].category_id] = {category: categories[i]}
          }
        }
        let n = 0
        for (let i = 0; i < categories.length; i++) {
          if (categories[i].pid > 0) {
            if ($.inArray(_self.ids, categories[i].category_id)) {
              categories[i].checked = true
              n += 1
            } else {
              categories[i].checked = false
            }
            if (result[categories[i].pid].children) {
              result[categories[i].pid].children.push(categories[i])
            } else {
              result[categories[i].pid].children = [categories[i]]
            }
          }
        }
        if (n >= 10) {
          $('#job-list input[type=checkbox]').not('input:checked').attr('disabled', true)
        } else {
          $('#job-list input[type=checkbox]').not('input:checked').attr('disabled', false)
        }
        _self.list = result
        _self.origins = data.categorys
        _self.$dispatch('categories', data.categorys)
      })
    },
    props: ['current'],
    watch: {
      current (categories) {
        console.log(categories, 'categories')
        let ids = []
        for (let i = 0; i < categories.length; i++) {
          ids.push(categories[i].category_id)
        }

        this.ids = ids
        console.log(this.ids, 'ids')
      },
      ids (val) {
        if (val.length >= 10) {
          $('#job-list input[type=checkbox]').not('input:checked').attr('disabled', true)
        } else {
          $('#job-list input[type=checkbox]').not('input:checked').attr('disabled', false)
        }
      }
    },
    methods: {
      updateCurrent () {
        let result = []
        for (let i = 0; i < this.ids.length; i++) {
          let index = _.findIndex(this.origins, {category_id: this.ids[i]})
          result.push(this.origins[index])
        }
        this.current = result
      },
      update_user_category () {
        let _self = this
        category_service.update_user_category({category: this.ids.join(',')}).success((data) => {
          if (data.error_code === 0) {
            _self.$dispatch('save', 'categories_modal')
            _self.updateCurrent()
          } else {
            alert(data.msg)
          }
        })
      },
      close () {
        let _self = this
        _self.$dispatch('close', 'categories_modal')
      }
    }
  }
</script>
