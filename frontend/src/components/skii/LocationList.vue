
<template>
    <div class="centered-container">
      <h2 class="text-3xl text-center">
        Locations Space
      </h2>
      <div class="flex flex-col items-center my-8 space-y-5">
            <div class="flex my-8 space-y-5 flex-rowitems-center" v-for="location in locations">
              <location :djangoPk="location.uuid"></location>
            </div>
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
  import Location from '@/components/skii/Location.vue'
  
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
  