<template>
  <sw-header class="fixed top-0 left-0 z-40 w-screen h-16" :class="css ? css : 'primary'"
    @togglemenu="isMenuVisible = !isMenuVisible">
    <template #branding>
      <div class="flex flex-row items-center h-full cursor-pointer" @click="$router.push('/')">
        <div class="mx-3">
          <i-twemoji:ninja-medium-light-skin-tone class="text-5xl"></i-twemoji:ninja-medium-light-skin-tone>
        </div>
        <div class="text-2xl txt-lighter">Django Spa Ninja</div>
      </div>
    </template>
    <template #mobile-branding>
      <div class="inline-flex flex-row items-center h-full pt-1 ml-2 text-2xl truncate" @click="$router.push('/')">
        <div class="flex flex-row items-center h-full">
          <i-twemoji:ninja-medium-light-skin-tone class="mx-3 text-5xl"></i-twemoji:ninja-medium-light-skin-tone>
          <div class="text-2xl txt-lighter">Django Spa Ninja</div>
        </div>
      </div>
    </template>
    <template #mobile-back>
      <div class="pl-2 text-2xl" v-show="loc != '/'">
        <i-eva:arrow-back-outline />
      </div>
    </template>
    <template #menu>
      <div class="flex flex-row items-center justify-end h-full">
        <button v-for="link in links" class="border-none btn" @click="closeMenu(); $router.push(link.href)"
          v-html="link.name"></button>
        <py-status :py="py"></py-status>
        <a :href="repoUrl" class="btn">
          <i-fa-brands:github class="text-2xl" @click=""></i-fa-brands:github>
        </a>
        <div class="px-5 text-lg cursor-pointer txt-lighter dark:txt-light" @click="toggleDarkMode()">
          <i-fa-solid:moon v-if="!user.isDarkMode.value"></i-fa-solid:moon>
          <i-fa-solid:sun v-else></i-fa-solid:sun>
        </div>
      </div>
    </template>
  </sw-header>
  <sw-mobile-menu :is-visible="isMenuVisible" class="absolute left-0 z-30 w-full lighter top-14">
    <div class="flex flex-col p-3 space-y-5">
      <button v-for="link in links" class="border-none btn" @click="closeMenu(); $router.push(link.href)"
        v-html="link.name"></button>
      <div class="pr-5 text-lg" @click="closeMenu(); toggleDarkMode()">
        <i-fa-solid:moon v-if="!user.isDarkMode.value"></i-fa-solid:moon>
        <i-fa-solid:sun v-else></i-fa-solid:sun>
      </div>
    </div>
  </sw-mobile-menu>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { SwHeader, SwMobileMenu } from "@snowind/header";
import { PyStatus } from "vuepython"
import { user, py } from "@/state";
import { libTitle, repoUrl } from "@/conf";
import { useRouter } from "vue-router";

defineProps({
  css: {
    type: String,
    default: "",
  },
  skipDarkModeToggle: {
    type: Boolean,
    default: false,
  },
  libTitle: {
    type: String,
    required: true,
  },
  links: {
    type: Object as () => Array<{ href: string, name: string }>,
    required: true,
  }
});

const router = useRouter();

const isMenuVisible = ref(false);

const loc = computed(() => window.location.pathname);

function closeMenu() {
  isMenuVisible.value = false;
}

function toggleDarkMode() {
  user.toggleDarkMode();
  router.go(0)
}
</script>