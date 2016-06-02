import level from '../config/level'
import paymethod from '../config/paymethod'
import role from '../config/role'
import degree from '../config/degree'
import workload from '../config/workload'
import workloadC from '../config/workload-c'
import language from '../config/language'
import duration from '../config/duration'

export default {
  install (Vue, options) {
    Vue.filter('level', (value, name = 'title') => {
      let config = level[name]
      return config[value] ? config[value] : value
    })
    Vue.filter('paymethod', (value) => {
      return paymethod[value] ? paymethod[value] : value
    })
    Vue.filter('role', (value) => {
      return role[value] ? role[value] : value
    })
    Vue.filter('degree', (value) => {
      return degree[value] ? degree[value] : value
    })
    Vue.filter('workload', (value) => {
      return workload[value] ? workload[value] : value
    })
    Vue.filter('workloadC', (value) => {
      return workloadC[value] ? workloadC[value] : value
    })
    Vue.filter('language', (value) => {
      return language[value] ? language[value] : value
    })
    Vue.filter('duration', (value) => {
      return duration[value] ? duration[value] : value
    })
  }
}
