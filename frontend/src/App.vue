<template>
  <div :class="{ dark: user.isDarkMode.value == true }">
    <div class="flex flex-col h-full min-h-screen lightbg">
      <the-header></the-header>
      <div class="flex-grow w-full pb-24">
        <Menubar :model="items">
            <template #start>
            </template>
            <template #end>
                <InputText placeholder="Search" type="text" />
            </template>
        </Menubar>
        <router-view></router-view>
      </div>
    </div>
    <Toast />
    <ConfirmDialog>
      <template #message="slotProps">
        <div class="flex flex-row items-center p-4">
          <div>
            <named-icon :icon="`${slotProps.message.icon}`" class="text-3xl"></named-icon>
          </div>
          <div class="pl-2">{{ slotProps.message.message }}</div>
        </div>
      </template>
    </ConfirmDialog>
  </div>
</template>

<script setup lang="ts">
import { onBeforeMount, onMounted, ref } from 'vue';
import Toast from 'primevue/toast';
import ConfirmDialog from 'primevue/confirmdialog';
import TheHeader from "@/components/TheHeader.vue";
import Menubar from 'primevue/menubar';
import InputText from 'primevue/inputtext';
import { initState, initUserState, user } from '@/state';
const items = ref([
      {
          label: 'Profile',
          icon: 'pi pi-fw pi pi-fw pi-user',
          items: [
              {
                  label: 'Student',
                  icon: 'pi pi-fw pi-user-plus',
                  to: { "name": "list_student_record" }
              },
              {
                  label: 'Teacher',
                  icon: 'pi pi-fw pi-user-plus',
                  to: { "name": "list_teacher_record" }
              },
              {
                  separator: true
              },
              {
                  label: 'Location',
                  icon: 'pi pi-fw pi-user-plus',
                  to: { "name": "list_location_record" }
              },
          ]
      },
      {
        label: 'Events',
        icon: 'pi pi-fw pi-calendar',
        items: [
            {
                label: 'Edit',
                icon: 'pi pi-fw pi-pencil',
                items: [
                    {
                        label: 'Save',
                        icon: 'pi pi-fw pi-calendar-plus'
                    },
                    {
                        label: 'Delete',
                        icon: 'pi pi-fw pi-calendar-minus'
                    }
                ]
            },
            {
                label: 'Archieve',
                icon: 'pi pi-fw pi-calendar-times',
                items: [
                    {
                        label: 'Remove',
                        icon: 'pi pi-fw pi-calendar-minus'
                    }
                ]
            }
        ]
    },
    {
        label: 'Quit',
        icon: 'pi pi-fw pi-power-off'
    }
])
onBeforeMount(() => initState());
onMounted(() => initUserState());
</script>

<style lang="sass">
.app-form
  & input, .p-dropdown
    @apply w-full xxs:min-w-[22rem] xs:min-w-[24rem]
.p-dialog
  & .p-button.successbtn, .p-button.successbtn:enabled:hover
    @apply success border-none ring-0
  & .p-button.dangerbtn, .p-button.dangerbtn:enabled:hover
    @apply danger border-none ring-0
  & .p-button.warningbtn, .p-button.warningbtn:enabled:hover
    @apply warning border-none ring-0

</style>




