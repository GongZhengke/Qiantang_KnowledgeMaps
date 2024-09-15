<template>

    <div>
        <a-table :columns="columns" :data="data" />

    </div>
</template>
  
<script>
import { ref } from 'vue';
// import { IconSearch } from '@arco-design/web-vue/es/icon';
import API from "../../axios";
export default {
    setup() {
        const columns = [
            {
                title: '用户名',
                dataIndex: 'username',
            },
            {
                title: '手机号',
                dataIndex: 'phone',
            },
            {
                title: '邮箱',
                dataIndex: 'email',
            },
            {
                title: '权限',
                dataIndex: 'is_superuser',
            },
        ];
        let data = ref([]);

        API({
            url: "/api/admin/user/list",
            method: "get",
        }).then((res) => {
            if (res.data.errcode == 200) {
                data.value = res.data.user
            }
        });
        
        return {
            columns,
            data
        }
    },
    name: 'HomeView',
    data() {
        return {
            loginStatue: 0,
            superuser: '',

        }
    },
    components: {


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
                        this.superuser = res.data.user[0].is_superuser
                    } else {
                        this.loginStatue = 0;
                        this.$router.push('/login')
                    }
                });
            } else {
                this.loginStatue = 1;
                this.superuser = uData.is_superuser
                if (this.superuser != 1) {
                    this.$router.push('/');
                } else {
                }
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