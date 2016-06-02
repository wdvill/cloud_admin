<template>
  <active :proposal="proposal" v-if="(proposal.status == 'active' && proposal.ptype == 'D' ) || proposal.status == 'interview'"></active>
  <invite :proposal="proposal" v-if="proposal.status == 'active' && proposal.ptype == 'I'"></invite>
  <hire :proposal="proposal" v-if="proposal.status == 'hire'"></hire>
  <revoke :proposal="proposal" v-if="proposal.status == 'revoke'"></revoke>
  <refuse :proposal="proposal" v-if="proposal.status == 'refuse'"></refuse>
  <archive :proposal="proposal" v-if="proposal.status == 'archive'"></archive>
</template>

<script>
  import active from './operate_active.vue'
  import invite from './operate_invite.vue'
  import revoke from './operate_revoke.vue'
  import refuse from './operate_refuse.vue'
  import archive from './operate_archive.vue'
  import hire from './operate_hire.vue'

  export default {
    created () { },
    data () {
      return {
        status: false
      }
    },
    props: ['proposal'],
    components: {
      active,
      invite,
      revoke,
      hire,
      archive,
      refuse
    }
  }
</script>

