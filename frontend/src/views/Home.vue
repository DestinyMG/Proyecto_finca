<template>
    <BaseAdmin>
        <template #default>

            <div class="welcome-banner">
                <h2>BIENVENIDO al Sistema de Gestión de Finca</h2>
                <p>Administra eficientemente todos los aspectos de tu finca desde un solo lugar.</p>
            </div>

            <div class="dashboard-grid">

                <div class="card-item">
                    <div class="card-icon">🐄</div>
                    <div class="card-content">
                        <h3>Registro de Ganado</h3>
                        <p>Gestiona el inventario completo de tu ganado, incluyendo información detallada de cada
                            animal.</p>
                    </div>
                </div>

                <div class="card-item">
                    <div class="card-icon">🍼</div>
                    <div class="card-content">
                        <h3>Control de Nacimientos</h3>
                        <p>Registra y realiza seguimiento a todos los nacimientos en tu finca.</p>
                    </div>
                </div>

                <div class="card-item">
                    <div class="card-icon">💉</div>
                    <div class="card-content">
                        <h3>Programa de Vacunación</h3>
                        <p>Administra el calendario de vacunación y tratamientos veterinarios.</p>
                    </div>
                </div>

                <div class="card-item">
                    <div class="card-icon">🤰</div>
                    <div class="card-content">
                        <h3>Seguimiento de Preñez</h3>
                        <p>Controla el estado reproductivo de tus animales y programa inseminaciones.</p>
                    </div>
                </div>

                <div class="card-item">
                    <div class="card-icon">🥛</div>
                    <div class="card-content">
                        <h3>Producción Lechera</h3>
                        <p>Registra y analiza la producción diaria de leche de tu ganado.</p>
                    </div>
                </div>

                <div class="card-item">
                    <div class="card-icon">📊</div>
                    <div class="card-content">
                        <h3>Reportes y Análisis</h3>
                        <p>Genera reportes detallados sobre el rendimiento y estado de tu finca.</p>
                    </div>
                </div>

            </div>
        </template>
    </BaseAdmin>
</template>

<script setup>
// Asegúrate de que la ruta a tu componente BaseAdmin sea correcta
import BaseAdmin from '../components/BaseAdmin.vue';
</script>

<style scoped>
/* --- 1. Estilos para el Banner de Bienvenida --- */
.welcome-banner {
    background-color: #28a745;
    /* Verde principal de la imagen */
    color: white;
    padding: 1.5rem 2rem;
    border-radius: 8px;
    margin-bottom: 2rem;
    /* Separación entre el banner y las tarjetas */
    box-shadow: 0 4px 10px rgba(40, 167, 69, 0.3);
}

.welcome-banner h2 {
    margin: 0;
    font-size: 1.75rem;
    /* Tamaño de fuente grande para el título */
    font-weight: 600;
}

.welcome-banner p {
    margin: 0.5rem 0 0;
    font-size: 1rem;
    opacity: 0.9;
    /* Texto ligeramente menos prominente */
}

/* --- 2. Estilos para la Rejilla de Opciones --- */
.dashboard-grid {
    display: grid;
    /* CSS Grid Responsivo:
    - En pantallas grandes, crea 3 columnas (1fr 1fr 1fr).
    - En pantallas más pequeñas, se ajustará automáticamente.
    - 'auto-fit' crea tantas columnas como quepan.
    - 'minmax(280px, 1fr)' dice que cada columna debe tener un mínimo
      de 280px y un máximo de 1 fracción (se reparten el espacio).
  */
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
    /* Espacio entre las tarjetas */
}

/* --- 3. Estilos para cada Tarjeta (Card) --- */
.card-item {
    background-color: #ffffff;
    border-radius: 10px;
    padding: 1.5rem;
    /* Sombra sutil como en la imagen */
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
    display: flex;
    align-items: flex-start;
    /* Alinea icono y texto arriba */
    gap: 1rem;
    /* Espacio entre icono y contenido de texto */
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card-item:hover {
    transform: translateY(-5px);
    /* Efecto de "levantar" al pasar el mouse */
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
}

.card-icon {
    flex-shrink: 0;
    /* Evita que el icono se encoja */
    width: 45px;
    height: 45px;
    border-radius: 10px;
    /* Bordes redondeados como en la imagen */
    background-color: #28a745;
    /* Fondo verde para el icono */
    color: white;
    /* Emoji/icono en blanco */
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    /* Tamaño del emoji */
}

.card-content h3 {
    margin: 0;
    font-size: 1.15rem;
    /* Tamaño del título de la tarjeta */
    font-weight: 600;
    color: #333;
    /* Color de texto oscuro */
}

.card-content p {
    margin: 0.5rem 0 0;
    font-size: 0.9rem;
    color: #666;
    /* Color de texto gris para la descripción */
    line-height: 1.5;
}
</style>