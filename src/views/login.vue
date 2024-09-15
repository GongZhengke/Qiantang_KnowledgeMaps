<template>
  <div class="home">

    <div class="index-info">

      <Login @on-submit="handleSubmit" :style="{ width: '400px', margin: 'auto' }">
        <UserName name="username" />
        <Password name="password" />
        <Submit />
        <Button size="large" :style="{ width: '400px', marginTop: '10px' }" @click="changePage('/reg')" long>没有账户？立即注册</Button>
      </Login>


    </div>


  </div>
</template>

<script>
// import { IconSearch } from '@arco-design/web-vue/es/icon';
import { reactive } from 'vue'
import API from "../axios"
import qs from 'qs'
import { Message } from '@arco-design/web-vue'
import { useRouter } from 'vue-router'

export default {
  // setup() {
  //   const form = reactive({
  //     username: '',
  //     password: '',
  //   })

  //   var token = ''

  //   API({
  //     url: '/api/getToken',
  //     method: 'get'
  //   })
  //     .then((res) => {
  //       token = res.data.csrftoken
  //     })

  //   const successmsg = (infos) => Message.success({ content: infos })
  //   const warningmsg = (infos) => Message.warning({ content: infos })
  //   const userRouter = useRouter()

  //   const handleSubmit = ({ values, errors }) => {
  //     if (errors == '' || errors == undefined) {
  //       API({
  //         url: '/api/user/login',
  //         method: 'post',
  //         data: qs.stringify({ username: form.username, password: form.password }),
  //         headers: { 'X-CSRFToken': token }
  //       })
  //         .then((res) => {
  //           if (res.data.errcode == 200) {
  //             successmsg(res.data.errmsg)
  //             userRouter.push({
  //               path: '/'
  //             })
  //           } else {
  //             warningmsg(res.data.errmsg)
  //           }
  //         })
  //     }


  //   }


  //   return {
  //     form,
  //     handleSubmit
  //   }
  // },
  
  data(){
    return{
      token:''
    }
  },
  created(){
    this.getToken()
  },
  methods: {
    getToken(){
      API({
          url: '/api/getToken',
          method: 'get'
        })
          .then((res) => {
            this.token = res.data.csrftoken
          })
    },
    changePage(url) {
      this.$router.push(url)
    },
    handleSubmit(valid, { username, password }) {
      if (valid) {

        API({
          url: '/api/user/login',
          method: 'post',
          data: qs.stringify({ username: username, password: password }),
          headers: { 'X-CSRFToken': this.token }
        })
          .then((res) => {
            if (res.data.errcode == 200) {
              this.$message.success(res.data.errmsg)
              this.$router.push('/')
            } else {
              this.$message.warning(res.data.errmsg)
            }
          })
      }
    }
  }
}
</script>
<style scoped>
.home {
  background-color: #fff;
  min-height: 200px;
  padding: 30px;
  padding-bottom: 5px;
  border-radius: 3px;
}


.index-info {
  display: flex;
  min-height: 700px;
}
</style>