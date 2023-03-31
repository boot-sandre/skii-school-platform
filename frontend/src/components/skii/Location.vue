<template>
    <div class="relative w-full h-full mb-3 text-3xl font-medium text-center text-900">Location Information</div>
    <Card style="width: 25em">
    <template #header>
        <img alt="user header" src="/static/default.png" />
    </template>
    <template #title>{{ record.label }}</template>
    <template #subtitle>{{ record.description }}</template>
    <template #content>
        <ul>
            <li>
                {{ record.address1 }}
            </li>
            <li>
                {{ record.address2 }}
            </li>
            <li>
                {{ record.city }}
            </li>
            <li>
                {{ record.country }}
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
import { api } from '@/state';
import Button from 'primevue/button';

const record = shallowRef<LocationContract>({
    label: "",
    address1: "",
    address2: null,
    city: "",
    country: "FR",
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