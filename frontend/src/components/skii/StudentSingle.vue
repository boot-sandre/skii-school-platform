
<template>
    <div class="flex flex-col centered-container">
      <h1>
        Students Space
      </h1>
      <div v-if="student" class="flex flex-col items-center my-8 space-y-5">
          <Panel  :toggleable="true">
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
              <button class="w-full btn bord-background success" @click="saveAgent()">Save</button>
            </form-card>
          </Panel>
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
  import { confirmDanger, msg } from '@/notify';
  
  const student = ref<StudentAgentContract>();

  const props = defineProps({
    agent_pk: {
      type: String,
      required: true,
    }
  });
  
  async function load() {
    fetch_agent(Number(props.agent_pk));
  }

  async function fetch_agent(agent_pk: number) {
    const url = `/skii/models/student/${agent_pk}`
    console.log("url: " + url)
    const res = await api.get<StudentSingleResponse>(url);
    console.log("DATA", JSON.stringify(res.data, null, "  "));
    if (res.ok) {
      student.value = res.data.item;
    }
  }
  
  function saveAgent() {
    confirmDanger(
      `Save the ${student.value.id} student?`,
      "The student will be permanently modified",
      async () => {
        const url = `/skii/models/student/save/${student.value.id}`;
        const payload = student.value;
        console.log("save agent url", url);
        const { error, res, errors } = await forms.post(url, payload);
        if (res.ok) {
          router.push("/student")
          msg.success("Student saved", "The student has been successfuly saved");
        }
      }
    )
  }

  function deleteStudent(student: StudentAgentContract) {
    confirmDanger(
      `Delete the ${student.id} student?`,
      "The student will be permanently deleted",
      async () => {
        const url = `/skii/models/student/delete/${student.id}`;
        console.log("DEL", url);
        const res = await api.del(url);
        if (res.ok) {
          msg.success("Student deleted", "The student has been successfuly deleted");
          router.push("/student");
        }
      }
    )
  }
  
  onBeforeMount(() => load())

  </script>
  