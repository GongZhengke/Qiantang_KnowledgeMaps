<template>
  <menuVue></menuVue>

  <div class="loading-div" v-if="loading == true" >
    <a-spin tip="正在加载中" style="margin: auto;">
    </a-spin>
  </div>

  <div class="content">

    <router-view />
  </div>
  <a-layout-footer>ZJWEUer KnowledgeGraph &copy; 2022-2024 浙水院软工21-1智慧水利创新团队</a-layout-footer>
</template>
<script>
import menuVue from './components/menu.vue';
import API from "./axios";
export default {
  setup() {
    return {
    }
  },
  data(){
    return{
      loading:false,
    }
  },
  components: {
    menuVue
  },
  mounted() {

  },
  
}
</script>
<style>
body{
  background-color: var(--color-neutral-2)!important;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
.content{
  padding: 65px;
  padding-top: 85px;
  padding-bottom: 10px;
}
.arco-layout-footer{
  display: flex;
  flex-direction: column;
  justify-content: center;
  font-size: 14px;
  font-stretch: condensed;
  text-align: center;
  padding: 30px;
  padding-top: 15px;
  color: #aaa;
}
.index-search input{
    font-size: 16px!important;
}
.index-search button{
    font-size: 16px!important;
    height: 55px!important;
}

.loading-div{
  position: fixed;
  width: 100%;
  height: 100%;
  display: flex;
  background-color: #ffffff30;
  z-index: 999;
  backdrop-filter: blur(2px);
}
.loading-div .arco-spin-icon {
    color: rgb(var(--arcoblue-5));
    font-size: 39px;
}
.loading-div .arco-spin-tip{
    color: rgb(var(--arcoblue-5));
    font-size: 20px;
}
.ivu-poptip-rel {
    width: 100%!important;
}

</style>
