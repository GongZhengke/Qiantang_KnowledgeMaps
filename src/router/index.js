import {
  createRouter,
  createWebHistory
} from 'vue-router'


const routes = [{
    path: '/',
    name: 'home',
    component: () => import('../views/home.vue'),
    meta: {
      title: '首页'
    }
  }, {
    path: '/qs',
    name: 'qs',
    component: () => import('../views/qs.vue'),
    meta: {
      title: '智能问答'
    }
  },
  {
    path: '/profile',
    name: 'profile',
    component: () => import('../views/profile.vue'),
    meta: {
      title: '个人资料'
    }
  },
  {
    path: '/settings',
    name: 'settings',
    component: () => import('../views/settings.vue'),
    meta: {
      title: '安全设置'
    }
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/login.vue'),
    meta: {
      title: '登录'
    }
  },
  {
    path: '/reg',
    name: 'reg',
    component: () => import('../views/reg.vue'),
    meta: {
      title: '注册'
    }
  },
  // Admin
  {
    path: '/admin/user/list',
    name: 'userlist',
    component: () => import('../views/admin/userlist.vue'),
    meta: {
      title: '用户列表'
    }
  },
]




const router = createRouter({
  history: createWebHistory(),
  routes,
})


router.beforeEach((to, from, next) => { //beforeEach是router的钩子函数，在进入路由前执行
  if (to.meta.title) { //判断是否有标题
    document.title = to.meta.title + '｜钱塘江流域知识图谱查询系统'
  } else {
    document.title = '钱塘江流域知识图谱查询系统'
  }
  next() //执行进入路由，如果不写就不会进入目标页
})

export default router