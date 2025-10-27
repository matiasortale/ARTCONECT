import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="ATR Conect", layout="wide")

# Título principal
st.title("🎭 ATR Conect")
st.subheader("Conectando restaurantes y artistas independientes de Buenos Aires")

# Inicializar DataFrames en session_state
if 'artistas_df' not in st.session_state:
    st.session_state.artistas_df = pd.DataFrame(columns=[
        'nombre', 'profesion', 'estilo', 'precio', 'zona', 'contacto', 'redes', 'calificacion', 'reseñas'
    ])

if 'restaurantes_df' not in st.session_state:
    st.session_state.restaurantes_df = pd.DataFrame(columns=[
        'nombre', 'zona', 'direccion', 'contacto', 'redes', 'calificacion', 'reseñas'
    ])

# Sidebar para navegación
menu = st.sidebar.selectbox("Menú Principal", [
    "Inicio", "Registrar Artista", "Registrar Restaurante",
    "Buscar Artistas", "Buscar Restaurantes", "Estadísticas"
])

# Página de Inicio
if menu == "Inicio":
    st.header("Bienvenido a ATR Conect")
    st.write("""
    **Conectamos artistas independientes con restaurantes y bares de Buenos Aires**

    - 🎵 Artistas: Registra tu perfil, muestra tu talento y encuentra lugares para presentarte
    - 🍽️ Restaurantes: Encuentra artistas perfectos para tu establecimiento
    - ⭐ Califica y deja reseñas para construir una comunidad confiable
    """)

    # Mostrar estadísticas rápidas
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Artistas Registrados", len(st.session_state.artistas_df))
    with col2:
        st.metric("Restaurantes Registrados", len(st.session_state.restaurantes_df))

# Registrar Artista
elif menu == "Registrar Artista":
    st.header("🎨 Registrar Nuevo Artista")

    with st.form("form_artista"):
        nombre = st.text_input("Nombre Artístico")
        profesion = st.selectbox("Profesión", ["Cantante", "Músico", "Stand Up", "Actor", "DJ", "Otro"])
        estilo = st.text_input("Estilo de Show")
        precio = st.number_input("Precio aproximado ($)", min_value=0)
        zona = st.selectbox("Zona",
                            ["Palermo", "Recoleta", "Belgrano", "San Telmo", "Microcentro", "Almagro", "Caballito",
                             "Otro"])
        contacto = st.text_input("Email o Teléfono")
        redes = st.text_input("Redes Sociales (@usuario)")

        submitted = st.form_submit_button("Registrar Artista")

        if submitted and nombre:
            nuevo_artista = {
                'nombre': nombre, 'profesion': profesion, 'estilo': estilo,
                'precio': precio, 'zona': zona, 'contacto': contacto,
                'redes': redes, 'calificacion': 0, 'reseñas': ''
            }
            st.session_state.artistas_df = pd.concat([
                st.session_state.artistas_df,
                pd.DataFrame([nuevo_artista])
            ], ignore_index=True)
            st.success(f"✅ {nombre} registrado exitosamente!")

# Registrar Restaurante
elif menu == "Registrar Restaurante":
    st.header("🍽️ Registrar Nuevo Restaurante")

    with st.form("form_restaurante"):
        nombre = st.text_input("Nombre del Restaurante/Bar")
        zona = st.selectbox("Zona",
                            ["Palermo", "Recoleta", "Belgrano", "San Telmo", "Microcentro", "Almagro", "Caballito",
                             "Otro"])
        direccion = st.text_input("Dirección")
        contacto = st.text_input("Email o Teléfono")
        redes = st.text_input("Redes Sociales")

        submitted = st.form_submit_button("Registrar Restaurante")

        if submitted and nombre:
            nuevo_restaurante = {
                'nombre': nombre, 'zona': zona, 'direccion': direccion,
                'contacto': contacto, 'redes': redes, 'calificacion': 0, 'reseñas': ''
            }
            st.session_state.restaurantes_df = pd.concat([
                st.session_state.restaurantes_df,
                pd.DataFrame([nuevo_restaurante])
            ], ignore_index=True)
            st.success(f"✅ {nombre} registrado exitosamente!")

# Buscar Artistas
elif menu == "Buscar Artistas":
    st.header("🔍 Buscar Artistas")

    col1, col2 = st.columns(2)
    with col1:
        profesion_filtro = st.selectbox("Filtrar por profesión",
                                        ["Todos"] + list(st.session_state.artistas_df['profesion'].unique()))
    with col2:
        zona_filtro = st.selectbox("Filtrar por zona", ["Todas"] + list(st.session_state.artistas_df['zona'].unique()))

    # Aplicar filtros
    artistas_filtrados = st.session_state.artistas_df.copy()
    if profesion_filtro != "Todos":
        artistas_filtrados = artistas_filtrados[artistas_filtrados['profesion'] == profesion_filtro]
    if zona_filtro != "Todas":
        artistas_filtrados = artistas_filtrados[artistas_filtrados['zona'] == zona_filtro]

    # Mostrar resultados
    if not artistas_filtrados.empty:
        for _, artista in artistas_filtrados.iterrows():
            with st.expander(f"🎭 {artista['nombre']} - {artista['profesion']}"):
                st.write(f"**Estilo:** {artista['estilo']}")
                st.write(f"**Precio:** ${artista['precio']}")
                st.write(f"**Zona:** {artista['zona']}")
                st.write(f"**Contacto:** {artista['contacto']}")
                st.write(f"**Redes:** {artista['redes']}")

                # Sistema de calificación simple
                calificacion = st.slider(f"Calificar a {artista['nombre']}", 1, 5, 3, key=f"calif_{artista['nombre']}")
                if st.button(f"Enviar calificación", key=f"btn_{artista['nombre']}"):
                    st.info(f"⭐ Calificación {calificacion}/5 enviada para {artista['nombre']}")
    else:
        st.warning("No se encontraron artistas con los filtros seleccionados")

# Buscar Restaurantes
elif menu == "Buscar Restaurantes":
    st.header("🔍 Buscar Restaurantes")

    zona_filtro = st.selectbox("Filtrar por zona", ["Todas"] + list(st.session_state.restaurantes_df['zona'].unique()))

    # Aplicar filtro
    restaurantes_filtrados = st.session_state.restaurantes_df
    if zona_filtro != "Todas":
        restaurantes_filtrados = restaurantes_filtrados[restaurantes_filtrados['zona'] == zona_filtro]

    # Mostrar resultados
    if not restaurantes_filtrados.empty:
        for _, restaurante in restaurantes_filtrados.iterrows():
            with st.expander(f"🍽️ {restaurante['nombre']}"):
                st.write(f"**Zona:** {restaurante['zona']}")
                st.write(f"**Dirección:** {restaurante['direccion']}")
                st.write(f"**Contacto:** {restaurante['contacto']}")
                st.write(f"**Redes:** {restaurante['redes']}")
    else:
        st.warning("No se encontraron restaurantes con los filtros seleccionados")

# Estadísticas
elif menu == "Estadísticas":
    st.header("📊 Estadísticas de ATR Conect")

    if not st.session_state.artistas_df.empty:
        # Gráfico de artistas por profesión
        fig_profesion = px.pie(
            st.session_state.artistas_df,
            names='profesion',
            title='Distribución de Artistas por Profesión'
        )
        st.plotly_chart(fig_profesion)

        # Gráfico de precios promedio por profesión
        if len(st.session_state.artistas_df) > 1:
            precio_promedio = st.session_state.artistas_df.groupby('profesion')['precio'].mean().reset_index()
            fig_precio = px.bar(
                precio_promedio,
                x='profesion',
                y='precio',
                title='Precio Promedio por Profesión',
                labels={'precio': 'Precio ($)', 'profesion': 'Profesión'}
            )
            st.plotly_chart(fig_precio)

    if not st.session_state.restaurantes_df.empty:
        # Gráfico de restaurantes por zona
        fig_zona = px.pie(
            st.session_state.restaurantes_df,
            names='zona',
            title='Distribución de Restaurantes por Zona'
        )
        st.plotly_chart(fig_zona)

# Información adicional en el sidebar
st.sidebar.markdown("---")
st.sidebar.info("""
**ATR Conect** v1.0
Conectando la comunidad artística con la gastronómica 🎭🍽️
""")