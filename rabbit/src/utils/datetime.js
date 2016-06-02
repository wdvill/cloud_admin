export default {
  getYearList (from = 1970) {
    let now = new Date().getFullYear()
    let list = []
    let i = now * 1
    for (; i >= from; i--) {
      list.push(i)
    }
    return list
  },
  getMonthList () {
    return [1, 2, 3, 4, 5, 6, 7, 8, 9, 12]
  },
  /* 计算两个Date类型时间差，以hh:mm:ss格式返回 */
  getDiff (start, end) {
    let diffStr = ''
    let difference = end.getTime() - start.getTime()
    if (difference > 0) {
      let hour = Math.floor(difference / (1000 * 60 * 60))
      let minute = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60))
      let second = Math.floor((difference % (1000 * 60 * 60)) % (1000 * 60) / 1000)
      if (parseInt(hour, 10) < 10) {
        hour = '0' + parseInt(hour, 10)
      }
      if (parseInt(minute, 10) < 10) {
        minute = '0' + parseInt(minute, 10)
      }
      if (parseInt(second, 10) < 10) {
        second = '0' + parseInt(second, 10)
      }
      diffStr = hour + ':' + minute + ':' + second
    }
    return diffStr
  }
}
