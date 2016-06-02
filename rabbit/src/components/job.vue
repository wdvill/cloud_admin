<template>
  <div class="work-experience">
    <p class="text-primary yzj-size-16">
      {[itemout.title]}
      <span class="both-line">
        |
      </span>
      {[itemout.company]}
      <span class="pull-right" v-if="ismyself">
        <img class="yzj-right-distance10 pointer" src="/static/images/edit-btn-icon.png"
        @click="edit(itemout)">
        <img class="pointer" src="/static/images/del-btn-icon.png" data-toggle="modal" data-target="#jobModal">
      </span>
    </p>
    <p class="yzj-top-distance20 yzj-size-14">
      <span class="yzj-right-distance10">
        时间：{[itemout.start_at | year_month]} ---- {[itemout.end_at | year_month]}
      </span>
      <span class="text-warning">
        {[itemout.role | role]}
      </span>
    </p>
    <p class="yzj-top-distance20 yzj-size-14 yzj-height30 yzj-word-break">
      工作描述：{[itemout.detail]}
    </p>
  </div>
  <div v-if="islast=='no'">
    <div class="line02">
    </div>
  </div>
  <confirm title="删除就业经历" msg="确定删除该就业经历么？" modal-id="jobModal" :ok-fn.sync="delete"></confirm>
</template>

<script>
  import role from '../filters/localize'
  import Vue from 'vue'
  import confirm from './confirm.vue'

  Vue.use(role)

  export default {
    created () {
      // reset date
      let regex = /^\d{4}-\d{2}/
      this.itemout.start_at = regex.exec(this.itemout.start_at)[0]
      this.itemout.end_at = regex.exec(this.itemout.end_at)[0]
    },
    data () {
      return {
        item: { text: 'text from experience' }
      }
    },
    props: ['itemout', 'index', 'islast', 'ismyself'],
    methods: {
      edit (item_data) {
        console.log('from experience none', item_data.name)
        this.$dispatch('edit', item_data, 'job')
      },
      delete () {
        this.$dispatch('delete_job', this.itemout)
      }
    },
    components: {
      confirm
    }
  }
</script>
