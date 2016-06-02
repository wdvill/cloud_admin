export default {
  install (Vue, options) {
    Vue.directive('yzj_star', function (value) {
      let star = ''
      let n_star = Math.floor(value)
      for (let i = 0; i < n_star; i++) {
        star = star + '<img src = "/static/images/raty/star-on.png" >&nbsp'
      }
      if (value - n_star > 0) {
        star = star + '<img src = "/static/images/raty/star-half.png" >&nbsp'
        for (let i = 0; i < 4 - value; i++) {
          star = star + '<img src = "/static/images/raty/star-off.png" >&nbsp'
        }
      } else {
        for (let i = 0; i < 5 - value; i++) {
          star = star + '<img src = "/static/images/raty/star-off.png" >&nbsp'
        }
      }
      this.el.innerHTML = star
    })
  }
}
