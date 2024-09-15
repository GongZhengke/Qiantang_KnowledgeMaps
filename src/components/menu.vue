<template>
    <div class="menu-demo">
        <a-menu mode="horizontal" :selected-keys="selectedKeys">
            <a-menu-item key="0" :style="{ padding: 0, marginRight: '38px' }" disabled>
                <div :style="{
                    width: '250px',
                    height: '30px',
                    borderRadius: '2px',
                    color: 'black',
                    fontSize: '20px',
                    cursor: 'text',
                }">
                    ZJWEUer KnowledgeGraph
                </div>
            </a-menu-item>
            <a-menu-item key="home" @click="changePage('/')"> 首页 </a-menu-item>
            <a-menu-item key="qs" @click="changePage('/qs')"> 智能问答 </a-menu-item>

            <a-menu-item key="0" class="right-avatar" :style="{ padding: 0, marginRight: '20px' }" disabled>
                <div :style="{
                    cursor: 'text',
                }">
                    <a-dropdown trigger="hover" v-if="loginStatue == 1">
                        <a-button type="text" style="color: var(--color-text-2)">
                            <template #icon>
                                <i class="b2font b2-user-heart-line b2-light b2-color"></i>
                            </template>
                            <template #default>{{username}}</template>
                        </a-button>
                        <template #content>
                            <a-doption @click="changePage('/profile')">个人资料</a-doption>
                            <a-doption @click="changePage('/settings')">安全设置</a-doption>
                            <a-doption @click="changePage('/admin/user/list')" v-if="superuser == 1">用户管理</a-doption>
                            <a-doption @click="logout()">退出登录</a-doption>
                        </template>
                    </a-dropdown>

                    <a-button type="text" style="color: var(--color-text-2)" v-if="loginStatue == 0"
                        @click="changePage('/login')">
                        <template #icon>
                            <i class="b2font b2-user-heart-line b2-light b2-color"></i>
                        </template>
                        <template #default>登录/注册</template>
                    </a-button>
                </div>
            </a-menu-item>
        </a-menu>
    </div>
</template>

<script>
import API from "../axios";
import qs from 'qs';
import { ref } from "vue";
export default {
    setup() { },
    name: "HomeView",
    data() {
        return {
            selectedKeys: [],
            loginStatue: 0,
            username:'',
            superuser:''
        };
    },
    components: {},
    methods: {
        changePage(url) {
            this.$router.push(url);
        },
        getKey() {
            let namer = this.$route.name;
            this.selectedKeys = [namer];
        },
        logout() {
            API({
                url: "/api/user/logout",
                method: "get",
            }).then((res) => {
                if (res.data.errcode == 200) {
                    this.$message.success({ content: res.data.errmsg });
                    sessionStorage.clear();
                    this.$router.push("/");
                    this.loginStatue = 0;
                } else {
                    this.$message.warning({ content: res.data.errmsg });
                }
            });
        },
        userinfo() {
            var uData = JSON.parse(sessionStorage.getItem('userData'))
            if (uData==null){
                API({
                    url: "/api/user/info",
                    method: "get",
                }).then((res) => {
                    if (res.data.errcode == 200) {
                        this.loginStatue = 1;
                        this.username = res.data.user[0].username
                        this.superuser = res.data.user[0].is_superuser
                        sessionStorage.setItem('userData',JSON.stringify(res.data.user[0]))
                    } else {
                        this.loginStatue = 0;
                    }
                });
            }else{
                this.loginStatue = 1;
                this.username = uData.username
                this.superuser = uData.is_superuser
            }

        },
    },

    created() { },
    watch: {
        // 监听路由
        $route() {
            this.getKey();
            this.userinfo();
        },
    },
};
</script>
<style scoped>
.menu-demo {
    box-sizing: border-box;
    width: 100%;
    padding: 0;
    background-color: var(--color-neutral-2);
    position: fixed;
    z-index: 1002;
}

.right-avatar {
    right: 0;
    position: absolute !important;
}
</style>
