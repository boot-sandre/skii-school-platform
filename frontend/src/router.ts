import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import HomeView from "./views/HomeView.vue"
import NotFound from "./views/NotFound.vue"

const baseTitle = "App"

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "home",
    component: HomeView,
    meta: {
      title: "Home",
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
    component: () => import("./views/skii/StudentView.vue"),
    path: "/student/fetch/list",
    name: "list_student_record",
    meta: {
      title: "Student(s)",
    }
  },
  {
    component: () => import("./components/skii/Student.vue"),
    path: "/student/:djangoPk",
    name: "fetch_student_record",
    props: true,
    meta: {
      title: "Student",
    }
  },
  {
    component: () => import("./components/skii/StudentSingle.vue"),
    path: "/student/create",
    name: "create_student_record",
    props: true,
    meta: {
      title: "Student",
    }
  },
  {
    path: "/teacher",
    component: () => import("./views/skii/TeacherView.vue"),
    name: 'user-view',
    meta: {
      title: "Teacher(s)"
    },
    children: [
      {
        component: () => import("./components/skii/TeacherList.vue"),
        path: "/teacher/list",
        name: "list_teacher_record",
        meta: {
          title: "Teacher(s)",
        }
      },
      {
        component: () => import("./components/skii/Teacher.vue"),
        path: "/teacher/fetch/:djangoPk/",
        name: "fetch_teacher_record",
        props: true,
        meta: {
          title: "Teacher",
        }
      },
      {
        component: () => import("./components/skii/Teacher.vue"),
        path: "/teacher/create",
        name: "create_teacher_record",
        props: true,
        meta: {
          title: "Teacher",
        }
      },
    ],
    
  },
  
  
  
  {
    path: "/:catchAll(.*)",
    component: NotFound,
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
