import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import HomeView from "./views/HomeView.vue"

const baseTitle = "App"

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    component: HomeView,
    meta: {
      title: "Home"
    }
  },
  {
    path: "/login",
    component: () => import("./views/account/LoginView.vue"),
    meta: {
      title: "Login"
    }
  },
  {
    path: "/logout",
    component: () => import("./views/account/LogoutView.vue"),
    meta: {
      title: "Logout"
    }
  },
  {
    path: "/account",
    component: () => import("./views/account/CreateAccountView.vue"),
    meta: {
      title: "Create account"
    }
  },
  {
    path: "/activate/:token",
    component: () => import("./views/account/ActivateAccountView.vue"),
    meta: {
      title: "Activate account"
    }
  },
  {
    path: "/page",
    component: () => import("./views/PageView.vue"),
    meta: {
      title: "A page"
    }
  },
  {
    path: "/student",
    component: () => import("./views/skii/StudentView.vue"),
    meta: {
      title: "Student(s)"
    }
  },
  {
    path: "/student/:agent_pk",
    component: () => import("./components/skii/StudentSingle.vue"),
    props: true,
    meta: {
      title: "Student"
    }
  },
  {
    path: "/teacher",
    component: () => import("./views/skii/TeacherView.vue"),
    meta: {
      title: "Teacher(s)"
    }
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.afterEach((to, from) => {
  document.title = `${baseTitle} - ${to.meta?.title}`;
});

export default router
