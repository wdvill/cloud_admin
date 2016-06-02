import $ from 'jquery'
import rules from './rules'
function Validate (options, context) {
  this.options = options ? options : {}
  this.context = context ? context : {}
  this.init(this.options, this.context)
}

Validate.prototype.init = function (fields, context) {
  $('input', context).blur((e) => {
    let elem = $(e.target)
    let name = elem.attr('name')

    console.log(context, elem, 'hllll', e.target)

    console.log(name, 'validate from')
    this.validateItem(name, context)

  })
  $('select', context).change((e) => {
    console.log(e, 'event')
    let elem = $(e.target)
    let name = elem.attr('name')

    console.log(elem, 'seleect', $(this))
    this.validateItem(name, context)

  })
}

Validate.prototype.validateItem = function (name, context) {
  let result = true
  let elem = $('input[name="' + name + '"]', context)
  if (elem.size() === 0) {
    elem = $('select[name="' + name + '"]', context)
  }
  let field = this.options[name]
  if (!field) {
    return
  }
  for (let key in field) {
    // 1. value of emlement 2. rule
    let flag = rules[key].handler.call(null, elem.val(), field[key])
    if (!flag) {
      result = false
    }
  }
  if (result) {
    $('.form-error[for="' + name + '"]', context).hide()
  } else {
    $('.form-error[for="' + name + '"]', context).show()
  }

  return result
}

Validate.prototype.validate = function () {
  let result = true
  for (let key in this.options) {
    let flag = this.validateItem(key, this.context)
    console.log(key, '----', flag)
    if (!flag) {
      result = flag
    }
  }
  console.log('final', result)
  return result
}

export default Validate
