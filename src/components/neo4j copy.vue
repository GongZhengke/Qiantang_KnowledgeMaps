<template>
    <div id="neo4jd3"></div>
  </template>
  
  <script>


  // import { IconSearch } from '@arco-design/web-vue/es/icon';
//   import userheaderVue from '@/components/userheader.vue';
  export default {
    setup() {
  
      return {
      }
    },
    data() {
      return {
  
      }
    },
    components: {
      // IconSearch
    //   userheaderVue
    },
    mounted(){
        this.load()
    },

    methods:{
        load(){
            onload = this.init;
            this.init();
        },
        init() {
                var neo4jd3 = new Neo4jd3('#neo4jd3', {
                    highlight: [
                        {
                            class: 'Project',
                            property: 'name',
                            value: 'neo4jd3'
                        }, {
                            class: 'User',
                            property: 'userId',
                            value: 'eisman'
                        }
                    ],
                    icons: {
//                        'Address': 'home',
                        'Api': 'gear',
//                        'BirthDate': 'birthday-cake',
                        'Cookie': 'paw',
//                        'CreditCard': 'credit-card',
//                        'Device': 'laptop',
                        'Email': 'at',
                        'Git': 'git',
                        'Github': 'github',
                        'Google': 'google',
//                        'icons': 'font-awesome',
                        'Ip': 'map-marker',
                        'Issues': 'exclamation-circle',
                        'Language': 'language',
                        'Options': 'sliders',
                        'Password': 'lock',
                        'Phone': 'phone',
                        'Project': 'folder-open',
                        'SecurityChallengeAnswer': 'commenting',
                        'User': 'user',
                        'zoomFit': 'arrows-alt',
                        'zoomIn': 'search-plus',
                        'zoomOut': 'search-minus'
                    },
                    images: {
                        'Address': '/docs/img/twemoji/1f3e0.svg',
//                        'Api': '/docs/img/twemoji/1f527.svg',
                        'BirthDate': '/docs/img/twemoji/1f382.svg',
                        'Cookie': '/docs/img/twemoji/1f36a.svg',
                        'CreditCard': '/docs/img/twemoji/1f4b3.svg',
                        'Device': '/docs/img/twemoji/1f4bb.svg',
                        'Email': '/docs/img/twemoji/2709.svg',
                        'Git': '/docs/img/twemoji/1f5c3.svg',
                        'Github': '/docs/img/twemoji/1f5c4.svg',
                        'icons': '/docs/img/twemoji/1f38f.svg',
                        'Ip': '/docs/img/twemoji/1f4cd.svg',
                        'Issues': '/docs/img/twemoji/1f4a9.svg',
                        'Language': '/docs/img/twemoji/1f1f1-1f1f7.svg',
                        'Options': '/docs/img/twemoji/2699.svg',
                        'Password': '/docs/img/twemoji/1f511.svg',
//                        'Phone': '/docs/img/twemoji/1f4de.svg',
                        'Project': '/docs/img/twemoji/2198.svg',
                        'Project|name|neo4jd3': '/docs/img/twemoji/2196.svg',
//                        'SecurityChallengeAnswer': '/docs/img/twemoji/1f4ac.svg',
                        'User': '/docs/img/twemoji/1f600.svg'
//                        'zoomFit': '/docs/img/twemoji/2194.svg',
//                        'zoomIn': '/docs/img/twemoji/1f50d.svg',
//                        'zoomOut': '/docs/img/twemoji/1f50e.svg'
                    },
                    minCollision: 60,
                    neo4jDataUrl: '/docs/json/neo4jData.json',
                    nodeRadius: 25,
                    onNodeDoubleClick: function(node) {
                        switch(node.id) {
                            case '25':
                                // Google
                                window.open(node.properties.url, '_blank');
                                break;
                            default:
                                var maxNodes = 5,
                                    data = neo4jd3.randomD3Data(node, maxNodes);
                                neo4jd3.updateWithD3Data(data);
                                break;
                        }
                    },
                    onRelationshipDoubleClick: function(relationship) {
                        console.log('double click on relationship: ' + JSON.stringify(relationship));
                    },
                    zoomFit: true
                });
            }

    }
  }
  </script>
  <style >
             .neo4jd3 {
                margin-top: 50px;
                margin-bottom: 50px;
                height: 600px;
                width: 100%;
                overflow: hidden;
            }
            .neo4jd3-graph {
    border: 0px solid #ddd!important;
    border-radius: 5px;
}
  </style>