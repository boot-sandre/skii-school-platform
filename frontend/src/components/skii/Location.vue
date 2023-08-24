<template>
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
                <div v-if="!state.editMode" class="w-full text-900 md:flex-order-0 flex-order-1">
                    {{ record.address1 }}
                </div>
                <div v-else class="w-full text-900 md:flex-order-0 flex-order-1">
                    <InputText type="text" v-model="record.address1"/>
                </div>
            </li>
            <li>
                <div class="w-6 font-medium text-500 md:w-2">Address 2</div>
                <div v-if="!state.editMode" class="w-full text-900 md:flex-order-0 flex-order-1">{{ record.address2 }}</div>
                <div v-else class="w-full text-900 md:flex-order-0 flex-order-1">
                    <InputText type="text" v-model="record.address2"/>
                </div>
            </li>
            <li>
                <div class="w-6 font-medium text-500 md:w-2">City</div>
                <div v-if="!state.editMode" class="w-full text-900 md:flex-order-0 flex-order-1">{{ record.city }}</div>
                <div v-else class="w-full text-900 md:flex-order-0 flex-order-1">
                    <InputText type="text" v-model="record.city"/>
                </div>
            </li>
            <li>
                <div class="w-6 font-medium text-500 md:w-2">Country</div>
                {{ record.country.name }}
                <div v-if="!state.editMode" class="w-full text-900 md:flex-order-0 flex-order-1">
                    <img :src="serverUrl + record.country.flag"/>
                </div>
                <div v-else class="w-full text-900 md:flex-order-0 flex-order-1">
                    <InputText type="text" v-model="record.country.code"/>
                </div>
            </li>
        </ul>
        <p>
            {{ record.content }}
        </p>
        <Button v-if="!state.editMode" @click="mutateEdit()">Edit</Button>
        <div v-else>
            <Button @click="saveRecord()">Save</Button>
            <Button @click="cancelRecord()">Cancel</Button>
        </div>
    </template>
</Card>
</template>

<script setup lang="ts">
import Card from 'primevue/card';
import { shallowRef, onBeforeMount, reactive, ref } from 'vue';
import { confirmDanger, msg } from '@/notify';
import { LocationContract, LocationSingleResponse, LocationState, LocationSaveContract } from '@/interfaces';
import InputText from 'primevue/inputtext';
import { api, serverUrl, forms} from '@/state';
import Button from 'primevue/button';
import router from '@/router';


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
    },
});
const state = reactive<LocationState>({
    editMode: false
}
    
)
  
async function load() {
    console.log("Component Location loading");
    console.log("djangoPk: " + props.djangoPk);
    console.log("state: " + state);
    fetchRecord()
}

async function mutateEdit() {
    state.editMode = !state.editMode
    console.log("editMode: " + state.editMode);
}

async function cancelRecord() {
    mutateEdit()
    fetchRecord()
}

async function saveRecord(creation=false) {
    confirmDanger(
      `Save the ${record.value.label} location?`,
      "The location will be permanently modified",
      async () => {
        var url:string = ""
        if (creation) {
          url = `/skii/location/create/`;
        } else {
          url = `/skii/location/save/${props.djangoPk}/`;
        }
        const country_code = record.value.country.code
        record.value.country = country_code
        const payload = <LocationSaveContract>(record.value);
        console.log("saveRecord url", url);
        console.log("saveRecord payload", payload);
        const { error, res, errors } = await forms.post(url, payload);
        if (res.ok) {
          // Notify user about deleteRecord success
          msg.success("Location saved", "The location has been successfuly saved");
          // Refresh current component
          record.value = res.data.item;
          mutateEdit()
        }
      }
    )

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