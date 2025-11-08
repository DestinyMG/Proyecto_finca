<template>
    <aside class="sidebar" :class="{ 'is-open': isOpen }">
        <div class="brand">
            <span class="brand-logo">🌱</span>
            <span class="brand-name">Mi Finca</span>
        </div>

        <nav class="navigation">
            <ul>
                <li>
                    <RouterLink to="/ganado">
                        <span class="nav-icon">📝</span><span>Registrar</span>
                    </RouterLink>
                </li>

                <li>
                    <RouterLink to="/enfermedades">
                        <span class="nav-icon">🤒</span><span>Enfermedades</span>
                    </RouterLink>
                </li>

                <li>
                    <RouterLink to="/vacunas">
                        <span class="nav-icon">💉</span><span>Vacunas</span>
                    </RouterLink>
                </li>

                <li>
                    <RouterLink to="/medicamentos">
                        <span class="nav-icon">💊</span><span>Medicamentos</span>
                    </RouterLink>
                </li>

                <li>
                    <RouterLink to="/registrosanitario">
                        <span class="nav-icon">✅</span><span>Sanidad</span>
                    </RouterLink>
                </li>

                <li>
                    <RouterLink to="/gestacion">
                        <span class="nav-icon">❤️</span><span>Gestación</span>
                    </RouterLink>
                </li>

                <li>
                    <RouterLink to="/produccion">
                        <span class="nav-icon">🥛</span><span>Producción</span>
                    </RouterLink>
                </li>

                <li>
                    <RouterLink to="/reportes">
                        <span class="nav-icon">📊</span><span>Reportes</span>
                    </RouterLink>
                </li>
            </ul>
        </nav>
    </aside>
</template>

<script setup>
// Define el prop 'isOpen' que viene de BaseAdmin
defineProps({
    isOpen: {
        type: Boolean,
        default: false
    }
});
</script>

<style scoped>
.sidebar {
    width: 260px;
    background: linear-gradient(180deg, #2d5a3a 0%, #3a6b47 100%);
    color: #f5f5f5;
    height: 100vh;
    position: fixed;
    top: 0;
    left: 0;
    display: flex;
    flex-direction: column;
    transition: transform 0.3s ease-in-out;
    z-index: 100;
    box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
    overflow: hidden;
}

/* Patrón sutil de hojas en el fondo */
.sidebar::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%23244a32' fill-opacity='0.1' fill-rule='evenodd'/%3E%3C/svg%3E");
    opacity: 0.3;
    z-index: -1;
}

.brand {
    display: flex;
    align-items: center;
    padding: 1.5rem 1.25rem;
    font-size: 1.5rem;
    font-weight: bold;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    background-color: rgba(45, 90, 58, 0.8);
}

.brand-logo {
    background-color: #d4a574;
    color: #2d5a3a;
    border-radius: 50%;
    width: 45px;
    height: 45px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 0.75rem;
    font-weight: bold;
    font-size: 1.8rem;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.brand-name {
    font-family: 'Georgia', serif;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
}

.navigation {
    flex: 1;
    padding: 1rem 0;
}

.navigation ul {
    list-style: none;
    padding: 0;
    margin: 0;
}

.navigation li a {
    display: flex;
    align-items: center;
    padding: 1rem 1.5rem;
    color: #e8f5e9;
    text-decoration: none;
    font-size: 1rem;
    transition: all 0.3s ease;
    border-left: 3px solid transparent;
    font-weight: 500;
}

.navigation li a:hover {
    background-color: rgba(212, 165, 116, 0.1);
    color: #ffffff;
    border-left-color: #d4a574;
    padding-left: 1.7rem;
}

.nav-icon {
    margin-right: 12px;
    font-size: 1.2rem;
    width: 24px;
    text-align: center;
}

/* Estilo para el ítem activo - USANDO LA CLASE DE VUE ROUTER */
.navigation li a.router-link-active,
.navigation li a.router-link-exact-active {
    background-color: rgba(212, 165, 116, 0.2);
    color: #ffffff;
    font-weight: 600;
    border-left: 4px solid #d4a574;
    padding-left: calc(1.5rem - 1px);
}

.sidebar-footer {
    padding: 1rem 1.5rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    background-color: rgba(45, 90, 58, 0.8);
}

.weather-info {
    display: flex;
    align-items: center;
    font-size: 0.9rem;
    color: #e8f5e9;
}

.weather-icon {
    margin-right: 8px;
    font-size: 1.2rem;
}

.weather-text {
    font-weight: 500;
}

/* --- Estilos Responsivos --- */
@media (max-width: 768px) {
    .sidebar {
        transform: translateX(-100%);
        width: 280px;
    }

    .sidebar.is-open {
        transform: translateX(0);
    }
}

@media (min-width: 769px) {
    .sidebar {
        transform: translateX(0);
    }
}
</style>