import Vue from "vue";
import VueRouter from "vue-router";
import DashboardLayout from '@/views/DashboardLayout.vue';
import AuthLayout from '@/views/authentication/AuthLayout.vue';
import store from "@/store"

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    redirect: "locations",
    component: DashboardLayout,
    meta: {
      requiresAuth: true
    },
    children: [
      {
        path: "/locations",
        name: "location",
        component: () =>
          import(/* webpackChunkName: "locations" */ "../views/Locations.vue")
      },
      {
        path: "/departments",
        name: "department",
        component: () =>
          import(/* webpackChunkName: "departments" */ "../views/Departments.vue")
      },
      {
        path: "/categories",
        name: "category",
        component: () =>
          import(/* webpackChunkName: "categories" */ "../views/Categories.vue")
      },
      {
        path: "/subcategories",
        name: "subcategory",
        component: () =>
          import(/* webpackChunkName: "subcategories" */ "../views/Subcategories.vue")
      },
      {
        path: "/skus",
        name: "skus",
        component: () =>
          import(/* webpackChunkName: "skus" */ "../views/SKU.vue")
      },
      {
        path: "/infograph",
        name: "infograph",
        component: () =>
          import(/* webpackChunkName: "infograph" */ "../views/InfoGraph.vue")
      },
    ]
  },
  {
    path: '/',
    redirect: 'login',
    component: AuthLayout,
    children: [
      {
        path: '/login',
        name: 'login',
        component: () => import(/* webpackChunkName: "demo" */ '../views/authentication/Login.vue')
      }
    ]
  }

];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

router.beforeEach((to, from, next) => {
  if(to.matched.some(record => record.meta.requiresAuth)) {
    if (store.getters.isLoggedIn) {
      next()
      return
    }
    next('/login')
  } else {
    next()
  }
})

export default router;
