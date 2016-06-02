<template>
<div class="form-group">
  <label for="inputEmail3" class="col-xs-offset-1 col-xs-2 control-label yzj-size-16">
    <span class="text-warning size-18">
      *
    </span>
    身份角色
  </label>
  <div class="col-xs-7">
    <select class="form-control select-control" id="role" v-model="role" name="role">
      <option v-for="option in roles" v-bind:value="option.id">
        {[ option.name ]}
      </option>
    </select>
  </div>
</div>
<div class="form-group form-error" for="role">
  <div class="col-xs-offset-3 col-xs-9 text-warning yzj-size-14">
    <span class="glyphicon glyphicon-exclamation-sign yzj-right-distance10"
    aria-hidden="true">
    角色是必选字段
  </span>
</div>
</template>
<script>
  export default {
    created () {
      console.log('props', this.role)
    },
    data () {
      return {
        roles: [
          { id: 1, name: '实习生' },
          { id: 2, name: '普通员工' },
          { id: 3, name: '主管' },
          { id: 4, name: '经理' },
          { id: 5, name: '总经理' },
          { id: 6, name: '创始人' }
        ]
      }
    },
    props: ['role']
  }
</script>
