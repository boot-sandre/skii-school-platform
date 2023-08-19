<template>
    <div class="container card z-2">
        

    <div class="relative w-full h-full mb-3 text-3xl font-medium text-center text-900">User Information</div>
    <ul class="p-0 m-0 list-none">
        <li class="flex flex-wrap px-2 py-3 align-items-center border-top-1 surface-border">
            <div class="w-6 font-medium text-500 md:w-2">Title</div>
            <div class="w-full text-900 md:w-8 md:flex-order-0 flex-order-1">Heat</div>
            <div class="flex w-6 md:w-2 justify-content-end">
                <Button label="Edit" icon="pi pi-pencil" class="p-button-text"></Button>
            </div>
        </li>
        <li class="flex flex-wrap px-2 py-3 align-items-center border-top-1 surface-border">
            <div class="w-6 font-medium text-500 md:w-2">Genre</div>
            <div class="w-full text-900 md:w-8 md:flex-order-0 flex-order-1">
                <Chip label="Crime" class="mr-2"></Chip>
                <Chip label="Drama" class="mr-2"></Chip>
                <Chip label="Thriller"></Chip>
            </div>
            <div class="flex w-6 md:w-2 justify-content-end">
                <Button label="Edit" icon="pi pi-pencil" class="p-button-text"></Button>
            </div>
        </li>
        <li class="flex flex-wrap px-2 py-3 align-items-center border-top-1 surface-border">
            <div class="w-6 font-medium text-500 md:w-2">Director</div>
            <div class="w-full text-900 md:w-8 md:flex-order-0 flex-order-1">Michael Mann</div>
            <div class="flex w-6 md:w-2 justify-content-end">
                <Button label="Edit" icon="pi pi-pencil" class="p-button-text"></Button>
            </div>
        </li>
        <li class="flex flex-wrap px-2 py-3 align-items-center border-top-1 surface-border">
            <div class="w-6 font-medium text-500 md:w-2">Actors</div>
            <div class="w-full text-900 md:w-8 md:flex-order-0 flex-order-1">Robert De Niro, Al Pacino</div>
            <div class="flex w-6 md:w-2 justify-content-end">
                <Button label="Edit" icon="pi pi-pencil" class="p-button-text"></Button>
            </div>
        </li>
        <li class="flex flex-wrap px-2 py-3 align-items-center border-top-1 border-bottom-1 surface-border">
            <div class="w-6 font-medium text-500 md:w-2">Plot</div>
            <div class="w-full text-900 md:w-8 md:flex-order-0 flex-order-1 line-height-3">
                A group of professional bank robbers start to feel the heat from police
                when they unknowingly leave a clue at their latest heist.</div>
            <div class="flex w-6 md:w-2 justify-content-end">
                <Button label="Edit" icon="pi pi-pencil" class="p-button-text"></Button>
            </div>
        </li>
    </ul>
</div>
</template>

<script setup lang="ts">
import { onBeforeMount, ref } from 'vue';

</script>