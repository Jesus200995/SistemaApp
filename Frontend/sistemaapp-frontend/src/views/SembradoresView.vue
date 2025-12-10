<template>
  <div class="sembradores-container">
    <!-- Fondo decorativo con blobs animados -->
    <div class="background-blobs">
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
      <div class="blob blob-3"></div>
    </div>

    <!-- Header principal con botón de regreso -->
    <header class="header-sembradores">
      <div class="header-wrapper">
        <div class="header-left">
          <router-link to="/dashboard" class="back-button" title="Volver al Dashboard">
            <ArrowLeft class="back-icon" />
          </router-link>
          <div class="header-icon-small">
            <Sprout class="icon-stat" />
          </div>
          <div class="header-text">
            <h1 class="header-title">Sembradores</h1>
            <p class="header-subtitle">Registro y gestión</p>
          </div>
        </div>
        <button @click="recargarSembradores" class="reload-button" title="Recargar">
          <svg class="reload-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8M21 3v5h-5M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16M3 21v-5h5"></path>
          </svg>
        </button>
      </div>
    </header>

    <!-- Contenido principal -->
    <main class="sembradores-main">
      <div class="sembradores-content">
        <!-- Formulario de registro -->
        <section
          v-motion
          :initial="{ opacity: 0, y: 30 }"
          :enter="{ opacity: 1, y: 0, transition: { duration: 600 } }"
          class="form-section"
        >
          <div class="form-header">
            <h2 class="form-title">Registrar Nuevo Sembrador</h2>
            <p class="form-subtitle">Completa los datos del sembrador</p>
          </div>

          <form @submit.prevent="crearSembrador" class="sembrador-form">
            <!-- Fila 1: Nombre y CURP -->
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">Nombre Completo *</label>
                <div class="input-wrapper">
                  <User class="input-icon" />
                  <input
                    v-model="form.nombre"
                    type="text"
                    placeholder="JUAN PÉREZ GARCÍA"
                    class="form-input"
                    required
                    minlength="2"
                    @input="form.nombre = form.nombre.toUpperCase()"
                  />
                </div>
              </div>

              <div class="form-group">
                <label class="form-label">CURP *</label>
                <div class="input-wrapper">
                  <IdCard class="input-icon" />
                  <input
                    v-model="form.curp"
                    type="text"
                    placeholder="Ej: GAPA850101HDFRRL09"
                    class="form-input"
                    maxlength="18"
                    minlength="18"
                    pattern="[A-Z]{4}[0-9]{6}[HM][A-Z]{5}[A-Z0-9]{2}"
                    @input="form.curp = form.curp.toUpperCase().replace(/[^A-Z0-9]/g, '')"
                    required
                  />
                </div>
                <span class="input-hint" v-if="form.curp && form.curp.length > 0 && form.curp.length < 18">
                  {{ form.curp.length }}/18 caracteres
                </span>
              </div>
            </div>

            <!-- Fila 2: Comunidad y Territorio -->
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">Comunidad *</label>
                <div class="input-wrapper">
                  <MapPin class="input-icon" />
                  <input
                    v-model="form.comunidad"
                    type="text"
                    placeholder="La Esperanza"
                    class="form-input"
                    required
                  />
                </div>
              </div>

              <div class="form-group">
                <label class="form-label">Territorio *</label>
                <div class="select-wrapper">
                  <Globe class="input-icon" />
                  <select
                    v-model="form.territorio"
                    class="form-select"
                    required
                  >
                    <option value="">-- Selecciona --</option>
                    <option value="Acapulco - Centro - Norte - Tierra Caliente">Acapulco - Centro - Norte - Tierra Caliente</option>
                    <option value="Acayucan">Acayucan</option>
                    <option value="Balancán">Balancán</option>
                    <option value="Chihuahua / Sonora">Chihuahua / Sonora</option>
                    <option value="Colima">Colima</option>
                    <option value="Comalcalco">Comalcalco</option>
                    <option value="Córdoba">Córdoba</option>
                    <option value="Costa Chica - Montaña">Costa Chica - Montaña</option>
                    <option value="Costa Grande - Sierra">Costa Grande - Sierra</option>
                    <option value="Durango / Zacatecas">Durango / Zacatecas</option>
                    <option value="Hidalgo">Hidalgo</option>
                    <option value="Istmo">Istmo</option>
                    <option value="Michoacán">Michoacán</option>
                    <option value="Mixteca">Mixteca</option>
                    <option value="Morelos">Morelos</option>
                    <option value="Nayarit / Jalisco">Nayarit / Jalisco</option>
                    <option value="Ocosingo">Ocosingo</option>
                    <option value="Palenque">Palenque</option>
                    <option value="Papantla">Papantla</option>
                    <option value="Pichucalco">Pichucalco</option>
                    <option value="Puebla">Puebla</option>
                    <option value="San Luis Potosí">San Luis Potosí</option>
                    <option value="Sinaloa">Sinaloa</option>
                    <option value="Tamaulipas">Tamaulipas</option>
                    <option value="Tantoyuca">Tantoyuca</option>
                    <option value="Tapachula">Tapachula</option>
                    <option value="Teapa">Teapa</option>
                    <option value="Tlaxcala / Estado de México">Tlaxcala / Estado de México</option>
                    <option value="Tzucacab / Opb">Tzucacab / Opb</option>
                    <option value="Xpujil">Xpujil</option>
                    <option value="Oficinas Centrales">Oficinas Centrales</option>
                  </select>
                </div>
              </div>
            </div>

            <!-- Fila 3: Cultivo y Teléfono -->
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">Cultivo Principal *</label>
                <div class="select-wrapper">
                  <Leaf class="input-icon" />
                  <select
                    v-model="form.cultivo_principal"
                    class="form-select"
                    required
                  >
                    <option value="">-- Selecciona cultivo --</option>
                    <!-- Granos básicos -->
                    <option value="Maíz">Maíz</option>
                    <option value="Frijol">Frijol</option>
                    <option value="Trigo">Trigo</option>
                    <option value="Arroz">Arroz</option>
                    <option value="Sorgo">Sorgo</option>
                    <option value="Avena">Avena</option>
                    <option value="Cebada">Cebada</option>
                    <!-- Hortalizas -->
                    <option value="Tomate">Tomate</option>
                    <option value="Chile">Chile</option>
                    <option value="Cebolla">Cebolla</option>
                    <option value="Calabaza">Calabaza</option>
                    <option value="Pepino">Pepino</option>
                    <option value="Zanahoria">Zanahoria</option>
                    <option value="Lechuga">Lechuga</option>
                    <option value="Brócoli">Brócoli</option>
                    <option value="Coliflor">Coliflor</option>
                    <option value="Espinaca">Espinaca</option>
                    <option value="Chayote">Chayote</option>
                    <option value="Ejote">Ejote</option>
                    <option value="Nopal">Nopal</option>
                    <!-- Frutas -->
                    <option value="Aguacate">Aguacate</option>
                    <option value="Limón">Limón</option>
                    <option value="Naranja">Naranja</option>
                    <option value="Mango">Mango</option>
                    <option value="Plátano">Plátano</option>
                    <option value="Papaya">Papaya</option>
                    <option value="Piña">Piña</option>
                    <option value="Sandía">Sandía</option>
                    <option value="Melón">Melón</option>
                    <option value="Fresa">Fresa</option>
                    <option value="Guayaba">Guayaba</option>
                    <option value="Manzana">Manzana</option>
                    <option value="Durazno">Durazno</option>
                    <option value="Uva">Uva</option>
                    <option value="Coco">Coco</option>
                    <option value="Tamarindo">Tamarindo</option>
                    <option value="Ciruela">Ciruela</option>
                    <option value="Zarzamora">Zarzamora</option>
                    <option value="Frambuesa">Frambuesa</option>
                    <option value="Arándano">Arándano</option>
                    <!-- Oleaginosas -->
                    <option value="Soya">Soya</option>
                    <option value="Cacahuate">Cacahuate</option>
                    <option value="Ajonjolí">Ajonjolí</option>
                    <option value="Girasol">Girasol</option>
                    <option value="Cártamo">Cártamo</option>
                    <!-- Cultivos industriales -->
                    <option value="Caña de azúcar">Caña de azúcar</option>
                    <option value="Café">Café</option>
                    <option value="Cacao">Cacao</option>
                    <option value="Algodón">Algodón</option>
                    <option value="Tabaco">Tabaco</option>
                    <option value="Agave">Agave</option>
                    <option value="Henequén">Henequén</option>
                    <option value="Vainilla">Vainilla</option>
                    <!-- Tubérculos -->
                    <option value="Papa">Papa</option>
                    <option value="Camote">Camote</option>
                    <option value="Yuca">Yuca</option>
                    <option value="Jícama">Jícama</option>
                    <!-- Especias y condimentos -->
                    <option value="Cilantro">Cilantro</option>
                    <option value="Perejil">Perejil</option>
                    <option value="Epazote">Epazote</option>
                    <option value="Orégano">Orégano</option>
                    <option value="Hierbabuena">Hierbabuena</option>
                    <!-- Forrajes -->
                    <option value="Alfalfa">Alfalfa</option>
                    <option value="Pasto">Pasto</option>
                    <option value="Maíz forrajero">Maíz forrajero</option>
                    <!-- Otros -->
                    <option value="Amaranto">Amaranto</option>
                    <option value="Chía">Chía</option>
                    <option value="Quinoa">Quinoa</option>
                    <option value="Jamaica">Jamaica</option>
                    <option value="Achiote">Achiote</option>
                    <option value="Palma de aceite">Palma de aceite</option>
                    <option value="Hule">Hule</option>
                    <option value="Flores">Flores</option>
                    <option value="Otro">Otro</option>
                  </select>
                </div>
              </div>

              <div class="form-group">
                <label class="form-label">Teléfono *</label>
                <div class="input-wrapper">
                  <Phone class="input-icon" />
                  <input
                    v-model="form.telefono"
                    type="tel"
                    placeholder="10 dígitos"
                    class="form-input"
                    required
                    maxlength="10"
                    minlength="10"
                    pattern="[0-9]{10}"
                    @input="form.telefono = form.telefono.replace(/[^0-9]/g, '').slice(0, 10)"
                  />
                </div>
                <span class="input-hint" v-if="form.telefono && form.telefono.length > 0 && form.telefono.length < 10">
                  {{ form.telefono.length }}/10 dígitos
                </span>
              </div>
            </div>

            <!-- Botón de envío -->
            <button type="submit" class="submit-btn" :disabled="loading">
              <Sprout class="btn-icon" v-if="!loading" />
              <span class="btn-text">{{ loading ? 'Guardando...' : 'Guardar Sembrador' }}</span>
            </button>
          </form>
        </section>

        <!-- Sección de lista de sembradores -->
        <section
          v-motion
          :initial="{ opacity: 0, y: 30 }"
          :enter="{ opacity: 1, y: 0, transition: { delay: 200, duration: 600 } }"
          class="list-section"
        >
          <div class="list-header">
            <h2 class="list-title">
              <span class="count-badge">{{ sembradores.length }}</span>
              Sembradores Registrados
            </h2>
            <p class="list-subtitle">Gestión de sembradores en tu jurisdicción</p>
          </div>

          <!-- Estado vacío -->
          <div v-if="sembradores.length === 0" class="empty-state">
            <div class="empty-icon">
              <Sprout />
            </div>
            <h3 class="empty-title">Sin sembradores aún</h3>
            <p class="empty-text">Registra el primer sembrador para comenzar</p>
          </div>

          <!-- Tabla de sembradores -->
          <div v-else class="table-wrapper">
            <div class="table-container">
              <table class="sembradores-table">
                <thead>
                  <tr class="table-header-row">
                    <th class="table-header-cell">Nombre</th>
                    <th class="table-header-cell">CURP</th>
                    <th class="table-header-cell">Comunidad</th>
                    <th class="table-header-cell">Territorio</th>
                    <th class="table-header-cell">Cultivo</th>
                    <th class="table-header-cell">Teléfono</th>
                    <th class="table-header-cell">Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="(sembrador, index) in sembradores"
                    :key="sembrador.id"
                    class="table-body-row"
                    :style="{
                      animation: `slideIn 0.3s ease ${index * 0.05}s`
                    }"
                  >
                    <td class="table-cell">
                      <div class="cell-content">
                        <div class="cell-icon">
                          <User class="icon-small" />
                        </div>
                        <span class="cell-text">{{ sembrador.nombre }}</span>
                      </div>
                    </td>
                    <td class="table-cell">
                      <span class="cell-curp">{{ sembrador.curp || 'N/A' }}</span>
                    </td>
                    <td class="table-cell">
                      <div class="cell-location">
                        <MapPin class="icon-tiny" />
                        {{ sembrador.comunidad }}
                      </div>
                    </td>
                    <td class="table-cell">
                      <span class="cell-badge territorio-badge">{{ sembrador.territorio || 'N/A' }}</span>
                    </td>
                    <td class="table-cell">
                      <span class="cell-badge">{{ sembrador.cultivo_principal }}</span>
                    </td>
                    <td class="table-cell">
                      <a :href="`tel:${sembrador.telefono}`" class="cell-phone">
                        {{ sembrador.telefono }}
                      </a>
                    </td>
                    <td class="table-cell">
                      <div class="cell-actions">
                        <button
                          @click="editarSembrador(sembrador)"
                          class="action-btn edit-btn"
                          title="Editar"
                        >
                          <Edit2 class="action-icon" />
                        </button>
                        <button
                          @click="eliminarSembrador(sembrador.id)"
                          class="action-btn delete-btn"
                          title="Eliminar"
                        >
                          <Trash2 class="action-icon" />
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </section>
      </div>
    </main>

    <!-- Modal de Edición -->
    <Teleport to="body">
      <div v-if="showEditModal" class="modal-overlay" @click.self="cerrarModalEdicion">
        <div class="modal-edicion" v-motion
          :initial="{ opacity: 0, scale: 0.9, y: 20 }"
          :enter="{ opacity: 1, scale: 1, y: 0, transition: { duration: 300 } }"
        >
          <div class="modal-header">
            <h2 class="modal-title">Editar Sembrador</h2>
            <button @click="cerrarModalEdicion" class="modal-close-btn" title="Cerrar">
              <X class="modal-close-icon" />
            </button>
          </div>

          <form @submit.prevent="guardarEdicion" class="modal-form">
            <!-- Fila 1: Nombre y CURP -->
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">Nombre Completo *</label>
                <div class="input-wrapper">
                  <User class="input-icon" />
                  <input
                    v-model="form.nombre"
                    type="text"
                    placeholder="JUAN PÉREZ GARCÍA"
                    class="form-input"
                    required
                    minlength="2"
                    @input="form.nombre = form.nombre.toUpperCase()"
                  />
                </div>
              </div>

              <div class="form-group">
                <label class="form-label">CURP *</label>
                <div class="input-wrapper">
                  <IdCard class="input-icon" />
                  <input
                    v-model="form.curp"
                    type="text"
                    placeholder="Ej: GAPA850101HDFRRL09"
                    class="form-input"
                    maxlength="18"
                    minlength="18"
                    pattern="[A-Z]{4}[0-9]{6}[HM][A-Z]{5}[A-Z0-9]{2}"
                    @input="form.curp = form.curp.toUpperCase().replace(/[^A-Z0-9]/g, '')"
                    required
                  />
                </div>
              </div>
            </div>

            <!-- Fila 2: Comunidad y Territorio -->
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">Comunidad *</label>
                <div class="input-wrapper">
                  <MapPin class="input-icon" />
                  <input
                    v-model="form.comunidad"
                    type="text"
                    placeholder="La Esperanza"
                    class="form-input"
                    required
                  />
                </div>
              </div>

              <div class="form-group">
                <label class="form-label">Territorio *</label>
                <div class="select-wrapper">
                  <Globe class="input-icon" />
                  <select
                    v-model="form.territorio"
                    class="form-select"
                    required
                  >
                    <option value="">-- Selecciona --</option>
                    <option value="Acapulco - Centro - Norte - Tierra Caliente">Acapulco - Centro - Norte - Tierra Caliente</option>
                    <option value="Acayucan">Acayucan</option>
                    <option value="Balancán">Balancán</option>
                    <option value="Chihuahua / Sonora">Chihuahua / Sonora</option>
                    <option value="Colima">Colima</option>
                    <option value="Comalcalco">Comalcalco</option>
                    <option value="Córdoba">Córdoba</option>
                    <option value="Costa Chica - Montaña">Costa Chica - Montaña</option>
                    <option value="Costa Grande - Sierra">Costa Grande - Sierra</option>
                    <option value="Durango / Zacatecas">Durango / Zacatecas</option>
                    <option value="Hidalgo">Hidalgo</option>
                    <option value="Istmo">Istmo</option>
                    <option value="Michoacán">Michoacán</option>
                    <option value="Mixteca">Mixteca</option>
                    <option value="Morelos">Morelos</option>
                    <option value="Nayarit / Jalisco">Nayarit / Jalisco</option>
                    <option value="Ocosingo">Ocosingo</option>
                    <option value="Palenque">Palenque</option>
                    <option value="Papantla">Papantla</option>
                    <option value="Pichucalco">Pichucalco</option>
                    <option value="Puebla">Puebla</option>
                    <option value="San Luis Potosí">San Luis Potosí</option>
                    <option value="Sinaloa">Sinaloa</option>
                    <option value="Tamaulipas">Tamaulipas</option>
                    <option value="Tantoyuca">Tantoyuca</option>
                    <option value="Tapachula">Tapachula</option>
                    <option value="Teapa">Teapa</option>
                    <option value="Tlaxcala / Estado de México">Tlaxcala / Estado de México</option>
                    <option value="Tzucacab / Opb">Tzucacab / Opb</option>
                    <option value="Xpujil">Xpujil</option>
                    <option value="Oficinas Centrales">Oficinas Centrales</option>
                  </select>
                </div>
              </div>
            </div>

            <!-- Fila 3: Cultivo y Teléfono -->
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">Cultivo Principal *</label>
                <div class="select-wrapper">
                  <Leaf class="input-icon" />
                  <select
                    v-model="form.cultivo_principal"
                    class="form-select"
                    required
                  >
                    <option value="">-- Selecciona cultivo --</option>
                    <option value="Maíz">Maíz</option>
                    <option value="Frijol">Frijol</option>
                    <option value="Trigo">Trigo</option>
                    <option value="Arroz">Arroz</option>
                    <option value="Sorgo">Sorgo</option>
                    <option value="Avena">Avena</option>
                    <option value="Cebada">Cebada</option>
                    <option value="Tomate">Tomate</option>
                    <option value="Chile">Chile</option>
                    <option value="Cebolla">Cebolla</option>
                    <option value="Calabaza">Calabaza</option>
                    <option value="Pepino">Pepino</option>
                    <option value="Zanahoria">Zanahoria</option>
                    <option value="Lechuga">Lechuga</option>
                    <option value="Brócoli">Brócoli</option>
                    <option value="Coliflor">Coliflor</option>
                    <option value="Espinaca">Espinaca</option>
                    <option value="Chayote">Chayote</option>
                    <option value="Ejote">Ejote</option>
                    <option value="Nopal">Nopal</option>
                    <option value="Aguacate">Aguacate</option>
                    <option value="Limón">Limón</option>
                    <option value="Naranja">Naranja</option>
                    <option value="Mango">Mango</option>
                    <option value="Plátano">Plátano</option>
                    <option value="Papaya">Papaya</option>
                    <option value="Piña">Piña</option>
                    <option value="Sandía">Sandía</option>
                    <option value="Melón">Melón</option>
                    <option value="Fresa">Fresa</option>
                    <option value="Guayaba">Guayaba</option>
                    <option value="Manzana">Manzana</option>
                    <option value="Durazno">Durazno</option>
                    <option value="Uva">Uva</option>
                    <option value="Coco">Coco</option>
                    <option value="Tamarindo">Tamarindo</option>
                    <option value="Ciruela">Ciruela</option>
                    <option value="Zarzamora">Zarzamora</option>
                    <option value="Frambuesa">Frambuesa</option>
                    <option value="Arándano">Arándano</option>
                    <option value="Soya">Soya</option>
                    <option value="Cacahuate">Cacahuate</option>
                    <option value="Ajonjolí">Ajonjolí</option>
                    <option value="Girasol">Girasol</option>
                    <option value="Cártamo">Cártamo</option>
                    <option value="Caña de azúcar">Caña de azúcar</option>
                    <option value="Café">Café</option>
                    <option value="Cacao">Cacao</option>
                    <option value="Algodón">Algodón</option>
                    <option value="Tabaco">Tabaco</option>
                    <option value="Agave">Agave</option>
                    <option value="Henequén">Henequén</option>
                    <option value="Vainilla">Vainilla</option>
                    <option value="Papa">Papa</option>
                    <option value="Camote">Camote</option>
                    <option value="Yuca">Yuca</option>
                    <option value="Jícama">Jícama</option>
                    <option value="Cilantro">Cilantro</option>
                    <option value="Perejil">Perejil</option>
                    <option value="Epazote">Epazote</option>
                    <option value="Orégano">Orégano</option>
                    <option value="Hierbabuena">Hierbabuena</option>
                    <option value="Alfalfa">Alfalfa</option>
                    <option value="Pasto">Pasto</option>
                    <option value="Maíz forrajero">Maíz forrajero</option>
                    <option value="Amaranto">Amaranto</option>
                    <option value="Chía">Chía</option>
                    <option value="Quinoa">Quinoa</option>
                    <option value="Jamaica">Jamaica</option>
                    <option value="Achiote">Achiote</option>
                    <option value="Palma de aceite">Palma de aceite</option>
                    <option value="Hule">Hule</option>
                    <option value="Flores">Flores</option>
                    <option value="Otro">Otro</option>
                  </select>
                </div>
              </div>

              <div class="form-group">
                <label class="form-label">Teléfono *</label>
                <div class="input-wrapper">
                  <Phone class="input-icon" />
                  <input
                    v-model="form.telefono"
                    type="tel"
                    placeholder="10 dígitos"
                    class="form-input"
                    required
                    maxlength="10"
                    minlength="10"
                    pattern="[0-9]{10}"
                    @input="form.telefono = form.telefono.replace(/[^0-9]/g, '').slice(0, 10)"
                  />
                </div>
              </div>
            </div>

            <!-- Botones -->
            <div class="modal-actions">
              <button type="button" @click="cerrarModalEdicion" class="btn-cancelar">
                Cancelar
              </button>
              <button type="submit" class="btn-guardar" :disabled="loading">
                {{ loading ? 'Guardando...' : 'Guardar Cambios' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useAuthStore } from '../stores/auth'
import { getSecureApiUrl } from '../utils/api'
import {
  Sprout,
  User,
  MapPin,
  Leaf,
  Phone,
  Edit2,
  Trash2,
  ArrowLeft,
  IdCard,
  Globe,
  X
} from 'lucide-vue-next'
import Swal from 'sweetalert2'

const auth = useAuthStore()
const sembradores = ref([])
const loading = ref(false)
const showEditModal = ref(false)
const editingId = ref<number | null>(null)

const form = ref({
  nombre: '',
  curp: '',
  comunidad: '',
  territorio: '',
  cultivo_principal: '',
  telefono: ''
})

// Obtener sembradores
const getSembradores = async () => {
  try {
    const apiUrl = getSecureApiUrl()
    const res = await axios.get(`${apiUrl}/sembradores/`, {
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    sembradores.value = res.data.items || res.data
  } catch (err: any) {
    console.error('Error al cargar sembradores:', err)
    Swal.fire('⚠️ Advertencia', 'No se pudieron cargar los sembradores', 'warning')
  }
}

// Crear sembrador
const crearSembrador = async () => {
  try {
    // Validar campos obligatorios
    if (!form.value.nombre || !form.value.comunidad || !form.value.cultivo_principal || !form.value.telefono) {
      Swal.fire('❌ Error', 'Por favor completa todos los campos obligatorios', 'error')
      return
    }

    // Validar territorio obligatorio
    if (!form.value.territorio) {
      Swal.fire('❌ Error', 'Debes seleccionar un territorio', 'error')
      return
    }

    // Validar CURP obligatorio
    if (!form.value.curp || !form.value.curp.trim()) {
      Swal.fire('❌ Error', 'El CURP es obligatorio', 'error')
      return
    }

    const curpValue = form.value.curp.trim().toUpperCase()
    if (curpValue.length !== 18) {
      Swal.fire('❌ Error', `El CURP debe tener exactamente 18 caracteres. Actualmente tiene ${curpValue.length} caracteres.`, 'error')
      return
    }
    const curpRegex = /^[A-Z]{4}[0-9]{6}[HM][A-Z]{5}[A-Z0-9]{2}$/
    if (!curpRegex.test(curpValue)) {
      Swal.fire('❌ Error', 'El CURP no tiene un formato válido.\n\nFormato esperado: AAAA######HAAAAA##\n• 4 letras iniciales\n• 6 dígitos (fecha nacimiento)\n• H o M (sexo)\n• 5 letras (estado + consonantes)\n• 2 caracteres finales', 'error')
      return
    }

    loading.value = true
    const apiUrl = getSecureApiUrl()

    await axios.post(`${apiUrl}/sembradores/`, form.value, {
      headers: { Authorization: `Bearer ${auth.token}` }
    })

    Swal.fire('✅ Éxito', 'Sembrador registrado correctamente', 'success')
    
    // Limpiar formulario
    form.value = {
      nombre: '',
      curp: '',
      comunidad: '',
      territorio: '',
      cultivo_principal: '',
      telefono: ''
    }

    // Recargar lista
    await getSembradores()
  } catch (err: any) {
    const errorMsg = err.response?.data?.detail || 'No se pudo registrar el sembrador'
    Swal.fire('❌ Error', errorMsg, 'error')
  } finally {
    loading.value = false
  }
}

// Editar sembrador - abrir modal
const editarSembrador = (sembrador: any) => {
  editingId.value = sembrador.id
  form.value = {
    nombre: sembrador.nombre || '',
    curp: sembrador.curp || '',
    comunidad: sembrador.comunidad || '',
    territorio: sembrador.territorio || '',
    cultivo_principal: sembrador.cultivo_principal || '',
    telefono: sembrador.telefono || ''
  }
  showEditModal.value = true
}

// Guardar cambios de edición
const guardarEdicion = async () => {
  try {
    // Validar campos obligatorios
    if (!form.value.nombre || !form.value.comunidad || !form.value.cultivo_principal || !form.value.telefono) {
      Swal.fire('❌ Error', 'Por favor completa todos los campos obligatorios', 'error')
      return
    }

    // Validar territorio obligatorio
    if (!form.value.territorio) {
      Swal.fire('❌ Error', 'Debes seleccionar un territorio', 'error')
      return
    }

    // Validar CURP obligatorio
    if (!form.value.curp || !form.value.curp.trim()) {
      Swal.fire('❌ Error', 'El CURP es obligatorio', 'error')
      return
    }

    const curpValue = form.value.curp.trim().toUpperCase()
    if (curpValue.length !== 18) {
      Swal.fire('❌ Error', `El CURP debe tener exactamente 18 caracteres. Actualmente tiene ${curpValue.length} caracteres.`, 'error')
      return
    }
    const curpRegex = /^[A-Z]{4}[0-9]{6}[HM][A-Z]{5}[A-Z0-9]{2}$/
    if (!curpRegex.test(curpValue)) {
      Swal.fire('❌ Error', 'El CURP no tiene un formato válido.\n\nFormato esperado: AAAA######HAAAAA##', 'error')
      return
    }

    loading.value = true
    const apiUrl = getSecureApiUrl()

    await axios.put(`${apiUrl}/sembradores/${editingId.value}`, form.value, {
      headers: { Authorization: `Bearer ${auth.token}` }
    })

    Swal.fire('✅ Éxito', 'Sembrador actualizado correctamente', 'success')
    cerrarModalEdicion()
    await getSembradores()
  } catch (err: any) {
    const errorMsg = err.response?.data?.detail || 'No se pudo actualizar el sembrador'
    Swal.fire('❌ Error', errorMsg, 'error')
  } finally {
    loading.value = false
  }
}

// Cerrar modal de edición
const cerrarModalEdicion = () => {
  showEditModal.value = false
  editingId.value = null
  form.value = {
    nombre: '',
    curp: '',
    comunidad: '',
    territorio: '',
    cultivo_principal: '',
    telefono: ''
  }
}

// Eliminar sembrador
const eliminarSembrador = async (id: number) => {
  const result = await Swal.fire({
    title: '⚠️ Confirmar eliminación',
    text: '¿Estás seguro de que deseas eliminar este sembrador?',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#ef4444',
    cancelButtonColor: '#6b7280',
    confirmButtonText: 'Sí, eliminar',
    cancelButtonText: 'Cancelar'
  })

  if (result.isConfirmed) {
    try {
      const apiUrl = getSecureApiUrl()
      await axios.delete(`${apiUrl}/sembradores/${id}`, {
        headers: { Authorization: `Bearer ${auth.token}` }
      })

      Swal.fire('✅ Eliminado', 'Sembrador eliminado correctamente', 'success')
      await getSembradores()
    } catch (err: any) {
      Swal.fire('❌ Error', 'No se pudo eliminar el sembrador', 'error')
    }
  }
}

const recargarSembradores = async () => {
  try {
    await getSembradores()
    await Swal.fire('✅ Recargado', 'Los sembradores se han actualizado', 'success')
  } catch (err) {
    await Swal.fire('❌ Error', 'No se pudo recargar los sembradores', 'error')
  }
}

onMounted(getSembradores)
// Cargar sembradores al montar
onMounted(getSembradores)
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* ========== CONTAINER ========== */
.sembradores-container {
  min-height: 100vh;
  width: 100%;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
  position: relative;
  overflow-x: hidden;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

/* ========== BACKGROUND BLOBS ========== */
.background-blobs {
  position: fixed;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
  z-index: 0;
}

.blob {
  position: absolute;
  opacity: 0.08;
  filter: blur(120px);
  mix-blend-mode: screen;
  border-radius: 50%;
}

.blob-1 {
  width: 600px;
  height: 600px;
  background: linear-gradient(135deg, #10b981, #06b6d4);
  top: -300px;
  left: -300px;
  animation: float 8s ease-in-out infinite;
}

.blob-2 {
  width: 500px;
  height: 500px;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  top: 50%;
  right: -250px;
  animation: float 10s ease-in-out infinite reverse;
}

.blob-3 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #ec4899, #f59e0b);
  bottom: -200px;
  left: 50%;
  animation: float 12s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(30px, -50px); }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ========== HEADER ========== */
.header-sembradores {
  position: relative;
  z-index: 10;
  background: rgba(132, 204, 22, 0.12);
  border-bottom: 1px solid rgba(132, 204, 22, 0.1);
  backdrop-filter: blur(12px);
  padding: 1rem 1.2rem;
  box-shadow: 0 4px 20px rgba(132, 204, 22, 0.1);
  width: 100%;
}

.header-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
}

/* ========== BACK BUTTON ========== */
.back-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(132, 204, 22, 0.1);
  border: 1.5px solid rgba(132, 204, 22, 0.4);
  cursor: pointer;
  text-decoration: none;
  transition: all 0.3s ease;
  color: #84cc16;
  backdrop-filter: blur(10px);
  flex-shrink: 0;
}

.back-button:hover {
  background: rgba(132, 204, 22, 0.2);
  transform: translateX(-4px);
  box-shadow: 0 4px 15px rgba(132, 204, 22, 0.3);
  border-color: rgba(132, 204, 22, 0.6);
}

.back-icon {
  width: 20px;
  height: 20px;
  stroke-width: 2.5;
}

.header-icon-small {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 6px;
  background: transparent;
  flex-shrink: 0;
}

.icon-stat {
  width: 20px;
  height: 20px;
  color: #84cc16;
  stroke-width: 2;
}

.header-text {
  display: flex;
  flex-direction: column;
}

.header-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: #84cc16;
  margin: 0;
  text-shadow: 0 0 8px rgba(132, 204, 22, 0.4);
}

.header-subtitle {
  font-size: 0.75rem;
  color: #cbd5e1;
  margin: 0;
  margin-top: 0.2rem;
}

/* ========== RELOAD BUTTON ========== */
.reload-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(59, 130, 246, 0.1);
  border: 1.5px solid rgba(59, 130, 246, 0.4);
  cursor: pointer;
  transition: all 0.3s ease;
  color: #3b82f6;
  backdrop-filter: blur(10px);
  flex-shrink: 0;
  padding: 0;
}

.reload-button:hover {
  background: rgba(59, 130, 246, 0.2);
  box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
  border-color: rgba(59, 130, 246, 0.6);
}

.reload-button:active {
  transform: scale(0.95);
}

.reload-icon {
  width: 22px;
  height: 22px;
  stroke-width: 2.5;
}

/* ========== MAIN CONTENT ========== */
.sembradores-main {
  position: relative;
  z-index: 5;
  min-height: calc(100vh - 100px);
  padding: 1.25rem;
}

.sembradores-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

/* ========== FORM SECTION ========== */
.form-section {
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.8) 100%);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 16px;
  padding: 1.25rem;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.form-header {
  margin-bottom: 1rem;
}

.form-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: #84cc16;
  margin-bottom: 0.2rem;
  text-shadow: 0 0 8px rgba(132, 204, 22, 0.3);
}

.form-subtitle {
  font-size: 0.7rem;
  color: #cbd5e1;
}

.sembrador-form {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 0.85rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.form-label {
  font-size: 0.65rem;
  font-weight: 600;
  color: #e2e8f0;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.optional-label {
  font-weight: 400;
  color: #64748b;
  text-transform: lowercase;
  font-size: 0.6rem;
}

.input-hint {
  font-size: 0.6rem;
  color: #f59e0b;
  margin-top: 0.2rem;
  font-weight: 500;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 10px;
  width: 14px;
  height: 14px;
  color: #10b981;
  pointer-events: none;
}

.form-input {
  width: 100%;
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 8px;
  padding: 0.5rem 0.75rem 0.5rem 2rem;
  color: #e2e8f0;
  font-size: 0.8rem;
  transition: all 0.3s ease;
}

.form-input::placeholder {
  color: #64748b;
  font-size: 0.75rem;
}

.form-input:focus {
  outline: none;
  border-color: #10b981;
  background: rgba(15, 23, 42, 0.7);
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.1);
}

/* ========== SELECT WRAPPER ========== */
.select-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.select-wrapper .input-icon {
  position: absolute;
  left: 0.6rem;
  width: 14px;
  height: 14px;
  color: #10b981;
  pointer-events: none;
  z-index: 1;
}

.form-select {
  width: 100%;
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 8px;
  padding: 0.5rem 2rem 0.5rem 2rem;
  color: #e2e8f0;
  font-size: 0.8rem;
  transition: all 0.3s ease;
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%2394a3b8'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'%3E%3C/path%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.6rem center;
  background-size: 1rem;
}

.form-select:focus {
  outline: none;
  border-color: #10b981;
  background-color: rgba(15, 23, 42, 0.7);
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.1);
}

.form-select option {
  background: #1e293b;
  color: #e2e8f0;
}

/* ========== SUBMIT BUTTON ========== */
.submit-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 0.6rem 1rem;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
  margin-top: 0.5rem;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
}

.submit-btn:active:not(:disabled) {
  transform: translateY(0);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-icon {
  width: 14px;
  height: 14px;
}

.btn-text {
  font-weight: 600;
}

/* ========== LIST SECTION ========== */
.list-section {
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.8) 100%);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 16px;
  padding: 1.25rem;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.list-header {
  margin-bottom: 1rem;
}

.list-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: #f1f5f9;
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin-bottom: 0.3rem;
}

.count-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border-radius: 6px;
  font-weight: 700;
  font-size: 0.75rem;
}

.list-subtitle {
  font-size: 0.75rem;
  color: #cbd5e1;
}

/* ========== EMPTY STATE ========== */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 1.5rem 1rem;
  text-align: center;
}

.empty-icon {
  width: 50px;
  height: 50px;
  background: rgba(16, 185, 129, 0.15);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.6rem;
  color: #10b981;
}

.empty-icon svg {
  width: 24px;
  height: 24px;
}

.empty-title {
  font-size: 0.9rem;
  font-weight: 600;
  color: #f1f5f9;
  margin-bottom: 0.3rem;
}

.empty-text {
  font-size: 0.75rem;
  color: #cbd5e1;
}

/* ========== TABLE ========== */
.table-wrapper {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

.table-container {
  min-width: 100%;
}

.sembradores-table {
  width: 100%;
  border-collapse: collapse;
}

.table-header-row {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%);
  border-bottom: 2px solid rgba(16, 185, 129, 0.2);
}

.table-header-cell {
  padding: 1rem;
  text-align: left;
  font-size: 0.875rem;
  font-weight: 600;
  color: #cbd5e1;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.table-body-row {
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
  transition: all 0.3s ease;
}

.table-body-row:hover {
  background: rgba(16, 185, 129, 0.05);
}

.table-cell {
  padding: 1rem;
  color: #e2e8f0;
  font-size: 0.9rem;
}

.cell-content {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.cell-icon {
  width: 32px;
  height: 32px;
  background: rgba(16, 185, 129, 0.1);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.icon-small {
  width: 16px;
  height: 16px;
  color: #10b981;
}

.cell-text {
  font-weight: 500;
}

.cell-location {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #cbd5e1;
}

.icon-tiny {
  width: 14px;
  height: 14px;
  color: #10b981;
  flex-shrink: 0;
}

.cell-badge {
  display: inline-block;
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(16, 185, 129, 0.1) 100%);
  color: #a7f3d0;
  padding: 0.375rem 0.75rem;
  border-radius: 6px;
  font-weight: 500;
  font-size: 0.875rem;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.territorio-badge {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(99, 102, 241, 0.1) 100%);
  color: #c4b5fd;
  border: 1px solid rgba(99, 102, 241, 0.3);
}

.cell-curp {
  font-family: 'Courier New', monospace;
  font-size: 0.75rem;
  color: #94a3b8;
  letter-spacing: 0.5px;
}

.cell-phone {
  color: #3b82f6;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
}

.cell-phone:hover {
  color: #60a5fa;
}

.cell-location-small {
  font-size: 0.85rem;
  color: #94a3b8;
  font-family: 'Courier New', monospace;
}

.cell-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.action-btn {
  width: 36px;
  height: 36px;
  border: 1px solid rgba(148, 163, 184, 0.2);
  background: rgba(15, 23, 42, 0.5);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.edit-btn:hover {
  background: rgba(59, 130, 246, 0.1);
  border-color: rgba(59, 130, 246, 0.3);
}

.delete-btn:hover {
  background: rgba(239, 68, 68, 0.1);
  border-color: rgba(239, 68, 68, 0.3);
}

.action-icon {
  width: 18px;
  height: 18px;
}

.edit-btn .action-icon {
  color: #3b82f6;
}

.delete-btn .action-icon {
  color: #ef4444;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
  .header-sembradores {
    padding: 0.8rem 1rem;
  }

  .header-icon-small {
    width: 28px;
    height: 28px;
  }

  .icon-stat {
    width: 18px;
    height: 18px;
  }

  .header-title {
    font-size: 0.85rem;
  }

  .header-subtitle {
    font-size: 0.7rem;
  }

  .reload-button {
    width: 36px;
    height: 36px;
  }

  .reload-icon {
    width: 20px;
    height: 20px;
  }

  .sembradores-main {
    padding: 1rem;
  }

  .form-title {
    font-size: 1.1rem;
  }

  .form-label {
    font-size: 0.7rem;
  }

  .list-title {
    font-size: 1rem;
  }

  .table-header-cell,
  .table-cell {
    padding: 0.6rem 0.5rem;
    font-size: 0.75rem;
  }

  .table-header-cell {
    font-size: 0.7rem;
  }

  .form-input {
    font-size: 16px;
  }
}

@media (max-width: 640px) {
  .header-sembradores {
    padding: 0.75rem 0.9rem;
  }

  .header-icon-small {
    width: 28px;
    height: 28px;
  }

  .icon-stat {
    width: 18px;
    height: 18px;
  }

  .header-title {
    font-size: 0.8rem;
  }

  .header-subtitle {
    font-size: 0.7rem;
  }

  .reload-button {
    width: 36px;
    height: 36px;
  }

  .reload-icon {
    width: 20px;
    height: 20px;
  }

  .form-title {
    font-size: 1.05rem;
  }

  .form-label {
    font-size: 0.65rem;
  }

  .table-header-cell,
  .table-cell {
    padding: 0.5rem 0.4rem;
    font-size: 0.7rem;
  }
}

@media (max-width: 480px) {
  .header-sembradores {
    padding: 0.7rem 0.8rem;
  }

  .header-icon-small {
    width: 26px;
    height: 26px;
  }

  .icon-stat {
    width: 16px;
    height: 16px;
  }

  .header-title {
    font-size: 0.75rem;
  }

  .header-subtitle {
    font-size: 0.65rem;
  }

  .back-button {
    width: 34px;
    height: 34px;
  }

  .back-icon {
    width: 16px;
    height: 16px;
  }

  .reload-button {
    width: 34px;
    height: 34px;
  }

  .reload-icon {
    width: 18px;
    height: 18px;
  }

  .header-title {
    font-size: 0.75rem;
  }

  .header-subtitle {
    font-size: 0.65rem;
  }

  .form-section,
  .list-section {
    padding: 1rem;
    border-radius: 12px;
  }

  .form-title,
  .list-title {
    font-size: 1rem;
  }

  .form-label {
    font-size: 0.6rem;
  }

  .table-header-cell,
  .table-cell {
    padding: 0.4rem 0.3rem;
    font-size: 0.65rem;
  }

  .submit-btn {
    padding: 0.75rem 1rem;
    font-size: 0.9rem;
  }
}

/* ========== MODAL DE EDICIÓN ========== */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
  padding: 1rem;
  overflow-y: auto;
}

.modal-edicion {
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
  border: 1px solid rgba(132, 204, 22, 0.2);
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(12px);
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  animation: modalSlideIn 0.3s ease;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: translateY(20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem;
  border-bottom: 1px solid rgba(132, 204, 22, 0.1);
  background: rgba(132, 204, 22, 0.05);
  border-radius: 16px 16px 0 0;
}

.modal-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #84cc16;
  text-shadow: 0 0 8px rgba(132, 204, 22, 0.3);
  margin: 0;
}

.modal-close-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  cursor: pointer;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.modal-close-btn:hover {
  background: rgba(239, 68, 68, 0.2);
  border-color: rgba(239, 68, 68, 0.5);
}

.modal-close-icon {
  width: 20px;
  height: 20px;
  color: #ef4444;
}

.modal-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1.5rem;
}

.modal-actions {
  display: flex;
  gap: 0.75rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(132, 204, 22, 0.1);
}

.btn-cancelar {
  flex: 1;
  padding: 0.75rem 1rem;
  background: rgba(107, 114, 128, 0.1);
  border: 1px solid rgba(107, 114, 128, 0.3);
  border-radius: 8px;
  color: #d1d5db;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.btn-cancelar:hover {
  background: rgba(107, 114, 128, 0.2);
  border-color: rgba(107, 114, 128, 0.5);
}

.btn-guardar {
  flex: 1;
  padding: 0.75rem 1rem;
  background: linear-gradient(135deg, #84cc16, #65a30d);
  border: 1px solid rgba(132, 204, 22, 0.5);
  border-radius: 8px;
  color: #0f172a;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  box-shadow: 0 4px 12px rgba(132, 204, 22, 0.2);
}

.btn-guardar:hover:not(:disabled) {
  background: linear-gradient(135deg, #a3e635, #84cc16);
  box-shadow: 0 6px 16px rgba(132, 204, 22, 0.3);
  transform: translateY(-2px);
}

.btn-guardar:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* ========== BOTONES CIRCULARES ========== */
.action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 1px solid rgba(148, 163, 184, 0.3);
  background: rgba(15, 23, 42, 0.5);
  cursor: pointer;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.action-btn:hover {
  transform: scale(1.1);
}

.edit-btn:hover {
  background: rgba(16, 185, 129, 0.15);
  border-color: rgba(16, 185, 129, 0.5);
}

.delete-btn:hover {
  background: rgba(239, 68, 68, 0.15);
  border-color: rgba(239, 68, 68, 0.5);
}

.action-icon {
  width: 18px;
  height: 18px;
}

.edit-btn:hover .action-icon {
  color: #10b981;
}

.delete-btn:hover .action-icon {
  color: #ef4444;
}

/* ========== RESPONSIVE MODAL ========== */
@media (max-height: 700px) {
  .modal-edicion {
    max-height: 95vh;
    border-radius: 12px;
  }

  .modal-header {
    padding: 1rem;
  }

  .modal-form {
    padding: 1rem;
    gap: 0.8rem;
  }

  .form-group {
    gap: 0.2rem;
  }

  .form-label {
    font-size: 0.65rem;
  }

  .form-input,
  .form-select {
    padding: 0.4rem 0.6rem 0.4rem 1.8rem;
    font-size: 14px;
  }
}

@media (max-width: 768px) {
  .modal-overlay {
    padding: 0.5rem;
  }

  .modal-edicion {
    width: 100%;
    max-height: 95vh;
    max-width: 95vw;
  }

  .modal-header {
    padding: 1rem;
  }

  .modal-form {
    padding: 1rem;
  }

  .form-row {
    grid-template-columns: 1fr;
    gap: 0.7rem;
  }

  .modal-actions {
    flex-direction: column;
    gap: 0.5rem;
  }

  .btn-cancelar,
  .btn-guardar {
    padding: 0.65rem 0.9rem;
    font-size: 0.85rem;
  }
}

@media (max-width: 480px) {
  .modal-edicion {
    border-radius: 12px;
  }

  .modal-header {
    padding: 0.9rem;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .modal-title {
    font-size: 1.1rem;
    flex: 1;
  }

  .modal-close-btn {
    width: 36px;
    height: 36px;
  }

  .modal-close-icon {
    width: 18px;
    height: 18px;
  }

  .modal-form {
    padding: 0.9rem;
    gap: 0.65rem;
  }

  .form-label {
    font-size: 0.6rem;
  }

  .form-input,
  .form-select {
    padding: 0.35rem 0.5rem 0.35rem 1.6rem;
    font-size: 14px;
  }

  .form-row {
    gap: 0.6rem;
  }

  .action-btn {
    width: 36px;
    height: 36px;
  }

  .action-icon {
    width: 16px;
    height: 16px;
  }

  .btn-cancelar,
  .btn-guardar {
    padding: 0.6rem 0.8rem;
    font-size: 0.8rem;
  }

  .modal-actions {
    gap: 0.4rem;
  }
}

/* ========== ORIENTACIÓN HORIZONTAL (LANDSCAPE) ========== */
@media (max-height: 600px) and (orientation: landscape) {
  .modal-edicion {
    max-height: 90vh;
  }

  .modal-header {
    padding: 0.8rem;
  }

  .modal-form {
    padding: 0.8rem;
    gap: 0.6rem;
  }

  .form-row {
    gap: 0.6rem;
  }

  .form-label {
    font-size: 0.6rem;
  }

  .form-input,
  .form-select {
    padding: 0.3rem 0.5rem 0.3rem 1.5rem;
    font-size: 13px;
  }

  .form-group {
    gap: 0.1rem;
  }

  .modal-actions {
    gap: 0.4rem;
  }

  .btn-cancelar,
  .btn-guardar {
    padding: 0.5rem 0.7rem;
    font-size: 0.75rem;
  }

  .modal-title {
    font-size: 1rem;
  }

  .action-btn {
    width: 32px;
    height: 32px;
  }

  .action-icon {
    width: 14px;
    height: 14px;
  }
}

/* ========== TABLET LANDSCAPE ========== */
@media (min-width: 768px) and (max-width: 1024px) and (orientation: landscape) {
  .modal-edicion {
    max-width: 700px;
    max-height: 85vh;
  }

  .form-row {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* ========== SCROLLBAR MODAL ========== */
.modal-edicion::-webkit-scrollbar {
  width: 6px;
}

.modal-edicion::-webkit-scrollbar-track {
  background: transparent;
}

.modal-edicion::-webkit-scrollbar-thumb {
  background: rgba(132, 204, 22, 0.3);
  border-radius: 3px;
}

.modal-edicion::-webkit-scrollbar-thumb:hover {
  background: rgba(132, 204, 22, 0.5);
}

/* ========== SCROLLBAR ========== */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: rgba(148, 163, 184, 0.3);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(148, 163, 184, 0.5);
}
</style>

