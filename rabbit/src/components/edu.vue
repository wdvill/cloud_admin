<template>
  <div class="work-experience">
    <p class="text-primary yzj-size-16">
      {[itemout.degreename]}
      <span class="both-line">
        |
      </span>
      {[itemout.area]}
      <span class="both-line">
      <span class="both-line">
        |
      </span>
      {[itemout.school]}
      <span class="pull-right" v-if="ismyself">
        <img class="yzj-right-distance10 pointer" src="/static/images/edit-btn-icon.png" @click="edit(itemout)" >
        <img class="pointer" src="/static/images/del-btn-icon.png" data-toggle="modal" data-target="#eduModal">
      </span>
    </p>
    <p class="yzj-top-distance20 yzj-size-14">
      <span class="yzj-right-distance10">
        时间：{[itemout.start_at | year]} ---- {[itemout.end_at | year]}
      </span>
    </p>
    <p class="yzj-top-distance20 yzj-size-14 yzj-height30">
      简介：{[itemout.detail]}
    </p>
  </div>
  <div v-if="islast=='no'">
    <div class="line02">
    </div>
  </div>
  <confirm title="删除教育经历" msg="确定删除该教育经历么？" modal-id="eduModal" :ok-fn.sync="delete"></confirm>
</template>
<script>
  import confirm from './confirm.vue'
  
  export default {
    created () {
      // reset date
      this.itemout.start_at = /^\d{4}/.exec(this.itemout.start_at)[0]
      this.itemout.end_at = /^\d{4}/.exec(this.itemout.end_at)[0]
    },
    props: ['itemout', 'index', 'islast', 'ismyself'],
    methods: {
      edit (item_data) {
        this.$dispatch('edit', item_data, 'edu')
      },
      delete () {
        this.$dispatch('delete_edu', this.itemout)
      }
    },
    components: {
      confirm
    }
  }
</script>
