<template>
  <h2 class="text-3xl text-center">
    Teachers Space
  </h2>
  <div class="flex flex-col items-center my-8 space-y-5">
    <DataTable :value="teachers" class="p-datatable p-datatable-table" 
      tableStyle="min-width: 50rem" paginator :rows="5" :rowsPerPageOptions="[5, 10, 20, 50]">
      <template #header>
        <div class="flex-row-reverse flex-wrap ap-2">
          <span class="text-xl font-bold text-900">Teachers list ({{ count }} record(s))</span>
        </div>
        <div class="flex flex-row-reverse flex-wrap ap-2">
          <button type="button" @click="createAgent()" class="px-5 border-2 border-gray-400 rounded-md p-button-sm">Create</Button>
          <button type="button" @click="refresh()" class="px-5 border-2 border-gray-400 rounded-md p-button-sm">Refresh</Button>
        </div>
        
      </template>
      <Column field="user.username" header="Username"></Column>
      <Column field="user.email" header="Email"></Column>
      <Column header="Action" field="id">
        <template #body="{ data }">
          <button type="button"
            @click="editAgent(data)"
            class="px-5 border-2 border-gray-400 rounded-md p-button-sm">Edit</button>
          <button type="button"
            @click="deleteAgent(data)"
            class="px-5 border-2 border-gray-400 rounded-md p-button-sm">Delete</button>
        </template>
      </Column>
    </DataTable>
  </div>
</template>

<script setup lang="ts">
import { onBeforeMount, shallowRef, ref } from 'vue';
import { StudentAgentContract, StudentListResponse } from "@/interfaces";
import { serverUrl, api } from '@/state';
import InputSwitch from 'primevue/inputswitch';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Panel from 'primevue/panel';
import Button from 'primevue/button';
import { confirmDanger, msg } from '@/notify';
import router from '@/router';

var teachers = shallowRef<Array<StudentAgentContract>>([]);
var count = ref<Number>(0)

async function load() {
  console.log("Component TeacherList loading")
  const res = await api.get<StudentListResponse>("/skii/teacher/list/");
  if (res.ok) {
    teachers.value = res.data.items;
    count.value = res.data.count;
  }
}

function createAgent() {
  console.log("Create Teacher push route")
  router.push({
    name: "create_teacher_record"
  })
}

function refresh() {
  load()
}

function editAgent(teacher: StudentAgentContract) {
  console.log("Fetch Teacher")
  router.push({
    name: "fetch_teacher_record",
    params: {
      djangoPk: teacher.id
    }
  })
}

function deleteAgent(teacher: StudentAgentContract) {
  console.log("Delete Teacher")
  confirmDanger(
    `Delete the ${teacher.user.username} teacher?`,
    "The teacher will be permanently deleted",
    async () => {
      const url = `/skii/teacher/delete/${teacher.id}/`;
      const res = await api.del(url);
      if (res.ok) {
        load()
        msg.success("Teacher deleted", "The teacher has been successfuly deleted")
      }
    }
  )
}

onBeforeMount(() => load())
</script>
