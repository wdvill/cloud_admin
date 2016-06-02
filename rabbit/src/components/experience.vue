<template>
  <div class="work-experience">
    <div v-if="itemout.picture.path!=''">
      <div class="col-md-2 clear-left" style="float:left" v-if="itemout.picture.path">
        <img v-bind:src="itemout.picture.path" width="100" height="100" />
      </div>
      <div class="col-md-10">
        <p class="text-primary yzj-size-16">
        项目名称：<a v-if="!ismyself" style="cursor:pointer;color:#333" v-on:click="project_detail">{[itemout.name]}</a>
                  <span v-if="ismyself" class="text-muted">{[itemout.name]}</span>
          <span class="pull-right" v-if="ismyself">
            <img class="yzj-right-distance10 pointer" src="/static/images/edit-btn-icon.png" @click="edit(itemout)">
            <img class="pointer" src="/static/images/del-btn-icon.png" data-toggle="modal" data-target="#expModal">
          </span>
        </p>
        <p class="yzj-top-distance20 yzj-size-14">
          完成时间：{[itemout.end_at | year_month]}
        </p>
        <p class="yzj-top-distance20 yzj-size-14 yzj-height30">
          项目描述：{[itemout.detail]}
        </p>
        <p class="yzj-top-distance15 yzj-size-14">
          <span class="yzj-right-distance10">
            {[itemout.category.parent_name]}，
          </span>
          <span class="yzj-right-distance10">
            {[itemout.category.name]}
          </span>
        </p>
      </div>
    </div>
    <div v-if="itemout.picture.path==''">
      <p class="text-primary yzj-size-16">
        项目名称：<a v-if="!ismyself" style="cursor:pointer;color:#333" v-on:click="project_detail">{[itemout.name]}</a>
                  <span v-if="ismyself" class="text-muted">{[itemout.name]}</span>
        <span class="pull-right" v-if="ismyself">
          <img class="yzj-right-distance10" src="/static/images/edit-btn-icon.png" @click="edit(itemout)">
          <img src="/static/images/del-btn-icon.png" data-toggle="modal" data-target="#expModal">
        </span>
      </p>
      <p class="yzj-top-distance20 yzj-size-14">
        完成时间：{[itemout.end_at | year_month]}
      </p>
      <p class="yzj-top-distance20 yzj-size-14 yzj-height30">
        项目描述：{[itemout.detail]}
      </p>
      <p class="yzj-top-distance15 yzj-size-14">
        <span class="yzj-right-distance10">
          {[itemout.category.parent_name]}，
        </span>
        <span class="yzj-right-distance10">
          {[itemout.category.name]}
        </span>
      </p>
    </div>
    <div class="clearfix">
  </div>
  <div v-if="islast=='no'">
    <div class="line02">
    </div>
  </div>
  <confirm title="删除项目经验" msg="确定删除该项目经验么？" modal-id="expModal" :ok-fn.sync="delete"></confirm>

</template>

<script>
  import $ from 'jquery'
  import confirm from './confirm.vue'

  export default {
    data () {
      return {
        item: { text: 'text from experience' }
      }
    },
    props: ['itemout', 'index', 'islast', 'ismyself'],
    methods: {
      edit (item_data) {
        this.$dispatch('edit', item_data, 'item')
      },
      delete () {
        $.ajax({
          method: 'delete',
          url: '/api/portfolio',
          data: {pid: this.itemout.id},
          dataType: 'json'
        }).success((data) => {
          if (data.error_code === 0) {
            this.$dispatch('delete_project', this.itemout, 'item')
          }
        })
      },
      project_detail: function () {
        this.$dispatch('project_detail', this.itemout)
      }
    },
    components: {
      confirm
    }
  }
</script>
