<template>
    <p class="pull-left new-job-star {[userClass]}" title="这是个新人，还没有评分数据" v-if="eveluateNum === 0">
        <span class="font">NEW</span>
        <img class="new-star" src="../../assets/images/components/star-icon-white.png" />
    </p>
    <p class="pull-left {[userClass]}" v-if="eveluateNum > 0" title="{[averScore]}分，{[eveluateNum]}人评论">
        <template v-for="item in 5" >
            <img class="star" v-if="item+1 <= averScore" src="../../assets/images/components/star-icon-color.png" />
            <img class="star" v-if="item+1 < averScore && averScore < item+2" src="../../assets/images/components/star-icon-half.png" />
            <img class="star" v-if="item-averScore >= 0" src="../../assets/images/components/star-icon.png" />
        </template>
    </p>
</template>
<style lang="scss">
    .new-job-star{
        width: 72px;
        height: 20px;
        padding: 2px 12px;
        margin-top: -3px;
        background: url(../../assets/images/components/star-icon-newbg.png) left center no-repeat;
        background-size: 66px 20px;
        
        .font{
            font-size: 10px;
            color: #fff;
            font-weight: bold;
       }
    }
    .star{
        width: 14px;
        height: 13px;
    }
    .new-star{
        width: 12px !important;
    }
</style>
<script>

  export default {
    props: {
      // 平均分
      averScore: {
        type: Number,
        default: 0
      },
      // 评论人数
      eveluateNum: {
        type: Number,
        default: 0
      },
      // 用户自定义样式
      userClass: {
        type: String,
        default: 'yzj-right-distance45'
      }
    }
  }
</script>
