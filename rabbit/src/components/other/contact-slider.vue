<template>
  <div class="contact">
    <a href="" class="btn-services">联系在线客服</a>
    <a class="btn-feedback" v-on:click = "feedback">意见反馈</a>
    <p class="info">您还可以通过以下方式获得帮助</p>
    <ul class="list">
      <li class="phone">客服电话 : 3838479</li>
      <li class="service">客服QQ1 : 358987</li>
      <li class="service">客服QQ2 : 1245</li>
    </ul>
    <div class="qr">
      <img src="../../assets/images/components/qr.png" height="152" width="151" alt="">
      <p>扫码关注公众号，在线客服随时沟通</p>
    </div>
  </div>
</template>
<style lang="sass">
</style>
<script>
  export default {
    methods: {
      feedback () {
        this.$dispatch('open', 'float_msg')
      }
    }
  }
</script>
