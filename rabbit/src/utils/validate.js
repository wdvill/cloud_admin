import $ from 'jquery'
import YWORK from '../utils/ywk.js'
export default {
  RegEventBlur (form) {
    form.find('[required]').each((index, item) =>{
      $(item).blur(() =>{
        let name = $(item).attr('name')
        let value = YWORK.getValue($(item))
        let errorName = $(item).attr('data-error') ? $(item).attr('data-error') : name
        let errorNode = form.find('div[data-name="' + errorName + '"]')
        if (value === '' || typeof (value) === 'undefined') {
          let msg = $(item).attr('required-msg')
          errorNode.find('span[class="errorMsg"]').text(msg)
          errorNode.show()
        } else {
          errorNode.hide()
        }
      })
    })
  },
  validateForm (form) {
    let isLegal = true
    form.find('[required]').each((index, item) =>{
      let name = $(item).attr('name')
      let value = YWORK.getValue($(item))
      if (value === '' || typeof (value) === 'undefined') {
        isLegal = false
        let msg = $(item).attr('required-msg')
        let errorName = $(item).attr('data-error') ? $(item).attr('data-error') : name
        let errorNode = form.find('div[data-name="' + errorName + '"]')
        errorNode.find('span[class="errorMsg"]').html(msg)
        errorNode.show()
      }
    })
    return isLegal
  }
}
