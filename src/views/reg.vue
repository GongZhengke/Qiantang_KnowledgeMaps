<template>
  <div class="home">

    <div class="index-info demo-register">

      <Login ref="form" @on-submit="handleSubmit" :style="{ width: '400px', margin: 'auto' }">
        <UserName name="username" />
        <Email name="email" />
        <Mobile name="phone" />
        <Poptip trigger="focus" placement="top-end" width="240">
          <Password name="password" :rules="passwordRule" placeholder="至少6位密码，区分大小写"
            @on-change="handleChangePassword" />
          <template #content>
            <div class="demo-register-tip">
              <div class="demo-register-tip-title" :class="passwordTip.class">
                强度：{{ passwordTip.strong }}
              </div>
              <Progress :percent="passwordTip.percent" hide-info :stroke-width="6" :stroke-color="passwordTip.color" />
              <div class="demo-register-tip-desc">
                请至少输入 6 个字符。请不要使用容易被猜到的密码。
              </div>
            </div>
          </template>
        </Poptip>
        <Password name="passwordConfirm" :rules="passwordConfirmRule" placeholder="确认密码" />
        <Submit>注册</Submit>
        <Button size="large" :style="{ width: '400px', marginTop: '10px' }" @click="changePage('/login')"
          long>已有账户？立即登录</Button>
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
  //     phone: '',
  //     email: '',
  //   })

  //   var token = ''

  //   API({
  //     url: '/api/getToken',
  //     method: 'get'
  //   })
  //     .then((res) => {
  //       token = res.data.csrftoken
  //     })

  //   const successmsg =  (infos) => Message.success({content:infos})
  //   const warningmsg =  (infos) => Message.warning({content:infos})
  //   const userRouter = useRouter()

  //   const handleSubmit = ({values, errors}) => {
  //     if (errors == ''||errors == undefined) {
  //       API({
  //         url: '/api/user/reg',
  //         method: 'post',
  //         data: qs.stringify({username:form.username,password:form.password,email:form.email,phone:form.phone}),
  //         headers: { 'X-CSRFToken': token}
  //       })
  //         .then((res) => {
  //           if(res.data.errcode==200){
  //             successmsg(res.data.errmsg)
  //             userRouter.push({
  //               path:'/'
  //             })
  //           }else{
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

  data() {
    const validatePassCheck = (rule, value, callback) => {
      if (value !== this.$refs.form.formValidate.password) {
        callback(new Error('两次输入的密码不匹配！'));
      } else {
        callback();
      }
    };
    return {
      passwordRule: [
        {
          required: true, message: '密码不能为空！', trigger: 'change'
        },
        {
          min: 6, message: '密码不能少于6位！', trigger: 'change'
        }
      ],
      passwordConfirmRule: [
        {
          required: true, message: '确认密码不能为空！', trigger: 'change'
        },
        { validator: validatePassCheck, trigger: 'change' }
      ],
      // 密码长度，在密码强度提示时作为判断依据
      passwordLen: 0
    }
  },
  computed: {
    // 密码强度提示文案等
    passwordTip() {
      let strong = '强';
      let className = 'strong';
      let percent = this.passwordLen > 10 ? 10 : this.passwordLen;
      let color = '#19be6b';

      if (this.passwordLen < 6) {
        strong = '太短';
        className = 'low';
        color = '#ed4014';
      } else if (this.passwordLen < 8) {
        strong = '弱';
        className = 'medium';
        color = '#ff9900';
      } else if (this.passwordLen < 10) {
        strong = '中';
        className = 'medium';
        color = '#ff9900';
      }

      return {
        strong,
        class: 'demo-register-tip-' + this.passwordLen < 6 ? 'low' : (this.passwordLen < 10 ? 'medium' : 'strong'),
        percent: percent * 10,
        color
      }
    }
  },
  created() {
    this.getToken()
  },
  methods: {
    getToken() {
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
    handleChangePassword(val) {
      this.passwordLen = val.length;
    },
    handleSubmit(valid, { username, phone, email, password }) {
      if (valid) {

        API({
          url: '/api/user/reg',
          method: 'post',
          data: qs.stringify({ username: username, password: password , email:email , phone:phone }),
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
  },

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

.demo-register {
  width: 400px;
  margin: 0 auto !important;
}

.demo-register .ivu-poptip,
.demo-register .ivu-poptip-rel {
  display: block;
}

.demo-register-tip {
  text-align: left;
}

.demo-register-tip-low {
  color: #ed4014;
}

.demo-register-tip-medium {
  color: #ff9900;
}

.demo-register-tip-strong {
  color: #19be6b;
}

.demo-register-tip-title {
  font-size: 14px;
}

.demo-register-tip-desc {
  white-space: initial;
  font-size: 14px;
  margin-top: 6px;
}
</style>