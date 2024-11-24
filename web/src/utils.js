document.addEventListener("DOMContentLoaded", () => {
    const tabs = document.querySelectorAll(".nav-link");
    const content = document.getElementById("tab-content");

    // Función para cargar contenido desde un archivo
    async function loadContent(file) {
        try {
            const response = await fetch(file);
            if (!response.ok) throw new Error(`Error ${response.status}: No se pudo cargar ${file}`);
            const html = await response.text();
            content.innerHTML = html;

            // Disparar un evento personalizado cuando el contenido esté cargado
            const event = new Event("contentLoaded");
            content.dispatchEvent(event);
        } catch (error) {
            content.innerHTML = `<p class="text-danger">${error.message}</p>`;
        }
    }

    // Cargar contenido del primer enlace al cargar la página
    const firstTab = tabs[0];
    firstTab.classList.add("active"); // Asegurarse de que la primera pestaña sea activa
    loadContent(firstTab.getAttribute("data-file"));

    // Agregar eventos a las pestañas
    tabs.forEach(tab => {
        tab.addEventListener("click", (event) => {
            event.preventDefault();

            // Cambiar la pestaña activa
            tabs.forEach(t => t.classList.remove("active"));
            tab.classList.add("active");

            // Cargar contenido del archivo .html
            const file = tab.getAttribute("data-file");
            loadContent(file);
        });
    });

    // Inicializar funciones dinámicas después de que se cargue el contenido
    content.addEventListener("contentLoaded", () => {
        // Lógica específica para la pestaña "Histórico"
        if (content.querySelector("#image-gallery")) {
            cargarImagenes();
        }

        // Inicialización de controladores para otras secciones
        const rangoVentilador1 = document.getElementById('control-ventilador1');
        if (rangoVentilador1) {
            rangoVentilador1.addEventListener('input', function() {
                const valorActual = rangoVentilador1.value;
                handle(this, 'modificarVentilador1', valorActual);
            });
        }

        const rangoVentilador2 = document.getElementById('control-ventilador2');
        if (rangoVentilador2) {
            rangoVentilador2.addEventListener('input', function() {
                const valorActual = rangoVentilador2.value;
                handle(this, 'modificarVentilador2', valorActual);
            });
        }

        const rangoFoco = document.getElementById('control-foco');
        if (rangoFoco) {
            rangoFoco.addEventListener('input', function() {
                const valorActual = rangoFoco.value;
                handle(this, 'modificarFoco', valorActual);
            });
        }

        var objetivo = new XMLHttpRequest();
        objetivo.open("GET", "/get_setpoint", true);
        objetivo.onreadystatechange = function() {
            if (objetivo.readyState === 4 && objetivo.status === 200) {
            var data = JSON.parse(objetivo.responseText);
            // Actualización del valor "estado" del sistema de irrigación
            document.getElementById("temperatura-input").value = data.setpoint;
            }
        };
        objetivo.send();
    });
});

// Función para cargar imágenes en la galería
function cargarImagenes() {
    const gallery = document.getElementById('image-gallery');
    if (!gallery) return;

    // Limpiar la galería antes de cargar nuevas imágenes
    gallery.innerHTML = '';

    fetch('/get_images')
    .then(response => response.json())
    .then(images => {
        const gallery = document.getElementById('image-gallery');
        gallery.innerHTML = ''; // Limpia el contenido previo del contenedor

        images.forEach(image => {
            const imageDiv = document.createElement('div');
            imageDiv.classList.add('image-item');

            // Crear el título con fecha y hora
            const title = document.createElement('p');
            title.textContent = image.readable_time;
            title.classList.add('image-title'); // Clase para aplicar estilo si es necesario

            // Crear el elemento de imagen
            const img = document.createElement('img');
            img.src = image.url;
            img.alt = image.readable_time;

            // Crear el botón de descarga
            const downloadBtn = document.createElement('a');
            downloadBtn.href = image.url;
            downloadBtn.download = image.filename;
            downloadBtn.classList.add('download-btn');
            downloadBtn.textContent = 'Descargar';

            // Agregar el título, la imagen y el botón al contenedor
            imageDiv.appendChild(title);
            imageDiv.appendChild(img);
            imageDiv.appendChild(downloadBtn);

            gallery.appendChild(imageDiv);
        });
    })
    .catch(error => {
        console.error('Error al cargar las imágenes:', error);
    });

}



function prenderSistema(){
    habilitar_deshabilitar_botones(false)
    configurarEntradas()
    handle(this, 'modificarSistema', true)
}

function apagarSistema(){
    apagarIrrigacion()
    handle(this, "modificarVentilador1", 0)
    handle(this, "modificarVentilador2", 0)
    handle(this, "modificarFoco", 0)
    habilitar_deshabilitar_botones(true) // Deshabilitar
    handle(this, 'modificarSistema', false)
}

function prenderIrrigacion(){
    handle(this, 'modificarIrrigacion', true)
}

function apagarIrrigacion(){
    handle(this, 'modificarIrrigacion', false)
}

function configurarEntradas(){
    const rangos = document.querySelectorAll(".range-control");
    rangos.forEach(rango => {
        if(!rango.classList.contains("d-none")){
            const hijo = rango.querySelector("[id]")
            if(hijo.id == "control-ventilador1"){
                handle(this, "modificarVentilador1", document.getElementById("control-ventilador1").value)
            }else if(hijo.id == "control-ventilador2"){
                handle(this, "modificarVentilador2", document.getElementById("control-ventilador2").value)
            }else if(hijo.id == "control-foco"){
                handle(this, "modificarFoco", document.getElementById("control-foco").value)
            }
        }
    })
}

function habilitar_deshabilitar_botones(valor){

    document.getElementById("btn-irrigacion-on").disabled = valor
    document.getElementById("btn-irrigacion-off").disabled = valor

    const botones = document.querySelectorAll(".btn-control")
    botones.forEach(boton => {
        boton.disabled = valor
    })

    document.getElementById("control-ventilador1").disabled = valor
    document.getElementById("control-ventilador2").disabled = valor
    document.getElementById("control-foco").disabled = valor
}

function controlManual(id, boton){
    const div = document.getElementById(id).parentElement;
    if(div.classList.contains("d-none")){
        div.classList.remove("d-none")
        boton.value = "Manual";
        if(id == 'control-ventilador1'){
            handle(this, "modificarControlVentilador1", true)
            handle(this, "modificarVentilador1", document.getElementById("control-ventilador1").value)
        }else if(id == 'control-ventilador2'){
            handle(this, "modificarControlVentilador2", true)
            handle(this, "modificarVentilador2", document.getElementById("control-ventilador2").value)
        }else{
            handle(this, "modificarControlFoco", true)
            handle(this, "modificarFoco", document.getElementById("control-foco").value)
        }
    }else{
        div.classList.add("d-none")
        boton.value = "Automático";
        if(id == 'control-ventilador1')
            handle(this, "modificarControlVentilador1", false)
        else if(id == 'control-ventilador2')
            handle(this, "modificarControlVentilador2", false)
        else
            handle(this, "modificarControlFoco", false)
    }
}

// Ejecución de funciones periódicamente
setInterval(function() {

    // Obtiene el estado del sistema por método GET cada segundo
    var sistema = new XMLHttpRequest();
    sistema.open("GET", "/get_estado", true);
    sistema.onreadystatechange = function() {
        if (sistema.readyState === 4 && sistema.status === 200) {
            var data = JSON.parse(sistema.responseText);
            // Actualización del valor "estado" del sistema de invernadero
            document.getElementById("estado").innerText = "Estado: " + data.estado;
            document.getElementById("estado-sistema").value = data.estado; 
        }
    };
    sistema.send();

    if(document.getElementById("estado-sistema").value != 'Apagado'){
        // Actualización de grafica cada segundo
        var img = document.getElementById("tempImg");
        img.src = "./img/temperatura_grafica.png?" + new Date().getTime();
    
        // Obtiene la temperatura por método GET cada segundo
        var temperatura = new XMLHttpRequest();
        temperatura.open("GET", "/get_temperatura", true);
        temperatura.onreadystatechange = function() {
            if (temperatura.readyState === 4 && temperatura.status === 200) {
            var data = JSON.parse(temperatura.responseText);
            // Actualización del valor "temperatura"
            document.getElementById("temperatura").innerText = "Temperatura: " + data.temperatura + "°C";
            }
        };
        temperatura.send();
    
        // Obtiene la humedad por método GET cada segundo
        var humedad = new XMLHttpRequest();
        humedad.open("GET", "/get_humedad", true);
        humedad.onreadystatechange = function() {
            if (humedad.readyState === 4 && humedad.status === 200) {
            var data = JSON.parse(humedad.responseText);
            // Actualización del valor "humedad"
            document.getElementById("humedad").innerText = "Humedad: " + data.humedad;
            }
        };
        humedad.send();
    
        // Obtiene el estado del sistema de irrigación por método GET cada segundo
        var irrigacion = new XMLHttpRequest();
        irrigacion.open("GET", "/get_estado_irrigacion", true);
        irrigacion.onreadystatechange = function() {
            if (irrigacion.readyState === 4 && irrigacion.status === 200) {
            var data = JSON.parse(irrigacion.responseText);
            // Actualización del valor "estado" del sistema de irrigación
            document.getElementById("estado-irrigacion").innerText = "Estado: " + data.estado;
            }
        };
        irrigacion.send();
    
        var ventilador1 = new XMLHttpRequest();
        ventilador1.open("GET", "/get_ventilador1", true);
        ventilador1.onreadystatechange = function() {
            if (ventilador1.readyState === 4 && ventilador1.status === 200) {
                var data = JSON.parse(ventilador1.responseText);
                // Actualización del valor "estado" del sistema de irrigación
                document.getElementById("ventilador-1").innerText = data.ventilador1 + "%";
            }
        };
        ventilador1.send();
    
        var ventilador2 = new XMLHttpRequest();
        ventilador2.open("GET", "/get_ventilador2", true);
        ventilador2.onreadystatechange = function() {
            if (ventilador2.readyState === 4 && ventilador2.status === 200) {
                var data = JSON.parse(ventilador2.responseText);
                // Actualización del valor "estado" del sistema de irrigación
                document.getElementById("ventilador-2").innerText = data.ventilador2 + "%";
            }
        };
        ventilador2.send();
    
        var foco = new XMLHttpRequest();
        foco.open("GET", "/get_foco", true);
        foco.onreadystatechange = function() {
            if (foco.readyState === 4 && foco.status === 200) {
                var data = JSON.parse(foco.responseText);
                // Actualización del valor "estado" del sistema de irrigación
                document.getElementById("foco").innerText = data.foco + "%";
            }
        };
        foco.send();
    }

}, 500);

// Construye la petición POST
function handle(sender, action, value) {
    submit(action, value);
}

// Envia solicitudes POST
function submit(action, value) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", window.location.href, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        'action': action,
        'value': value,
    }));
}