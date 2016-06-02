import localize from '../utils/localize'
export default {
  install (Vue, options) {
    Vue.filter('level_str', (value) => {
      let level = localize.getLanLevel()
      return level[value] ? level[value] : value
    })
  }
}
