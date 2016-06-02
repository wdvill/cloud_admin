<template>
<modal :show.sync="showmodal" :large="large" width="800" style="overflow-y:scroll;">
  <div slot="modal-header" class="modal-header">
    <button type="button" class="close" data-dismiss="modal" aria-label="Close" id="project_close" @click="showmodal = false">
    <span aria-hidden="true" class="yzj-size-30">
      &times;
    </span>
  </div>
  <div slot="modal-body" class="modal-body">
    <slot name="content"></slot>
  </div>
  <div slot="modal-footer" class="modal-footer">
  </div>
</modal>
</template>

<script>
  import { modal } from 'vue-strap'
  export default {
    data () {
      return {
        'large': this.large ? this.large : 'true'
      }
    },
    components: {
      modal
    },
    props: ['showmodal', 'large']
  }
</script>
