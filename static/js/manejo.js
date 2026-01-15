function mostrarVentanaModal () { //Esta funcion es para mostrar la ventana donde va aparecer todos los formatos 

    menu = document.querySelector('.menuTickets') //Selecciona  el div que tiene almacenado el menu de los formatos
    menu.style.display = 'flex';//Y lo pone como display flex 
    
}
//Aca se mostrara el  menu para mostrar la ventana modal para añadir tickets 


function cerrarVentana (){ //Esta es la funcion de la [x]
//  que cuando le de clic se cierre la ventana 
      
    menu = document.querySelector('.menuTickets') //Se vuelve a seleccioanr el .menuTickets
    menu.style.display = 'none'; //Y se oculta con el display none 
    

}

const firmas = {};

function mostrarFormularioFormato(elemento){ //Cuando se de click sobre un elemento se activara esta funcion 2

        

    const cuadricula = document.querySelectorAll('.cuadriculaFormato') // Se selecciona el la cuadricula que es donde estan todos los formatos 
    
    cuadricula.forEach(c => {
        c.style.border = "1px solid var(--color-grisSuave)"
    }) //Todos los cuadros en los cuales estan los formatos les vamos a poner fondo gris

    elemento.style.border = "1px solid var(--color-menu-fondo)" //El elemento seleccionado se le pone el borde azul 
     
    const nombre = elemento.dataset.name //El data set [nombre] del boton seleccionado se guarda en la variable nombre
    
    let signaturePad; //El signaturePad

    fetch(`/tickets/formularios/${nombre}`).then(response => response.text()).then(html =>{//Se hace fetch a la url donde devuelve el contenido del html
             const  todos = document.querySelectorAll('.formatoContenido') //Selecciona todos los divs que tienen los formualrios de los  formatos
             todos.forEach(u=>u.style.display = 'none') //De todos se les pone el display none
             const mostrar = document.querySelector(`.formatoContenido[data-form="${nombre}"]`)//Se selecciona el div que tiene el formulario del div que se selecciono 
             mostrar.innerHTML = html //Se inserta el contenido que retorna el fetch
             mostrar.style.display = 'block' // Se pone display block
             mostrar.querySelectorAll('.entradaFormato__entrada--firmaCanvas').forEach(canvas =>{
                 
                 const idFirma = canvas.dataset.firma;
                 signaturePad = new SignaturePad(canvas);
                 ajustarCanvas(canvas, signaturePad); //Esta funcion es para ajustar el mouse con el trazo sin esto cuando el usuario pasa el mouse el trazo aparece muy a la derecha y no sobre el mouse
                 firmas[idFirma] = signaturePad
                 
                }) //Seleccionamos todo los canvas y con la libreria signaturePad que nos permitre firmar dentro de un canvas lo guardamos en la lista firmas 
            
             const inputArchivo = mostrar.querySelector('.valorDeArchivo')
             const label = mostrar.querySelector('.nombreDeArchivo')
             mostrar.querySelectorAll('.btn-primary--firma').forEach(btn =>{
                btn.addEventListener('click',() =>{
                    const idFirma = btn.dataset.firma;
                    const signaturePad = firmas[idFirma];
                     
                    const firmaAsignada = mostrar.querySelector(`.entradaFormato__entrada--firmaCanvas[data-firma=${idFirma}]`)

                    if(signaturePad){
                        
                        firmaAsignada.classList.remove('firmaCanvas--disabled')
                        
                        if(inputArchivo){
                        inputArchivo.value = ""
                        label.textContent = "Ningun Archivo Seleccionado"
                        }
                        signaturePad.clear();
                    }
                })//Aca hacemos la parte de eliminar firma donde se consulta a cual firma es la que queremos limpiar con clear()
             }) 
              
             
            if(mostrar.querySelector('.btn-primary--agregarSeccion') && mostrar.querySelector('.btn-primary--eliminarSeccion')){
                
             mostrar.querySelector('.btn-primary--agregarSeccion').addEventListener('click',function(e){
                     e.preventDefault()
                     
                     const contenedor = mostrar.querySelector('.miniSeccion')
                     const seccion = mostrar.querySelectorAll(".entradaFormato--flex")
                     const  nuevaSeccion = seccion[0].cloneNode(true)
                     const numero = seccion.length + 1;

                     
                     
                     if(nuevaSeccion.querySelector('.numeroPlan')){
                       nuevaSeccion.querySelector('.numeroPlan').value = numero
                     }
                     
                     contenedor.appendChild(nuevaSeccion)
             })

             mostrar.querySelector('.btn-primary--eliminarSeccion').addEventListener('click',function(e){
                   e.preventDefault()
                  
                   const seccion = mostrar.querySelectorAll(".entradaFormato--flex")
                   const cantidad = seccion.length
                   
                   if (cantidad > 1){
                   seccion[cantidad - 1].remove()
                   }
                   
             })
            }
             
              if(inputArchivo){
               inputArchivo.addEventListener("change",() =>{
                const fileName =  inputArchivo.files[0].name
                label.textContent = fileName
                const identificador = inputArchivo.dataset.firma
                const canvas = mostrar.querySelector(`.entradaFormato__entrada--firmaCanvas[data-firma="${identificador}"]`)
                canvas.classList.add('firmaCanvas--disabled')
                firmas[identificador].clear()

               })
            }

             const form = mostrar.querySelector(`.formularioFormato[data-form="${nombre}"]`)//Seleccionamos el formulario de contenido adecuado  

             form.addEventListener('submit', async function(event){ //Boton para enviar formulario 

             event.preventDefault() //Evitamos que realize alguna accion como cambair la url 
            
            const canvases = mostrar.querySelectorAll('.entradaFormato__entrada--firmaCanvas')
            for (const canvas of canvases) { //Seleccionamos todos los canvas para las firmas 
            
            const idFirma = canvas.dataset.firma 
            const signaturePad = firmas[idFirma];
            let firmaBase64 = "" 
             
            const inputArchivo = mostrar.querySelector(`.valorDeArchivo[data-firma="${idFirma}"]`)
            
            //Validamos en cada firma si esta vacia 
            if(inputArchivo && inputArchivo.files.length > 0){
                
                const file = inputArchivo.files[0]
                firmaBase64 = await archivoABase64(file);
                
            }else if(!signaturePad.isEmpty()){
                
                firmaBase64 = canvas.toDataURL('image/png') //Se convierte a base 64 la firma 
                
            }else{
                
                firmaBase64 = ""
            }
            const inputFirma = mostrar.querySelector(
                `.firmaValor[data-datosFirma="${idFirma}"]` 
            )//Se guarda en el input la firma 

            if (!inputFirma) {
                console.warn('No se encontró input para', idFirma)
                return
            }//Si no tiene ningun input asociado entonces mostrara ese mensaje de error en la consola 


            inputFirma.value = firmaBase64 //Se le asigna el valor del input , la firma 

          }

               const formData = new FormData(form)//Convertimos el formulario en un formData que es que  permite enviar imagenes , archivos y en este caso firmas  

               const response = await fetch(
                form.action,
                {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": document.querySelector(
                            '[name=csrfmiddlewaretoken]'
                        ).value
                    },
                    body: formData
                } //Aca hacemos un fetch de tipo post 
            )
            if (response.ok) { //Esto es mas que todo para validar  si se envio correctamente el formulario
                console.log("Formulario enviado correctamente")
            } else {
                console.error("Error al enviar formulario" , response.status , response.statusText)
            }
          })

             });
             
}


function ajustarCanvas(canvas, signaturePad) {
    const ratio = Math.max(window.devicePixelRatio || 1, 1);//Se obtiene el tamño de pixeles de la pantalla 
    const rect = canvas.getBoundingClientRect(); //Tamaño real del canvas con el css aplicado
    
    //Ajustar el tamaño interno del canvas que no es css son el sistema de cordenadas interno  
    canvas.width = rect.width * ratio;
    canvas.height = rect.height * ratio;
   
    canvas.getContext("2d").scale(ratio, ratio);//El contexto del 2d es para que el usuario pueda escribir en el canvas.Adapta el dibujo a esos pixeles con el scale  en el eje (x,y)
    signaturePad.clear(); //Evita firmas deformadas 
}


function archivoABase64(file) { //Este archivo recibe el archivo que se pasa por argumento de la funcion
    return new Promise((resolve, reject) => { //Retorna una promesa una promesa se puede resolver o se puede rechazar
        const reader = new FileReader(); //FileReader sirve para leer archivos del usuario el sirve de manera asincrona  

        reader.onload = () => resolve(reader.result); //Si no hay errores se ejecuta la funcion onload que es cuando el archivo termina de leerse y se resulve la promesa 
        reader.onerror = reject; //Si sucede un error se ejecuta el reject que es que se rechazo la promesa y entra en el acth si es que hay 

        reader.readAsDataURL(file); //Se convierte a base 64
    });
}

function EditarRegistro(btn){
   
   ticketId =  Number(btn.dataset.ticketId)
   formato = btn.dataset.formatoNombre
    
   window.location.href = `/tickets/formularios/${formato}/${ticketId}`
   
}

function BorrarRegistro(){

}

function VerRegistro(){

}
