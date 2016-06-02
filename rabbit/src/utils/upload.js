import Cookies from 'js-cookie'
import file_service from '../service/file_service'

export default {
  upload (file) {
    let data = new FormData()
    data.append('file', fileo)
    data.append('t', 'portfolio')
    data.append('_xsrf', Cookies.get('_xsrf'))

    return file_service.upload(data)
  }
}
