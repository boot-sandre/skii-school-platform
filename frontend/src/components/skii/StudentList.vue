
<template>
    <div class="flex flex-col centered-container">
      <page-title class="text-center">
        Students Space
      </page-title>
      <div class="flex flex-col items-center my-8 space-y-5">
          <Panel  :toggleable="true">
            <DataTable :value="students" tableStyle="min-width: 50rem" paginator :rows="5" :rowsPerPageOptions="[5, 10, 20, 50]">
              <Column field="user.username" header="Username"></Column>
              <Column field="user.email" header="Email"></Column>
              <Column header="Action" field="id">
                <template #body="slotProps">
                  <button type="button"
                    @click="$router.push(`/student/${slotProps.data.id}`)">Edit</button>
                  <button type="button"
                    @click="deleteStudent(slotProps.data)">Delete</button>
                </template>
              </Column>
            </DataTable>
          </Panel>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { onBeforeMount, ref } from 'vue';
  import { StudentAgentContract, StudentListResponse } from "@/interfaces";
  import { serverUrl, api } from '@/state';
  import DataTable from 'primevue/datatable';
  import Column from 'primevue/column';
  import Panel from 'primevue/panel';
  import { confirmDanger, msg } from '@/notify';
  
  const students = ref<Array<StudentAgentContract>>([]);
  
  async function load() {
    const res = await api.get<StudentListResponse>("/skii/models/student/list");
    console.log("DATA", JSON.stringify(res.data, null, "  "));
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
  