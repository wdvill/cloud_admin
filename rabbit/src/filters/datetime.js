import formatDate from '../utils/date'
export default {
  install (Vue, options) {
    Vue.filter('year_month', (value) => {
      let pattern = /\d{4}-\d{2}/.exec(value)
      return pattern ? pattern[0] : value
    })
    Vue.filter('year_month_day', (value) => {
      let pattern = /\d{4}-\d{2}-\d{2}/.exec(value)
      return pattern ? pattern[0] : value
    })
    Vue.filter('year', (value) => {
      let pattern = /\d{4}/.exec(value)
      return pattern ? pattern[0] : value
    })
    Vue.filter('dateformat', (value) => {
      return formatDate(value)
    })
    Vue.filter('hourformat', (value) => {
      let hour = Math.floor(value / 60)
      let minute = (value % 60)
      if (minute < 10) {
        minute = '0' + minute
      }
      return hour + ':' + minute
    })
    Vue.filter('days', (value) => {
      try {
        let regex = /^(\d{4})-(\d{2})-(\d{2})\s(\d{2}):(\d{2}):(\d{2})/g
        let pattern = regex.exec(value)
        let date = new Date()
        if (pattern) {
          date.setFullYear(pattern[1])
          date.setMonth(pattern[2] - 1)
          date.setDate(pattern[3])
          date.setHours(pattern[4])
          date.setMinutes(pattern[5])
          date.setSeconds(pattern[6])
        }
        let now = new Date()
        let millseconds = now.getTime() - date.getTime()
        let days = Math.floor(millseconds / (24 * 60 * 60 * 1000))

        return days < 1 ? Math.floor(millseconds / (60 * 60 * 1000)) + '小时前' : days + '天前'

      } catch (e) {
        console.log(e)
      }
    })
    Vue.filter('times', (value) => {
      return formateStyle(value)
      function formateTime (time, style) {
        let now = new Date()
        if (time === undefined) {
          return
        }
        let d = time.split(' ')
        let old = new Date(d[0].split('-')[0], d[0].split('-')[1] - 1, d[0].split('-')[2], d[1].split(':')[0], d[1].split(':')[1], d[1].split(':')[2])
        let dt = now.getTime() - old.getTime()
        switch (style) {
          case 's':
            return parseInt(dt / 1000, 10)
          case 'n':
            return parseInt(dt / 60000, 10)
          case 'h':
            return parseInt(dt / 3600000, 10)
          case 'd':
            return parseInt(dt / 86400000, 10)
          case 'm':
            return (now.getMonth() + 1) + ((now.getFullYear() - old.getFullYear()) * 12) - (old.getMonth() + 1)
          case 'y':
            return now.getFullYear() - old.getFullYear()
        }
      }
      function formateStyle (time) {
        if (time === '') {
          return null
        }
        if (formateTime(time, 's') < 60) {
          return formateTime(time, 's') + '秒'
        } else if (formateTime(time, 'n') < 60) {
          return formateTime(time, 'n') + '分钟'
        } else if (formateTime(time, 'h') < 24) {
          return formateTime(time, 'h') + '小时'
        } else if (formateTime(time, 'd') < 31) {
          return formateTime(time, 'd') + '天'
        } else if (formateTime(time, 'm') < 12) {
          return formateTime(time, 'm') + '个月'
        } else if (formateTime(time, 'y') < 60) {
          return formateTime(time, 'y') + '年'
        }
      }
    })
  }
}
