<template>
  <modal :show.sync="showModal" :large="true" width="800" >
    <div slot="modal-header" class="modal-header">
      <button type="button" class="close" data-dismiss="modal" aria-label="Close" id="project_close" @click="showModal = false">
      <span aria-hidden="true" class="yzj-size-30">
        &times;
      </span>
    </div>
    <div slot="modal-body" class="modal-body">
      <component :item="item" :is="currentView" v-ref:form></component>
    </div>
    <div slot="modal-footer" class="modal-footer">
      <div class="col-xs-10 col-xs-offset-2 yzj-bot-distance50">
        <div class="col-xs-4">
          <button type="button" class="btn btn-primary btn-block yzj-right-distance15"
          v-on:click="save">
          保存
          </button>
        </div>
        <div class="col-xs-4">
          <button type="button" class="btn btn-default btn-block yzj-right-distance15"
            data-dismiss="modal" v-on:click="showModal = false">
            取消
          </button>
        </div>
      </div>
    </div>
  </modal>
</template>

<script>
import { modal } from 'vue-strap'
import form_exp from './form_exp.vue'
import form_job from './form_job.vue'
import form_edu from './form_edu.vue'
import form_language from './form_language.vue'
import form_workload from './form_workload.vue'
import form_detail from './form_detail.vue'
import form_hourly from './form_hourly.vue'
import form_base from './form_base.vue'
import form_skills from './form_skills.vue'

export default {
  data () {
    return {
      msg: 'Hello from vue-loader!',
      showModal: false,
      currentView: 'form_exp',
      item: {},
      continue_save: true
    }
  },
  methods: {
    test (dataModel, type) {
      switch (type) {
        case 'job':
          this.currentView = 'form_job'
          this.continue_save = true
          break
        case 'item':
          this.currentView = 'form_exp'
          this.continue_save = true
          break
        case 'edu':
          this.currentView = 'form_edu'
          this.continue_save = true
          break
        case 'language':
          this.currentView = 'form_language'
          this.continue_save = true
          break
        case 'workload':
          this.currentView = 'form_workload'
          this.continue_save = false
          break
        case 'detail':
          this.currentView = 'form_detail'
          this.continue_save = false
          break
        case 'hourly':
          this.currentView = 'form_hourly'
          this.continue_save = false
          break
        case 'base':
          this.currentView = 'form_base'
          this.continue_save = false
          break
        case 'skills':
          this.currentView = 'form_skills'
          this.continue_save = false
          break

      }
      this.showModal = true
      this.msg = 'payfor'
      this.item = dataModel
    },
    save () {
      this.$refs.form.save()
    }
  },
  events: {
    close_modal () {
      this.showModal = false
    }
  },
  components: {
    modal,
    form_exp,
    form_job,
    form_edu,
    form_language,
    form_workload,
    form_detail,
    form_hourly,
    form_base,
    form_skills
  }
}
</script>
