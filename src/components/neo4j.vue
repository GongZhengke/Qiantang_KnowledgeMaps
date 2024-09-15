<template>
    <div id="main" class="col-12"></div>
</template>
  
<script>


// import { IconSearch } from '@arco-design/web-vue/es/icon';
//   import userheaderVue from '@/components/userheader.vue';
export default {
    setup() {

        return {
        }
    },
    props:['graphData'],
    data() {
        return {
            searchKey: '钱塘江'
        }
    },
    components: {
        // IconSearch
        //   userheaderVue
    },
    mounted() {
        this.load()
    },
    created(){
        console.log(this.graphData);
    },
    methods: {
        load() {
            onload = this.init(this.graphData);
            this.init(this.graphData);
        },
        init(graphData) {
            var myChart = echarts.init(document.getElementById('main'));
            var data = [];
            var links = [];
            var graph = graphData
            console.log(graph);
            var name = '';
            name = graph[0].n1.name
            console.log(name);
            for (var i = 0; i < 30 && i < graph.length; ++i) {
                node1 = {};
                node2 = {};
                link = {};
                var name1 = graph[i]['n1']['name'];
                var name2 = graph[i]['n2']['name'];
                var name3 = graph[i]['rel']['rel']

                if (searchKey == name2) {
                    var t = name1;
                    name1 = name2;
                    name2 = t;
                }

                node1['name'] = name1;
                node1['des'] = node1['name'];
                node1['symbolSize'] = 50;
                node1['category'] = 0;

                node2['name'] = name2;
                node2['des'] = node2['name'];
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


            option = {
                // 图的标题
                title: {
                    text: '知识图谱(可以使用鼠标滚轮缩放哦)'
                },
                // 提示框的配置
                tooltip: {
                    formatter: function (x) {
                        return x.data.des;
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
                        repulsion: 1200,
                        edgeLength: [10, 30]
                    },
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
                            textStyle: {}
                        }
                    },

                    // 数据
                    data: data,
                    links: links,
                    categories: categories,
                }]
            };
            myChart.setOption(option);
        }

    }
}
</script>
<style >
#main {
    margin-top: 50px;
    margin-bottom: 50px;
    height: 600px;
    width: 100%;
    overflow: hidden;
}

/* .neo4jd3-graph {
    border: 0px solid #ddd!important;
    border-radius: 5px;
} */
</style>