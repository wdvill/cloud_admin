export default {

  getValueByName (name) {
    let paramArr = location.search.substr(1).split('&')
    let parameter = {}

    for (let i = 0; i < paramArr.length; i++) {
      let param = paramArr[i].split('=')
      parameter[param[0]] = param[1]
    }
    return parameter[name] ? parameter[name] : ''
  },
  getLastId () {
    let paramArr = location.pathname.split('/')
    if (paramArr) {
      return paramArr[paramArr.length - 1]
    }
  },
  getLastTwoId () {
    let paramArr = location.pathname.split('/')
    if (paramArr) {
      return paramArr[paramArr.length - 2]
    }
  }
}
