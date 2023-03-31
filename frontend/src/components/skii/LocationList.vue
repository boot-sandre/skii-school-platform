
<template>
    <div class="centered-container">
      <h2 class="text-3xl text-center">
        Locations Space
      </h2>
      <div class="flex flex-col items-center my-8 space-y-5">
          <Panel header="Locations board" :toggleable="true">
            <DataTable :value="locations" class="p-datatable p-datatable-table" 
              tableStyle="min-width: 50rem" paginator :rows="5" :rowsPerPageOptions="[5, 10, 20, 50]">
              <template #header>
                <div class="flex-row-reverse flex-wrap ap-2">
                  <span class="text-xl font-bold text-900">Locations list ({{ count }} record(s))</span>
                </div>
                <div class="flex flex-row-reverse flex-wrap ap-2">
                  <button type="button" @click="createLocation()" class="px-5 border-2 border-gray-400 rounded-md p-button-sm">Create</Button>
                  <button type="button" @click="refresh()" class="px-5 border-2 border-gray-400 rounded-md p-button-sm">Refresh</Button>
                </div>
                
              </template>
              <Column field="label" header="Label"></Column>
              <Column field="address1" header="Address1"></Column>
              <Column field="address2" header="Address2"></Column>
              <Column field="city" header="City"></Column>
              <Column field="country" header="Country"></Column>

              <Column header="Action" field="id">
                <template #body="{ data }">
                  <button type="button"
                    @click="editLocation(data)"
                    class="px-5 border-2 border-gray-400 rounded-md p-button-sm">Edit</button>
                  <button type="button"
                    @click="deleteLocation(data)"
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
  import { LocationSingleResponse, LocationContract, LocationListResponse } from "@/interfaces";
  import { serverUrl, api } from '@/state';
  import InputSwitch from 'primevue/inputswitch';
  import DataTable from 'primevue/datatable';
  import Column from 'primevue/column';
  import Panel from 'primevue/panel';
  import Button from 'primevue/button';
  import { confirmDanger, msg } from '@/notify';
  import router from '@/router';
  
  const locations = ref<Array<LocationContract>>([]);
  var count = ref<Number>(0)
  
  async function load() {
    console.log("load component LocationList")
    const res = await api.get<LocationListResponse>("/skii/location/list/");
    if (res.ok) {
      locations.value = res.data.items;
      count.value = res.data.count;
    }
  }
  
  function createLocation() {
    console.log("go to create LocationLocation view")
    router.push({
      name: "create_location_record"
    })
  }

  function refresh() {
    locations.value = []
    load()
  }

  function editLocation(location: LocationContract) {
    console.log("Edit a location", location.uuid);
    router.push({
      name: "fetch_location_record",
      params: {
        djangoPk: location.uuid
      }
    })
  }

  function deleteLocation(location: LocationContract) {
    console.log("Delete a location", location.uuid);
    confirmDanger(
      `Delete the ${location.label} location?`,
      "The location will be permanently deleted",
      async () => {
        const url = `/skii/location/delete/${location.uuid}/`;
        const res = await api.del(url);
        if (res.ok) {
          load()
          msg.success("Location deleted", "The location has been successfuly deleted")
        }
      }
    )
  }

  onBeforeMount(() => load())
  </script>
  