<template>
    <h3 class="modal-title text-info text-center" id="myModalLabel">
      编辑职位和地区
    </h3>
    <form class="form-horizontal yzj-top-distance50" id="form-base">
     <div class="form-group">
      <label class="control-label col-xs-offset-2 col-xs-2 yzj-size-16 clear-left text-left text-info">
       职位</label>
       <div class="col-xs-6 clear-left">
        <input type="text" class="form-control" name="{[item.title]}" v-model="item.title" required required-msg="请填写职位"/>
      </div>
    </div>

    <div class="form-group error-div" name="error" data-name="{[item.title]}">
      <div class="col-xs-offset-4 col-xs-8 text-warning yzj-size-14">
        <span class="glyphicon glyphicon-exclamation-sign yzj-right-distance10" aria-hidden="true"></span>
        <span class="errorMsg"></span>
      </div>
    </div>

    <location v-bind:city_id.sync="item.location.location_id"></location>
  </form>

</template>
<script>
import $ from 'jquery'
import location from './location.vue'
import validate from '../utils/validate'
export default {
  data () {
    return {
    }
  },
  ready () {
    validate.RegEventBlur($('#form-base'))
  },
  methods: {
    save () {
      if (!validate.validateForm($('#form-base'))) {
        return
      }
      this.$dispatch('update_base', this.item)
      this.$dispatch('close_modal')
    }
  },
  props: ['item'],
  components: {
    location
  }

}
</script>
