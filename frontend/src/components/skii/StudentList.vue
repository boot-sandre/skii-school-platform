
<template>
    <div class="centered-container">
      <h2 class="text-3xl text-center">
        Students Space
      </h2>
      <div class="flex flex-col items-center my-8 space-y-5">
          <Panel header="Students board" :toggleable="true">
            <DataTable :value="students" class="p-datatable p-datatable-table" 
              tableStyle="min-width: 50rem" paginator :rows="5" :rowsPerPageOptions="[5, 10, 20, 50]">
              <template #header>
                <div class="flex-row-reverse flex-wrap ap-2">
                  <span class="text-xl font-bold text-900">Students list ({{ count }} record(s))</span>
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
                    @click="editStudent(data)"
                    class="px-5 border-2 border-gray-400 rounded-md p-button-sm">Edit</button>
                  <button type="button"
                    @click="deleteStudent(data)"
                    class="px-5 border-2 border-gray-400 rounded-md p-button-sm">Delete</button>
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
  import InputSwitch from 'primevue/inputswitch';
  import DataTable from 'primevue/datatable';
  import Column from 'primevue/column';
  import Panel from 'primevue/panel';
  import Button from 'primevue/button';
  import { confirmDanger, msg } from '@/notify';
  import router from '@/router';
  
  const students = ref<Array<StudentAgentContract>>([]);
  var count = ref<Number>(0)
  
  async function load() {
    console.log("load component StudentList")
    const res = await api.get<StudentListResponse>("/skii/student/list/");
    if (res.ok) {
      students.value = res.data.items;
      count.value = res.data.count;
    }
  }
  
  function createAgent() {
    console.log("go to create StudentAgent view")
    router.push({
      name: "create_student_record"
    })
  }

  function refresh() {
    students.value = []
    load()
  }

  function editStudent(student: StudentAgentContract) {
    console.log("Edit a student", student);
    router.push({
      name: "fetch_student_record",
      params: {
        djangoPk: student.id
      }
    })
  }

  function deleteStudent(student: StudentAgentContract) {
    console.log("Delete a student", student);
    confirmDanger(
      `Delete the ${student.user.username} student?`,
      "The student will be permanently deleted",
      async () => {
        const url = `/skii/student/delete/${student.id}/`;
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
  