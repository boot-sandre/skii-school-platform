
<template>
    <div class="flex flex-col centered-container">
      <h1 class="text-center">
        Students Space
      </h1>
      <div v-if="student" class="flex flex-col items-center my-8 space-y-5">
            <form-card class="mx-3">
              <span>
                <label for="username">Username</label>
                <InputText type="text" v-model="student.user.username" id="username"/>
              </span>
              <span>
                <label for="email">Email</label>
                <InputText type="text" v-model="student.user.email" id="email"/>
              </span>
              <span>
                <label for="first_name">Firstname</label>
                <InputText type="text" v-model="student.user.first_name" id="first_name"/>
              </span>
              <span>
                <label for="last_name">Lastname</label>
                <InputText type="text" v-model="student.user.last_name" id="last_name"/>
              </span>
              <button class="mt-5 btn txt-light" @click="$router.back()">Cancel</button>
              <button class="w-full btn bord-background success" @click="saveRecord()">Save</button>
            </form-card>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { onBeforeMount, ref } from 'vue';
  import { StudentAgentContract, StudentSingleResponse } from "@/interfaces";
  import { api, user, forms } from '@/state';
  import router from '@/router';
  import FormCard from '@/widgets/FormCard.vue';
  import InputText from 'primevue/inputtext';
  import Button from 'primevue/button';
  import { confirmDanger, msg } from '@/notify';
  
  const student = ref<StudentAgentContract>({
    user: {
      first_name: "",
      last_name: "",
      email: "",
      id: null,
      last_login: null,
      username: "user",
      is_active: true,
      date_joined: null,
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
      console.log("Component StudentAgentRecord loading");
      console.log("djangoPk: " + props.djangoPk);
      fetchRecord()
  }

  async function fetchRecord() {
    const is_digits: boolean = Boolean(
      String(Number(props.djangoPk)) === props.djangoPk)
    if ( is_digits ) {
      const res = await api.get<StudentSingleResponse>(
        `/skii/models/student/${props.djangoPk}`);
      if (res.ok) {
        student.value = res.data.item;
      }
    }
  }
  
  function saveRecord() {
    confirmDanger(
      `Save the ${student.value.user.username} student?`,
      "The student will be permanently modified",
      async () => {
        const url = `/skii/models/student/save/${props.djangoPk}`;
        const payload = student.value;
        console.log("saveRecord url", url);
        console.log("saveRecord payload", payload);
        const { error, res, errors } = await forms.post(url, payload);
        if (res.ok) {
          // Notify user about deleteRecord success
          msg.success("Student saved", "The student has been successfuly saved");
          // Refresh current component
          student.value = res.data.item;
          router.push({name: "list_student_record"})
        }
      }
    )
  }

  function deleteRecord(student: StudentAgentContract) {
    confirmDanger(
      `Delete the ${student.id} student?`,
      "The student will be permanently deleted",
      async () => {
        const url = `/skii/models/student/delete/${student.id}`;
        console.log("deleteRecord url", url);
        const res = await api.del(url);
        if (res.ok) {
          // Notify user about deleteRecord success
          msg.success("Student deleted", "The student has been successfuly deleted");
          // Get back to student list
          router.push({ name: "list_student_record"});
        }
      }
    )
  }
  
  onBeforeMount(() => load())

  </script>
  