export default {
  install (Vue, options) {
    Vue.filter('format', (value) => {
      return Math.floor(value * 100) / 100
    })
  }
}

