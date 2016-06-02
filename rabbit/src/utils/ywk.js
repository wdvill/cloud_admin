import Cookies from 'js-cookie'
import $ from 'jquery'
export default {
  getValue (obj) {
    let type = obj[0].type
    if (type === 'radio') {
      return $.trim(obj.find('[checked]').val())
    } else if (type === 'select') {
      return $.trim(obj.find('option:selected').val())
    } else if (type === 'checkbox') {
      let val = []
      obj.each((index, item) =>{
        if ($(item).is(':checked')) {
          val.push($(item).val())
        }
      })
      return val.join(',')
    } else {
      return $.trim(obj.val())
    }
  },
  assemblingData (data) {
    if (typeof (data) === 'object') {
      data._xsrf = Cookies.get('_xsrf')
    } else {
      data = {}
      data._xsrf = Cookies.get('_xsrf')
    }
    return data
  },
  postJson (url, data) {
    data = this.assemblingData(data)
    return $.ajax({
      url: url,
      type: 'post',
      dataType: 'json',
      data: data
    })
  },
  getJson (url, data) {
    return $.ajax({
      url: url + '?timestamp = ' + new Date().getTime(),
      type: 'get',
      dataType: 'json',
      data: data
    })
  },
  deleteJson (url, data) {
    data = this.assemblingData(data)
    return $.ajax({
      url: url,
      type: 'DELETE',
      dataType: 'json',
      data: data
    })
  },
  putJson (url, data) {
    data = this.assemblingData(data)
    return $.ajax({
      url: url,
      type: 'PUT',
      dataType: 'json',
      data: data
    })
  },
  postFile (url, data) {
    data.append('_xsrf', Cookies.get('_xsrf'))
    return $.ajax({
      type: 'POST',
      url: url,
      cache: false,
      dataType: 'json',
      data: data,
      processData: false,
      contentType: false
    })
  }
}
