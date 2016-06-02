<template>
<div class="float-window">
  <div v-for="data in datas"><a v-on:click="data.click?data.click():''" href="{[data.href]}" class="icon-{[$index + 1]}"></a><p>{[data.name]}</p></div>
</div>
</template>

<script>
  export default {
    data () {
      return {
        datas: [
          {name: '桌面软件', href: '#', click: ''},
          {name: 'APP下载', href: '#', click: ''},
          {name: '联系客服', href: '#', click: ''},
          {name: '意见反馈', href: 'javascript:;', click: this.open_window},
          {name: '回顶部', href: '#', click: ''}
        ]
      }
    },
    methods: {
      open_window () {
        let _self = this
        _self.$dispatch('open', 'float_msg')
      }
    }
  }
</script>
