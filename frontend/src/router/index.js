import { createRouter, createWebHistory } from 'vue-router'

import Prueba from '../components/Prueba.vue'
import BaseAdmin from '../components/BaseAdmin.vue'
import Home from '../views/Home.vue'
import Ganado from '../views/Ganado.vue'
import Enfermedades from '../views/Enfermedades.vue'
import Vacunas from '../views/Vacunas.vue'
import Medicamentos from '../views/Medicamentos.vue'
import RegistroSanitario from '../views/RegistroSanitario.vue'
import Produccion from '../views/Produccion.vue'
import Reportes from '../views/Reportes.vue'
import Gestacion from '../views/Gestacion.vue'
import DetalleAnimal from '../views/DetalleAnimal.vue'
const routes = [

    { path: '/prueba', name: 'prueba', component: Prueba },
    { path: '/admin', name: 'admin', component: BaseAdmin },
    { path: '/home', name: 'home', component: Home },
    { path: '/ganado', name: 'ganado', component: Ganado },
    { path: '/enfermedades', name: 'enfermedades', component: Enfermedades },
    { path: '/vacunas', name: 'vacunas', component: Vacunas },
    { path: '/medicamentos', name: 'medicamentos', component: Medicamentos },
    { path: '/registrosanitario', name: 'registrosanitario', component: RegistroSanitario },
    { path: '/produccion', name: 'produccion', component: Produccion },
    { path: '/reportes', name: 'reportes', component: Reportes },
    { path: '/gestacion', name: 'gestacion', component: Gestacion },
    { path: '/detalle-animal/:id', name: 'detalle-animal', component: DetalleAnimal, props: true },
]

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
})

export default router
