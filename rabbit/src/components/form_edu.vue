<template>
<form class="form-horizontal yzj-top-distance50" id="edu-form">
  <h3 class="modal-title text-info text-center" id="myModalLabel">
    <span v-show="!item.id">添加</span><span v-show="item.id">编辑</span>教育经历
  </h3>
  <div class="form-group">
    <label for="inputEmail3" class="col-xs-offset-1 col-xs-2 control-label yzj-size-16">
      <span class="text-warning size-18">*</span>
          学校
    </label>
    <div class="col-xs-7">
        <input type="text" maxlength="30" class="form-control" placeholder="接受教育的学校名称" v-model="item.school" name="school">
    </div>
  </div>
  <div class="form-group form-error" for="school">
    <div class="col-xs-offset-3 col-xs-9 text-warning yzj-size-14">
      <span class="glyphicon glyphicon-exclamation-sign yzj-right-distance10"
      aria-hidden="true">
      学校名称必须为1~30字符
      </span>
    </div>
  </div>
  <div class="form-group">
    <label for="inputEmail3" class="col-xs-offset-1 col-xs-2 control-label yzj-size-16">
      <span class="text-warning size-18">*</span>
        年份
    </label>
    <div class="col-xs-7">
      <div class="col-xs-3 clear-both">
        <date_year :yearv.sync="item.start_at" v-ref:year></date_year>
      </div>
      <div class="col-xs-1 clear-both text-center yzj-height50">
        ——
      </div>
      <div class="col-xs-3 clear-both">
        <date_year :yearv.sync="item.end_at" v-ref:year></date_year>
      </div>
    </div>
  </div>
  <div class="form-group" v-show="errDateEdu">
    <div class="col-xs-offset-3 col-xs-9 text-warning yzj-size-14">
      <span class="glyphicon glyphicon-exclamation-sign yzj-right-distance10"
      aria-hidden="true">
      </span>
      {[errDateEdu]}
    </div>
  </div>
  <div class="form-group">
    <label for="inputEmail3" class="col-xs-offset-1 col-xs-2 control-label yzj-size-16">
      <span class="text-warning size-18"> * </span>
      学位
    </label>
    <div class="col-xs-7">
      <select class="form-control select-control" name="degree" v-model="item.degree">
        <option value="">
          --请选择--
        </option>
        <option value="senior">
          高中
        </option>
        <option value="college">
          大专
        </option>
        <option value="bachelor">
          本科
        </option>
        <option value="master">
          硕士
        </option>
        <option value="mba">
          MBA
        </option>
        <option value="emba">
          EMBA
        </option>
        <option value="doctor">
          博士
        </option>
        <option value="others">
          其他
        </option>
      </select>
    </div>
  </div>
  <div class="form-group form-error" for="degree">
    <div class="col-xs-offset-3 col-xs-9 text-warning yzj-size-14">
      <span class="glyphicon glyphicon-exclamation-sign yzj-right-distance10"
      aria-hidden="true">
      学位为必选项
      </span>
    </div>
  </div>
  <div class="form-group">
    <label for="inputEmail3" class="col-xs-offset-1 col-xs-2 control-label yzj-size-16">
      专业
    </label>
    <div class="col-xs-7">
      <input type="text" maxlength="30" class="form-control" placeholder="请填写自己的专业名称" v-model="item.area">
    </div>
  </div>
  <div class="form-group" v-show="errArea">
    <div class="col-xs-offset-3 col-xs-9 text-warning yzj-size-14">
      <span class="glyphicon glyphicon-exclamation-sign yzj-right-distance10"
      aria-hidden="true">
      </span>
      {[errArea]}
    </div>
  </div>
  <div class="clearfix"> </div>
  <div class="form-group">
    <label for="inputEmail3" class="col-xs-offset-1 col-xs-2 control-label yzj-size-16">
      简介
    </label>
    <div class="col-xs-7">
      <textarea class="form-control" rows="15" v-model="item.detail" maxlength="300">
      </textarea>
    </div>
  </div>
  <div class="form-group" v-show="errDetailEdu">
    <div class="col-xs-offset-3 col-xs-9 text-warning yzj-size-14">
      <span class="glyphicon glyphicon-exclamation-sign yzj-right-distance10"
      aria-hidden="true">
      </span>
      {[errDetailEdu]}
    </div>
  </div>
</form>
</template>

<script>
  import $ from 'jquery'
  import date_year from './date_year.vue'
  import Validate from '../form/validate'

  let validateObj = null

  export default {
    ready () {
      let items = {
        school: {
          minlength: 1,
          maxlength: 50
        },
        degree: {
          required: true
        }
      }
      validateObj = new Validate(items, $('#edu-form'))
    },
    methods: {
      save () {
        let _self = this
        if (!validateObj.validate()) {
          return
        }
        if (_self.item.id) {
          $.ajax({
            url: '/api/education',
            method: 'put',
            data: {
              eid: this.item.id,
              school: this.item.school,
              degree: this.item.degree,
              start_at: this.item.start_at,
              role: this.item.role,
              end_at: this.item.end_at,
              area: this.item.area,
              detail: this.item.detail
            },
            dataType: 'json'
          }).success((data) => {
            if (data.error_code === 0) {
              _self.$dispatch('close_modal')
            } else {
              alert(data.msg)
            }
          })
        } else {
          $.post('/api/education',
            {
              school: this.item.school,
              degree: this.item.degree,
              start_at: this.item.start_at,
              role: this.item.role,
              end_at: this.item.end_at,
              area: this.item.area,
              detail: this.item.detail
            }, 'json').success((data) => {
              if (/String/.test(toString.call(data))) {
                data = $.parseJSON(data)
              }
              console.log(data, 'edu response')
              if (data.error_code === 0) {
                _self.$dispatch('add_edu', _self.item)
                _self.$dispatch('close_modal')
              } else {
                alert(data.msg)
              }
            })
        }
      }
    },
    components: {
      date_year
    },
    props: ['item']
  }
</script>
