export default {
  minlength: {
    handler (value, num) {
      return value && value.length >= num
    }
  },
  maxlength: {
    handler (value, num) {
      return value && value.length <= num
    }
  },
  required: {
    handler (value) {
      return value && value.replace(/^\s+|\s+$/g) !== ''
    }
  }
}
