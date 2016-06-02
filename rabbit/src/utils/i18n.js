import Cookies from 'js-cookie'
import $ from 'jquery'
export default {
  i18n () {
    let lang = Cookies.get('_lang')
    if (!lang) {
      lang = (navigator.language || navigator.browserLanguage).toLowerCase()
      if (lang === 'zh-cn') {
        let p = '/static/locale/locale-zh-cn.json'
        return $.getJSON(p)
      } else {
        let p = '/static/locale/locale-en.json'
        return $.getJSON(p)
      }
    }
  }
}
