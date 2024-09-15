<template>
  <div class="header" :style="{ height: this.height }">
    <a-space :size="12" direction="vertical" align="center">

      <a-typography-title :heading="1" style="margin: 0;color: cadetblue;">
        钱塘江流域知识图谱查询系统
      </a-typography-title>
      <div class="user-msg">
        <a-alert v-if="inconsidering" :style="{ marginTop: '30px' }">ZJWEUer KnowledgeGraph<br>正在搜索信息，请稍后~</a-alert>

        <a-input-search v-else v-model="searchKey" :style="{ width: '500px', marginTop: '30px' }" placeholder="请输入您要搜索的内容"
          search-button class="index-search" size="large" @search="search()">
          <template #button-icon>
            <icon-search style="color: white;" />
          </template>
          <template #button-default>
            搜索
          </template>
        </a-input-search>
      </div>
    </a-space>
  </div>


  <div class="home" v-if="update">

    <div class="index-info">

      <a-empty style="margin: auto;" v-if="update == false" />
      <!-- <neo4jVue v-if="update" :graphData="graphData"></neo4jVue> -->
      <div id="main" v-if="update" style="min-height: 700px;"></div>
    </div>


  </div>
</template>

<script>
import API from "../axios";
import qs from 'qs';
import { IconSearch } from '@arco-design/web-vue/es/icon';
import neo4jVue from '@/components/neo4j.vue';
export default {
  setup() {

    return {
    }
  },
  name: 'HomeView',
  data() {
    return {
      searchinfo: 1,
      update: false,
      inconsidering: false,
      graphData: [],
      searchKey: '',
      token: '',
      height: '804px'
    }
  },
  components: {
    IconSearch,
    neo4jVue
  },
  created() {
    this.getToken()
    var skey = this.$route.query.searchKey || null
    if (skey) {
      this.searchKey = skey
      this.search()
    }
  },
  methods: {
    search() {
      // this.$message.info({content:'服务端数据暂未对接',duration:1000})
      this.height = '250px';
      var uData = JSON.parse(sessionStorage.getItem('userData'))
      if (uData == null) {
        this.$message.info({ content: '用户未登录' })
        this.$router.push('/login')
      } else {
        if (this.searchKey == '') {
          this.$message.error('请输入关键字')
        } else {
          this.update = false
          // 在组件移除后，重新渲染组件
          // this.$nextTick可实现在DOM 状态更新后，执行传入的方法。

          this.inconsidering = true
          this.$nextTick(() => {
            this.$message.warning('正在搜索中')
            this.getData()
            this.update = true
          })
        }

      }

    },
    getData() {
      API({
        url: "/api/search",
        method: 'post',
        data: qs.stringify({ a1: this.searchKey }),
        headers: { 'X-CSRFToken': this.token }
      }).then((res) => {
        this.graphData = res.data
        if (this.graphData[0] == undefined) {
          this.$message.warning('暂无结果')
          this.update = false
          this.inconsidering = false
        } else {
          this.neo4j(this.graphData)
          this.$message.success('搜索成功')
          this.inconsidering = false
        }
      });
    },
    getToken() {
      API({
        url: '/api/getToken',
        method: 'get'
      })
        .then((res) => {
          this.token = res.data.csrftoken
        })
    },
    neo4j(graphData) {
      var myChart = echarts.init(document.getElementById('main'));
      var data = [];
      var links = [];
      var graph = graphData
      var name = '';
      name = graph[0].n1.name
      for (var i = 0; i < 30 && i < graph.length; ++i) {
        var node1 = {};
        var node2 = {};
        var link = {};
        var name1 = graph[i]['n1']['name'];
        var name2 = graph[i]['n2']['name'];
        var name3 = graph[i]['rel']['rel']

        if (this.searchKey == name2) {
          var t = name1;
          name1 = name2;
          name2 = t;
        }

        node1['name'] = name1;
        node1['des'] = node1['name'];
        node1['length'] = graph[i]['n1']['length']
        node1['area'] = graph[i]['n1']['area']
        node1['jd'] = graph[i]['n1']['jd']
        node1['wd'] = graph[i]['n1']['wd']
        node1['zcsw'] = graph[i]['n1']['zcsw']
        node1['intro'] = graph[i]['n1']['intro']
        node1['symbolSize'] = 50;
        node1['category'] = 0;

        node2['name'] = name2;
        node2['des'] = node2['name'];
        node2['length'] = graph[i]['n2']['length']
        node2['area'] = graph[i]['n2']['area']
        node2['jd'] = graph[i]['n2']['jd']
        node2['wd'] = graph[i]['n2']['wd']
        node2['zcsw'] = graph[i]['n2']['zcsw']
        node2['intro'] = graph[i]['n2']['intro']
        node2['symbolSize'] = 50;
        node2['category'] = 1;

        if (i == 0) data.push(node1);
        data.push(node2);

        link['source'] = name1;
        link['target'] = name2;
        link['name'] = name3;
        link['des'] = 'linkdes' + i;
        links.push(link);
      }


      var categories = [];
      for (var i = 0; i < 2; i++) {
        categories[i] = {
          name: '类目' + i
        };
      }


      var option = {
        // 图的标题
        title: {
          text: '搜索结果'
        },
        // 提示框的配置
        tooltip: {
          
          formatter: function (x) {
            // console.log(x);
            var disText = '';
            if (x.data.name != undefined && x.data.name !='') {
              disText += '名称：' + x.data.name
            }
            if (x.data.length != undefined && x.data.length !='') {
              disText += '</br>长度：' + x.data.length + 'km'
            }
            if (x.data.area != undefined && x.data.area !='') {
              disText += '</br>流域面积：' + x.data.area + 'km²'
            }
            if (x.data.jd != undefined && x.data.jd !='') {
              disText += '</br>经度：' + x.data.jd + '°'
            }
            if (x.data.wd != undefined && x.data.wd !='') {
              disText += '</br>纬度：' + x.data.wd + '°'
            }
            if (x.data.intro != undefined && x.data.intro !=''){
              var s = x.data.intro.length
              var t = s/20
              for(var i=0;i<t;i++){
                disText += '</br>' + x.data.intro.substring(i*20,(i+1)*20)
              }
              
            }
            // disText += '</br><b>' + x.data.name + '</b> <a href="">以此为关键字搜索</a>'
            return disText;
          }
        },
        // 工具箱
        toolbox: {
          // 显示工具箱
          show: true,
          feature: {
            mark: {
              show: true
            },
            // 还原
            restore: {
              show: true
            },
            // 保存为图片
            saveAsImage: {
              show: true
            }
          }
        },
        series: [{
          type: 'graph', // 类型:关系图
          layout: 'force', //图的布局，类型为力导图
          symbolSize: 50, // 调整节点的大小
          roam: true, // 是否开启鼠标缩放和平移漫游。默认不开启。如果只想要开启缩放或者平移,可以设置成 'scale' 或者 'move'。设置成 true 为都开启
          animation: false,
          edgeSymbol: ['circle', 'arrow'],
          edgeSymbolSize: [2, 10],
          edgeLabel: {
            normal: {
              textStyle: {
                fontSize: 20
              }
            }
          },
          force: {
            repulsion: 200,
            gravity: 0.05,
            edgeLength: 300,
            layoutAnimation: true
          },
          // force: {
          //   edgeLength: 300,
          //   repulsion: 200,
          //   gravity: 0.2,
          //   layoutAnimation: true
          // },
          draggable: true,
          lineStyle: {
            normal: {
              width: 2,
              color: '#4b565b',
            }
          },
          edgeLabel: {
            normal: {
              show: true,
              formatter: function (x) {
                return x.data.name;
              }
            }
          },
          label: {
            normal: {
              show: true,
              textStyle: {
                color: '#4b565b',
              },
              formatter: function (x) {
                return x.data.name;
              }
            }
          },


          // 数据
          data: data,
          links: links,
          categories: categories,
        }]
      };
      myChart.setOption(option);



      myChart.on('click', function (param) {
        // console.log(param.name);
        window.location.href = '?searchKey=' + param.name
      })

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

.index-search {
  margin: auto;
  display: flex;
}

.index-info {
  display: flex;
  min-height: 600px;
}



.header {
  display: flex;
  align-items: center;
  justify-content: center;

  color: var(--gray-10);
  background: url(//p3-armor.byteimg.com/tos-cn-i-49unhts6dw/41c6b125cc2e27021bf7fcc9a9b1897c.svg~tplv-49unhts6dw-image.image) no-repeat;
  background-size: cover;
  border-radius: 4px;
  margin-bottom: 10px;

}

.header :deep(.arco-avatar-trigger-icon-button) {
  color: rgb(var(--arcoblue-3));

}

.header :deep(.arco-avatar-trigger-icon-button) :deep(.arco-icon) {
  vertical-align: -1px;
}

.header .user-msg .arco-typography {
  margin-left: 6px;
}

.header .user-msg .arco-icon {
  color: rgb(var(--gray-10));
}
</style>