<template>
  <h3 class="modal-title text-info text-center" id="myModalLabel">
    <span v-show="!item.id">添加</span><span v-show="item.id">编辑</span>项目经验
  </h3>
  <validator name="validation">
  <form class="form-horizontal yzj-top-distance50">
    <div class="form-group">
      <label for="inputEmail3" class="col-xs-offset-1 col-xs-2 control-label yzj-size-16">
        <span class="text-warning size-18">
          *
        </span>
        项目名称
      </label>
      <div class="col-xs-7">
        <input type="text" maxlength="30" class="form-control" placeholder="请输入项目名称"
        v-model="item.name" id="name" v-validate:name="{'minlength': { rule: 1, initial: 'off' }, 'maxlength': 50}"
        maxlength="50">
      </div>
    </div>
    <div class="form-group" v-show="$validation.name.minlength || $validation.name.maxlength">
      <div class="col-xs-offset-3 col-xs-9 text-warning yzj-size-14">
        <span class="glyphicon glyphicon-exclamation-sign yzj-right-distance10"
        v-show="$validation.name.minlength">项目名称必须为1~50字符</span>
        <span class="glyphicon glyphicon-exclamation-sign yzj-right-distance10"
        v-show="$validation.name.maxlength">项目名称必须为1~50字符</span>
      </div>
    </div>
    <category v-bind:cateobj="item.category" v-ref:category></category>
    <div class="form-group">
      <label for="inputEmail3" class="col-xs-offset-1 col-xs-2 control-label yzj-size-16">
        <span class="text-warning size-18">
          *
        </span>
        项目简介
      </label>
      <div class="col-xs-7">
        <textarea class="form-control" maxlength="500" rows="10" id="detail" v-model="item.detail" v-validate:detail="{'required': { rule: true, initial: 'off' }}">
        </textarea>
      </div>
    </div>
    <div class="form-group" v-show="$validation.detail.required">
      <div class="col-xs-offset-3 col-xs-9 text-warning yzj-size-14">
        <span class="glyphicon glyphicon-exclamation-sign yzj-right-distance10"
        v-show="$validation.detail.required">项目简介不能为空</span>
      </div>
    </div>
    <div class="form-group">
      <label for="inputEmail3" class="col-xs-offset-1 col-xs-2 control-label yzj-size-16">
        完成时间
      </label>
      <div class="col-xs-7">
        <year_month :date.sync="item.end_at" v-ref:ymcom></year_month>
      </div>
    </div>
    <div class="form-group">
      <label for="inputEmail3" class="col-xs-offset-1 col-xs-2 control-label yzj-size-16">
        项目链接
      </label>
      <div class="col-xs-7">
        <input type="text" class="form-control" placeholder="请填写正确的地址格式" v-model="item.link">
      </div>
    </div>
    <upload :picturepath.sync="item.picture"></upload>
  </form>
  </validator>
</template>

<script>
import category from './category.vue'
import year_month from './year_month.vue'
import upload from './upload.vue'
import $ from 'jquery'

export default {
  data () {
    return {
      attachment_id: '',
      year: '',
      month: '',
      path: ''
    }
  },
  methods: {
    save () {
      this.$validate(true)
      let _self = this
      if (this.$validation.valid) {
        _self.item.category_id = _self.$refs.category.sub.selected.category_id
        _self.item.end_at = _self.$refs.ymcom.getValue()
        if (_self.attachment_id) {
          _self.item.picture_id = _self.attachment_id
          if (!_self.item.picture) {
            _self.item.picture = {}
          }
          _self.item.picture.path = _self.path
        }
        if (_self.item.id) {
          _self.item.pid = _self.item.id
          _self.item.category.parent_id = _self.$refs.category.top.selected.id
          _self.item.category.parent_name = _self.$refs.category.top.selected.name
          _self.item.category.id = _self.$refs.category.sub.selected.id
          _self.item.category.name = _self.$refs.category.sub.selected.name

          let formdata = $.extend({}, _self.item)
          if (!_self.attachment_id) {
            if (formdata.picture.path) {
              formdata.picture_id = formdata.picture.id
            } else {
              delete formdata.picture
            }
          }

          $.ajax({
            url: '/api/portfolio',
            method: 'put',
            dataType: 'json',
            data: formdata
          }).success((data) => {
            if (data.error_code === 0) {
              _self.$dispatch('update_project', _self.item)
              _self.$dispatch('close_modal')
            }
          })
        } else {
          _self.item.category = {}
          _self.item.category.parent_id = _self.$refs.category.top.selected.id
          _self.item.category.parent_name = _self.$refs.category.top.selected.name
          _self.item.category.id = _self.$refs.category.sub.selected.id
          _self.item.category.name = _self.$refs.category.sub.selected.name
          $.post('/api/portfolio', _self.item, (data) => {
            if (data.error_code === 0) {
              _self.item.id = data.portfolio_id
              _self.$dispatch('add_project', _self.item)
              _self.$dispatch('close_modal')
            }
          }, 'json')
        }
      }

    }
  },
  events: {
    upload_completed (attachment_id, path) {
      this.attachment_id = attachment_id
      this.path = path
    }
  },
  watch: {
    item (value) {
    }
  },
  props: ['item'],
  components: {
    category,
    year_month,
    upload
  }
}
</script>
