import YWORK from '../utils/ywk.js'

export default {
  upload (url, data) {
    return YWORK.postFile('/api/attachment' + url, data, 'application/json')
  }
}
