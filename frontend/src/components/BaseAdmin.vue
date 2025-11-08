<template>
    <div class="admin-layout">
        <Sidebar :is-open="isMobileSidebarOpen" />

        <div v-if="isMobileSidebarOpen" class="sidebar-overlay" @click="toggleMobileSidebar"></div>

        <div class="main-content">
            <Header @toggle-sidebar="toggleMobileSidebar" />

            <main class="content-area">
                <slot />
            </main>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import Header from './Header.vue';
import Sidebar from './Sidebar.vue';

// Ref para controlar la visibilidad del sidebar en móviles
const isMobileSidebarOpen = ref(false);

// Función para cambiar el estado
const toggleMobileSidebar = () => {
    isMobileSidebarOpen.value = !isMobileSidebarOpen.value;
};
</script>

<style scoped>
.admin-layout {
    display: flex;
    min-height: 100vh;
}

.main-content {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    width: 100%;
    /* Toma el 100% del espacio restante */
    background-color: #f4f7f6;
    /* Color de fondo del contenido */
}

.content-area {
    flex-grow: 1;
    padding: 1.5rem;
}

.sidebar-overlay {
    display: none;
    /* Oculto por defecto */
}

/* --- Estilos Responsivos --- */
@media (max-width: 768px) {

    /* En móvil, el contenido principal ocupa toda la pantalla */
    .main-content {
        margin-left: 0;
        width: 100%;
    }

    /* El overlay se muestra cuando el sidebar está abierto en móvil */
    .sidebar-overlay {
        display: block;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        z-index: 99;
    }
}

@media (min-width: 769px) {

    /* En desktop, el contenido principal tiene un margen izquierdo del ancho del sidebar */
    .main-content {
        margin-left: 250px;
        /* Asegúrate que coincida con el ancho del Sidebar */
        width: calc(100% - 250px);
    }
}
</style>