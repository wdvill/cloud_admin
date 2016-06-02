import pagination from '../utils/pagination'

let paginations = {}

export default {
  methods: {
    setPagination (name, data) {
      paginations['pagination_' + name] = new pagination.Pagination(data)
      let temp = paginations['pagination_' + name].more()
      this.$set(name + '_list_show', {})
      this.$set(name + '_list_show.array', temp.array)
      this.$set(name + '_list_show.more', temp.more)
    },
    more (name) {
      let pagination = paginations['pagination_' + name].more()
      this.$set(name + '_list_show.array', this[name + '_list_show'].array.concat(pagination.array))
      this.$set(name + '_list_show.more', pagination.more)
    },
    handleData (name, data) {
      if (data.error_code === 0) {
        this.$set(name + '_list', data.proposals)
        this.setPagination(name, data.proposals)
      }
    }
  }
}
