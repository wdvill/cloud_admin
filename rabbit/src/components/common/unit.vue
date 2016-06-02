<template>
  <span v-if="paymethod === 'hour'">元/小时</span>
  <span v-else>元</span>
</template>

<script>
  export default {
    props: ['paymethod']
  }
</script>
