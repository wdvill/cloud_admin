export default {
  install (Vue, options) {
    Vue.filter('substr', (value) => {
      return value.length > 100 ? value.substr(0, 100) + '..' : value
    })
    Vue.filter('substr_money', (value) => {
      if (/\./.test(value)) {
        let sum = value.toString().split('.')
        sum[1] = sum[1].length < 2 ? sum[1] += '0' : sum[1].substr(0, 2)
        value = sum[0] + '.' + sum[1]
      } else {
        value += '.00'
      }
      return value
    })
  }
}
