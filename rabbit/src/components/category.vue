<template>
  <div class="form-group">
    <label for="inputEmail3" class="col-xs-offset-1 col-xs-2 control-label yzj-size-16">
      <span class="text-warning size-18">
        *
      </span>
      项目类别
    </label>
    <div class="col-xs-3 clear-right">
      <select class="form-control select-control" id="lb01" v-model="top.selected" v-on:change="updateSub(top.selected.category_id, $event)">
        <option v-for="option in top.options" v-bind:value="option">
          {[ option.name ]}
        </option>
      </select>
    </div>
    <div class="col-xs-3 clear-right">
      <select class="form-control select-control" id="lb02" v-model="sub.selected">
        <option v-for="option in sub.options" v-bind:value="option">
          {[ option.name ]}
        </option>
      </select>
    </div>
  </div>
</template>
<script>
import $ from 'jquery'
export default {
  created () {
    let _self = this
    $.post('/api/category', {category_id: 0}, (data) => {
      _self.top.options = data.categorys
      _self.top.selected = data.categorys[0]
      _self.updateSub(_self.top.selected.category_id)
    }, 'json')
  },
  data () {
    return {
      dft: null,
      top: {
        selected: '',
        parent_name: '',
        options: []
      },
      sub: {
        selected: '',
        name: '',
        options: []
      }
    }
  },
  watch: {
    cateobj (value) {
      if (value) {
        this.setTop(value.parent_id)
        this.dft = value
      } else {
        this.top.selected = {}
        this.sub.selected = {}
      }
    }
  },
  methods: {
    updateSub (option) {
      let _self = this
      $.post('/api/category', {category_id: option}, (data) => {
        _self.sub.options = data.categorys
        if (_self.dft) {
          _self.setSub(_self.dft.id)
        } else {
          _self.sub.selected = data.categorys[0]
        }
      }, 'json')
    },
    setTop (id) {
      this.top.selected = this.getCategory(id, this.top.options)
    },
    setSub (id) {
      this.sub.selected = this.getCategory(id, this.sub.options)
    },
    getCategory (id, options) {
      for (let i = 0; i < options.length; i++) {
        if (id === options[i].category_id) {
          return options[i]
        }
      }
    }
  },
  props: ['cateobj']

}
</script>
