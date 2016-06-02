<template>
   <h3 class="modal-title text-info text-center" id="myModalLabel">
    工作状态
  </h3>
  <form class="form-horizontal yzj-top-distance50 col-xs-offset-2 clear-left">
    <h4 class="text-info"><strong>我当前的工作状态</strong></h4>
    <div class="yzj-top-distance30 yzj-size-16 text-info">
      <input type="radio" name="work" v-model="item" value="0"/>我现在不想工作
    </div>
    <div class="yzj-top-distance20 yzj-size-16 text-info">
      <input type="radio" name="work" v-model="item" value="1"/>每周可工作30小时以上
    </div>
    <div class="yzj-top-distance20 yzj-size-16 text-info">
      <input type="radio" name="work" v-model="item" value="2"/>每周可工作30小时以下
    </div>
    <div class="yzj-top-distance20 yzj-size-16 text-info">
      <input type="radio" name="work" v-model="item" value="3"/>根据需求者要求
    </div>
  </form>
  <div class="modal-footer">
      <div class="col-xs-10 col-xs-offset-2">
        <div class="col-xs-4">
          <button type="button" class="btn btn-primary btn-block yzj-right-distance15"
          v-on:click="save()">
          保存
          </button>
        </div>
        <div class="col-xs-4">
          <button type="button" class="btn btn-default btn-block yzj-right-distance15"
            data-dismiss="modal" v-on:click="close()">
            取消
          </button>
        </div>
      </div>
    </div>
</template>
<script>
export default {
  data () {
    return {
    }
  },
  methods: {
    save () {
      this.$dispatch('update_workload', this.item)
    },
    close () {
      this.$dispatch('close', 'workload_modal')
    }
  },
  props: ['item']

}
</script>
