
<template>
  <div class="flex flex-col centered-container">
    <page-title class="text-center">
      Students Space
    </page-title>
    <div class="flex flex-col items-center my-8 space-y-5">
      <div v-for="student in students" :key="student.id" class="w-full">
        <Panel  :toggleable="true">
           id : {{student.id}}
           user_id: {{student.user}}
        </Panel>
      </div>
    </div>
    
  </div>
</template>

<script setup lang="ts">
import { onBeforeMount, ref } from 'vue';
import { StudentAgentContract } from "@/interfaces";
import { serverUrl, api } from '@/state';
import Panel from 'primevue/panel';
import { confirmDanger, msg } from '@/notify';

const students = ref<Array<StudentAgentContract>>([]);

async function load() {
  const res = await api.get<Array<StudentAgentContract>>("/skii/models/student/list")
  console.log("DATA", JSON.stringify(res.data, null, "  "))
  if (res.ok) {
    students.value = res.data.items;
  }
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
        load()
        msg.success("Student deleted", "The student has been successfuly deleted")
      }
    }
  )
}


onBeforeMount(() => load())
</script>
