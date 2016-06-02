<template>
<div class="modal fade" id="alert" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
  <div class="modal-dialog modal-warning" role="document">
    <div class="modal-content">
      <div class="modal-header"></div>
      <div class="modal-body">
        <h4 class="modal-title text-center text-danger" id="myModalLabel"><strong>{[msg]}</strong></h4>
      </div>
      <div class="modal-footer text-center">
        <button type="button" class="btn btn-danger btn-sm" data-dismiss="modal">确定</button>
      </div>
    </div>
  </div>
</div>
</template>

<script>
  export default {
    props: ['msg']
  }
</script>
