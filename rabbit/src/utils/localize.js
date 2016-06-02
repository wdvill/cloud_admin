export default {
  getLanLevel () {
    let configs = window.COMMONS
    if (!configs) {
      return {}
    }

    return configs['_lang_level'] ? configs['_lang_level'] : {}
  }
}
