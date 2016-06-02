<template>
  <h3 class="modal-title text-info text-center" id="myModalLabel">
    价格
  </h3>
<div class="yzj-top-distance70 col-xs-offset-2 col-xs-8 clear-both">
  <div class="text-info yzj-size-16">
    <div class="col-xs-5 clear-left">
       网站显示
       <p class="yzj-top-distance10 yzj-size-14">需求者看到的您的标价</p>
    </div>
    <div class="col-xs-1 clear-both">
      <img class="yzj-top-distance10" src="/static/images/rmb-icon.png">
    </div>
    <div class="col-xs-4">
       <input type="number" max="99999.99" min="1" class="form-control" v-model="item" />
    </div>
    <div class="col-xs-2 clear-both yzj-top-distance15">
      <label class="control-label">/小时</label>
    </div>
  </div>
  <div class="clearfix"></div>
  <div class="text-info yzj-size-16 yzj-top-distance30">
    <div class="col-xs-5 clear-left">
      实际收益
      <p class="yzj-top-distance10 yzj-size-14">你实际获得的回报</p>
    </div>
    <div class="col-xs-1 clear-both">
      <img class="yzj-top-distance10" src="/static/images/rmb-icon.png">
    </div>
    <div class="col-xs-4">
       <input type="number" disabled="true" class="form-control" v-model="real_amount"/>
    </div>
    <div class="col-xs-2 clear-both yzj-top-distance15">
      <label class="control-label">/小时</label>
    </div>
  </div>
  <div class="clearfix yzj-bot-distance50"></div>
</template>
<script>
export default {
  data () {
    return {
      real_amount: (this.item * 0.9).toFixed(2)
    }
  },
  ready () {
    this.real_amount = (this.item * 0.9).toFixed(2)
  },
  methods: {
    save () {
      let regular = /^(\d{1,5}\.{1}\d{0,2}|\d{1,5})$/
      if (!regular.test(this.item)) {
        this.$dispatch('show_alert', '时薪必须是最多两位小数且小于6位的数字')
        return
      }
      this.$dispatch('update_hourly', this.item)
      this.$dispatch('close_modal')
    }
  },
  props: ['item'],
  watch: {
    item (val, oldval) {
      this.real_amount = (val * 0.9).toFixed(2)
    }
  }
}
</script>
