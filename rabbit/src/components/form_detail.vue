<template>
  <h3 class="modal-title text-info text-center" id="myModalLabel">
    个人简介
  </h3>
  <div class="yzj-top-distance50 col-xs-offset-2 clear-left col-xs-8 clear-right yzj-size-14">
    <p class="yzj-size-16">在个人简介里您可以向需求方展示您所拥有的技能和经验。</p>
    <p class="yzj-top-distance15">描述您的优势和技能</p>
    <p class="yzj-top-distance15">展示曾经出色的项目经验，成就以及您的教育经历</p>
    <p class="yzj-top-distance15">尽量简洁，不要出错</p>
  </div>
  <div class="clearfix"></div>
  <form class="form-horizontal yzj-top-distance20">
    <div class="col-xs-offset-2 clear-both col-xs-8">
      <textarea class="form-control" rows="9" v-model="item"  placeholder="可以使用多种软件，如Axure RP Por ，Min的jet MindManager等，耐心和很棒创造力！" >{[item]}</textarea>
    </div>
    <div class="clearfix"></div>
  </form>
</template>
<script>
export default {
  data () {
    return {
    }
  },
  methods: {
    save () {
      this.$dispatch('update_detail', this.item)
      this.$dispatch('close_modal')
    }
  },
  props: ['item']

}
</script>
