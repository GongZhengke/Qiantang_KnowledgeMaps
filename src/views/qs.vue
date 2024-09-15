<template>
    <div class="home">
        <a-alert v-if="inconsidering" :style="{ width: '70%', margin: '0 auto', marginTop: '30px' }">ZJWEUer AI
            正在搜索问题答案，请稍后~</a-alert>
        <a-input-search v-else v-model="searchKey" :style="{ width: '70%', marginTop: '30px' }" placeholder="请输入您要提问的内容"
            search-button class="index-search" size="large" @search="search()">
            <template #button-icon>
                <icon-search />
            </template>
            <template #button-default>
                发送问题
            </template>
        </a-input-search>
        <div class="index-info">

            <a-empty style="margin: auto;" v-if="update == false" />

            <div id="main" v-if="update">
                <a-comment style="margin-bottom: 30px;" v-for="(item, index) in qsData" :key="index" :author="item.author"
                    :datetime="item.time" :content="item.content">
                    <template #avatar>
                        <a-avatar>
                            <svg t="1677773831549" class="icon" viewBox="0 0 1024 1024" version="1.1"
                                xmlns="http://www.w3.org/2000/svg" p-id="8370" width="128" height="128">
                                <path
                                    d="M0.00001 512.077A511.923 511.923 0 1 0 511.92301 0 511.974 511.974 0 0 0 0.00001 512.077z"
                                    fill="#FFFFFF" p-id="8371"></path>
                                <path
                                    d="M887.49001 857.89c-13.697-71.82-139.895-140.459-253.165-177.96-5.54-1.846-40.014-17.339-18.417-82.798 56.43-57.815 99.214-150.924 99.214-242.597 0-140.82-93.827-214.742-202.891-214.742s-202.635 73.82-202.635 214.742c0 91.98 42.784 185.45 99.317 243.162 22.059 57.712-17.34 79.207-25.65 82.08-107.73 38.834-232.903 107.73-246.702 177.96a511.307 511.307 0 1 1 887.49-346.635 507.87 507.87 0 0 1-136.56 346.788"
                                    fill="#B8D4FF" p-id="8372"></path>
                            </svg>
                        </a-avatar>
                    </template>
                </a-comment>

            </div>
        </div>




    </div>
</template>
  
<script>
// import { IconSearch } from '@arco-design/web-vue/es/icon';
import API from "../axios";
import { IconSearch } from '@arco-design/web-vue/es/icon';
export default {
    setup() {

        return {
        }
    },
    name: 'HomeView',
    data() {
        return {
            update: true,
            inconsidering: false,
            searchKey: '',
            qsData: [
                {
                    'author': '智能问答机器人',
                    'content': '正在等待您的问题 ...',
                    'time': this.getTime()
                }
            ]
        }
    },
    components: {
        IconSearch

    },
    methods: {
        search() {
            var uData = JSON.parse(sessionStorage.getItem('userData'))
            if (uData == null) {
                this.$message.info({ content: '用户未登录' })
                this.$router.push('/login')
            } else {
                this.qsData.unshift(
                    {
                        'author': '我',
                        'content': this.searchKey,
                        'time': this.getTime()
                    }
                )
                var skey = this.searchKey
                this.searchKey = ''
                this.$message.loading('正在加载，请稍后！')
                this.inconsidering = true
                API({
                    url: '/api/chat/qs?question=' + skey,
                    method: 'get'
                })
                    .then(res => {
                        this.$message.success('获取成功！')
                        this.qsData.unshift(
                            {
                                'author': '智能问答机器人',
                                'content': res.data.answerData.choices[0].message.content,
                                'time': this.getTime()

                            }
                        )
                        this.inconsidering = false
                    }).catch(err => {
                        this.qsData.unshift(
                            {
                                'author': '智能问答机器人',
                                'content': '机器人开小差啦～请换个问题或者重新提问！',
                                'time': this.getTime()
                            }
                        )
                        this.inconsidering = false
                    })
            }
        },
        getTime() {
            let myDate = new Date()
            let wk = myDate.getDay()
            let yy = String(myDate.getFullYear())
            let mm = myDate.getMonth() + 1 < 10 ? '0' + (myDate.getMonth() + 1) : myDate.getMonth() + 1
            let dd = String(myDate.getDate() < 10 ? '0' + myDate.getDate() : myDate.getDate())
            let hou = String(myDate.getHours() < 10 ? '0' + myDate.getHours() : myDate.getHours())
            let min = String(myDate.getMinutes() < 10 ? '0' + myDate.getMinutes() : myDate.getMinutes())
            let sec = String(myDate.getSeconds() < 10 ? '0' + myDate.getSeconds() : myDate.getSeconds())
            let weeks = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']
            let week = weeks[wk]
            let nowTime = hou + ':' + min + ':' + sec
            return nowTime
        }
    },
    created() {

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

#main {
    padding: 50px 250px 50px 250px;
}

.index-search {
    margin: auto;
    display: flex;
}

.index-info {
    display: flex;
    min-height: 600px;
}
</style>