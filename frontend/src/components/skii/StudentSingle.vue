
<template>
    <div class="flex flex-col centered-container">
      <h1 class="text-center">
        Students Space
      </h1>
      <div v-if="student" class="flex flex-col items-center my-8 space-y-5">
            <div class="grid mx-3 formgrid p-fluid">
              <div class="mb-4 ield col-12 md:col-6">
                <label for="username">Username</label>
                <InputText type="text" v-model="student.user.username" id="username"/>
              </div>
              <div class="mb-4 ield col-12 md:col-6">
                <label for="email">Email</label>
                <InputText type="text" v-model="student.user.email" id="email"/>
              </div>
              <div class="mb-4 ield col-12 md:col-6">
                <label for="first_name">Firstname</label>
                <InputText type="text" v-model="student.user.first_name" id="first_name"/>
              </div>
              <div class="mb-4 ield col-12 md:col-6">
                <label for="last_name">Lastname</label>
                <InputText type="text" v-model="student.user.last_name" id="last_name"/>
              </div>
              <button class="px-5 mt-5 border-2 border-gray-400 rounded-md btn txt-light p-button-sm" @click="$router.back()">Cancel</Button>
              <button class="px-5 mt-5 border-2 border-gray-400 rounded-md btn txt-light p-button-sm" @click="saveRecord(Boolean(!props.djangoPk))">Save</Button>
            </div>
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
  
  function saveRecord(creation=false) {
    confirmDanger(
      `Save the ${student.value.user.username} student?`,
      "The student will be permanently modified",
      async () => {
        var url:string = ""
        if (creation) {
          url = `/skii/models/student/create/`;
        } else {
          url = `/skii/models/student/save/${props.djangoPk}`;
        }
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
  