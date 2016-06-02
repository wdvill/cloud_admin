<template>
  <h3 class="modal-title text-info text-center" id="myModalLabel">
    擅长技能
  </h3>
  <div class="clearfix"></div>
  <form class="form-horizontal yzj-top-distance50">
    <div class="col-xs-2" style="font-size:14px; margin-top:20px;">擅长技能</div>
    <div class="clear-both col-xs-8">
      <skills :selected_skills="item"></skills>
    </div>
    <div class="clearfix"></div>
  </form>
</template>
<script>
import skills from './skills.vue'
export default {
  methods: {
    save () {
      this.$dispatch('update_skills', this.item)
      this.$dispatch('close_modal')
    }
  },
  props: ['item'],
  components: {
    skills
  }
}
</script>
