<template>
    <div class="h-full mb-3 text-3xl font-medium text-center  text-900">Location Information</div>
    <Card style="width: 25em">
    <template #header>
        <img v-if="record.cover" :alt="record.cover.title" :src="serverUrl + record.cover.picture_url" />
    </template>
    <template #title>{{ record.label }}</template>
    <template #subtitle>{{ record.description }}</template>
    <template #content>
        <ul class="p-0 m-0 list-none">
            <li class="flex flex-wrap px-2 py-3 align-items-center border-top-1 surface-border">
                <div class="w-6 font-medium text-500 md:w-2">Address</div>
                <div class="w-full text-900 md:flex-order-0 flex-order-1">{{ record.address1 }}</div>
            </li>
            <li>
                <div class="w-6 font-medium text-500 md:w-2">Address 2</div>
                <div class="w-full text-900 md:flex-order-0 flex-order-1">{{ record.address2 }}</div>
            </li>
            <li>
                <div class="w-6 font-medium text-500 md:w-2">City</div>
                <div class="w-full text-900 md:flex-order-0 flex-order-1">{{ record.city }}</div>
            </li>
            <li>
                <div class="w-6 font-medium text-500 md:w-2">Country</div>
                {{ record.country.name }}
                <div class="w-full text-900 md:flex-order-0 flex-order-1">
                    <img :src="serverUrl + record.country.flag"/>
                </div>
            </li>
        </ul>
        <p>
            {{ record.content }}
        </p>
    </template>
</Card>
</template>

<script setup lang="ts">
import Card from 'primevue/card';
import { shallowRef, onBeforeMount } from 'vue';
import { LocationContract, LocationSingleResponse } from '@/interfaces';
import { api, serverUrl } from '@/state';
import Button from 'primevue/button';

const record = shallowRef<LocationContract>({
    label: "",
    address1: "",
    address2: null,
    city: "",
    country: {
        "code": "FR",
        "name": "France",
        "flag": ""
    },
    content: null,
    description: null,
})

const props = defineProps({
    djangoPk: {
        type: String,
        required: true,
    }
});
  
async function load() {
    console.log("Component Location loading");
    console.log("djangoPk: " + props.djangoPk);
    fetchRecord()
}

async function fetchRecord() {
    if ( props.djangoPk ) {
        const res = await api.get<LocationSingleResponse>(
        `/skii/location/fetch/${props.djangoPk}/`);
        if (res.ok) {
        record.value = res.data.item;
        }
    }
}

onBeforeMount(() => load())
</script>