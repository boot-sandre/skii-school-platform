
<template>
    <div class="flex flex-col centered-container">
      <h1 class="text-center">
        Teachers Space
      </h1>
      <div v-if="teacher" class="flex flex-col items-center my-8 space-y-5">
            <div class="grid mx-3 formgrid p-fluid">
              <div class="mb-4 ield col-12 md:col-6">
                <label for="username">Username</label>
                <InputText type="text" v-model="teacher.user.username" id="username"/>
              </div>
              <div class="mb-4 ield col-12 md:col-6">
                <label for="email">Email</label>
                <InputText type="text" v-model="teacher.user.email" id="email"/>
              </div>
              <div class="mb-4 ield col-12 md:col-6">
                <label for="first_name">Firstname</label>
                <InputText type="text" v-model="teacher.user.first_name" id="first_name"/>
              </div>
              <div class="mb-4 ield col-12 md:col-6">
                <label for="last_name">Lastname</label>
                <InputText type="text" v-model="teacher.user.last_name" id="last_name"/>
              </div>
              <button class="px-5 mt-5 border-2 border-gray-400 rounded-md btn txt-light p-button-sm" @click="saveRecord(Boolean(!props.djangoPk))">Save</Button>
              <button class="px-5 mt-5 border-2 border-gray-400 rounded-md btn txt-light p-button-sm" @click="$router.back()">Cancel</Button>
              </div>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { onBeforeMount, shallowRef } from 'vue';
  import { StudentAgentContract, StudentSingleResponse } from "@/interfaces";
  import { api, user, forms } from '@/state';
  import router from '@/router';
  import FormCard from '@/widgets/FormCard.vue';
  import InputText from 'primevue/inputtext';
  import Button from 'primevue/button';
  import { confirmDanger, msg } from '@/notify';
  
  const teacher = shallowRef<StudentAgentContract>({
    user: {
      first_name: "",
      last_name: "",
      email: "",
      id: null,
      username: "user",
      is_active: true,
    },
    id: null,
  })

  const props = defineProps({
    djangoPk: {
      type: String,
      required: true,
    }
  });
  
  async function load() {
      console.log("Component TeacherAgentRecord loading");
      console.log("djangoPk: " + props.djangoPk);
      fetchRecord()
  }

  async function fetchRecord() {
    const is_digits: boolean = Boolean(
      String(Number(props.djangoPk)) === props.djangoPk)
    if ( is_digits ) {
      const res = await api.get<StudentSingleResponse>(
        `/skii/teacher/fetch/${props.djangoPk}/`);
      if (res.ok) {
        teacher.value = res.data.item;
      }
    }
  }
  
  function saveRecord(creation=false) {
    confirmDanger(
      `Save the ${teacher.value.user.username} teacher?`,
      "The teacher will be permanently modified",
      async () => {
        var url:string = ""
        if (creation) {
          url = `/skii/teacher/create/`;
        } else {
          url = `/skii/teacher/save/${props.djangoPk}/`;
        }
        const payload = teacher.value;
        console.log("saveRecord url", url);
        console.log("saveRecord payload", payload);
        const { error, res, errors } = await forms.post(url, payload);
        if (res.ok) {
          // Notify user about deleteRecord success
          msg.success("Teacher saved", "The teacher has been successfuly saved");
          // Refresh current component
          teacher.value = res.data.item;
          router.push({name: "list_teacher_record"})
        }
      }
    )
  }

  function deleteRecord(teacher: StudentAgentContract) {
    confirmDanger(
      `Delete the ${teacher.id} teacher?`,
      "The teacher will be permanently deleted",
      async () => {
        const url = `/skii/teacher/delete/${teacher.id}/`;
        console.log("deleteRecord url", url);
        const res = await api.del(url);
        if (res.ok) {
          // Notify user about deleteRecord success
          msg.success("Teacher deleted", "The teacher has been successfuly deleted");
          // Get back to teacher list
          router.push({ name: "list_teacher_record"});
        }
      }
    )
  }
  
  onBeforeMount(() => load())

  </script>
  