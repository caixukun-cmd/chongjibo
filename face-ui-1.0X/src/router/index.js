import Vue from 'vue'
import VueRouter from 'vue-router'
import login from '../views/login/index'
import desktop from '../components/desktop/index'
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'login',
    component: login
  },
  {
    path: '/home',
    name: 'home',
    component: () => import('@/views/home/index'),
    redirect: '/desktop',
    children:[
      {
        path: '/desktop',
        name: 'desktop',
        component: desktop
      },
      {
        path: '/faceList',
        name: 'face',
        component: () => import('@/components/face/index')
      },
      {
        path: '/faceLog',
        name: 'log',
        component: () => import('@/components/faceLog/index')
      },
      {
        path: '/videoCamera',
        name: 'video',
        component: () => import('@/components/videoCamera/index')
      },
      {
        path: '/warning',
        name: 'video',
        component: () => import('@/components/warning/index')
      },
      // 新增的路由配置
      {
        path: '/viewLogs',
        name: 'viewLogs',
        component: () => import('@/components/viewLogs/index')
      }
    ]
  }
]

const router = new VueRouter({
  routes
})


router.beforeEach((to,from,next)=>{
  if(to.path === '/') return next()
  let face_token = localStorage.getItem("face_token");
  if (!face_token) return next("/")
  next()
})

export default router
