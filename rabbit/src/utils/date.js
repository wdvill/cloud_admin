function formatDate (date) {
  let datetime = new Date(date)

  let getStr = function (num) {
    return num * 1 < 10 ? '0' + num : num
  }

  return [datetime.getFullYear(), getStr(datetime.getMonth() * 1 + 1), getStr(datetime.getDate())].join('-')
}

export default {
  formatDate: formatDate
}
