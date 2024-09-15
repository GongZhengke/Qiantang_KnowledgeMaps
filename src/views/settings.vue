<template>
  <userheaderVue :username="username" :userid="userid" :email="email" :staff="staff"
    :phone="phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2')"></userheaderVue>
  <div class="home">

    <div class="index-info">

      <a-empty style="margin: auto;" />

    </div>


  </div>
</template>

<script>
// import { IconSearch } from '@arco-design/web-vue/es/icon';
import API from "../axios";

import userheaderVue from '@/components/userheader.vue';
export default {
  setup() {

    return {
    }
  },
  name: 'HomeView',
  data() {
    return {
      loginStatue: 0,
      username: '',
      userid: '',
      email: '',
      staff: '',
      phone: ''
    }
  },
  components: {
    // IconSearch
    userheaderVue
  },
  methods: {
    userinfo() {
      var uData = JSON.parse(sessionStorage.getItem('userData'))
      if (uData == null) {
        API({
          url: "/api/user/info",
          method: "get",
        }).then((res) => {
          if (res.data.errcode == 200) {
            this.loginStatue = 1;
            sessionStorage.setItem('userData', JSON.stringify(res.data.user[0]))
            this.userid = res.data.user[0].userid
            this.username = res.data.user[0].username
            this.email = res.data.user[0].email
            this.staff = res.data.user[0].is_staff
            this.phone = res.data.user[0].phone
          } else {
            this.loginStatue = 0;
            this.$router.push('/login')
          }
        });
      } else {
        this.loginStatue = 1;
        this.userid = uData.userid
        this.username = uData.username
        this.email = uData.email
        this.staff = uData.is_staff
        this.phone = uData.phone
      }
    },
  },
  created() {
    this.userinfo();
  }

}
</script>
<style scoped>
.home {
  background-color: #fff;
  min-height: 100px;
  padding: 30px;
  padding-bottom: 5px;
  border-radius: 3px;
}


.index-info {
  display: flex;
  min-height: 500px;
}
</style>