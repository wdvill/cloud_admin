export default {
  data: {
    modals: {}
  },
  methods: {
    close (target) {
      this.$set(['modals', target].join('.'), false)
    },
    open (target) {
      this.$set(['modals', target].join('.'), true)
    }
  },
  events: {
    save (target) {
      this.close(target)
    },
    cancel (target) {
      this.close(target)
    },
    close (target) {
      this.close(target)
    }
  }
}
