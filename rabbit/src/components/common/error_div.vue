<template>
	<div class="form-group error-div" name="error" data-name="{[name]}">
    <div class="col-xs-offset-3 col-xs-6 clear-left text-warning yzj-size-14">
      <span class="glyphicon glyphicon-exclamation-sign yzj-right-distance10" aria-hidden="true"></span>
      <span class="errorMsg"></span>
    </div>
  </div>
</template>

<script>
  export default {
    props: ['name']
  }
</script>
