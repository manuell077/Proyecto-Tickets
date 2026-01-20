function seleccionItems(nombre_submodulo,nombre_modulo){ //Esta funcion es para mostrar el contenido  de cada submodulo
    
    document.querySelectorAll('.menuNavegacion__item--submenu').forEach(li => li.classList.remove('menuNavegacion__item--menuSeleccionado')); // Se hace lo mismo que con el menu de los modulos eliminando y añadiendo el estilo 
    const elementoSeleccionado = document.querySelector('.menuNavegacion__item--submenu')
    elementoSeleccionado.classList.add('menuNavegacion__item--menuSeleccionado') 
     
    fetch(`/menu/submodulos/contenido/${nombre_submodulo}/${nombre_modulo}`).then( //Se realiza la peticion a la url donde se le pasa el nombre del submodulo esta url esta asociado a una vista que lo que hace es traer el contenido dinamico de cada submodulo
      r =>  r.text())
      .then(html =>{
         document.querySelector('.contenidoDinamico').innerHTML = html //Se le añade el contenido como texto a html 
      })
    
}

function mostrarSubmodulos(moduleId){ //Esta funcion sirve para mostrar los submodulos obteniedo el moduleId seleccionado por el usuario 
   

  document.querySelectorAll('.menuNavegacion__item').forEach(li => li.classList.remove('menuNavegacion__item--menuSeleccionado'));//Aca elimina todos los estilos que tenian el menu seleccionado
  

  const elementoSeleccionado = document.querySelector('.menuNavegacion__item')
  elementoSeleccionado.classList.add('menuNavegacion__item--menuSeleccionado') //Aca le añade la clase de menuSeleccionado que es el fondo blanco ovalado 


   fetch(`/menu/submodulos/${moduleId}/`) // Aca realiza una solicitud a la url donde trae todos los submodulos de acuedo al modulo que selecciono el usuario 
   .then(r => r.json())
   .then(data => {
     const ul = document.querySelector('.menuNavegacion__Lista--submenu')
     ul.innerHTML  = "" //Aca borra todo el contenido de la lista 
       
    document.querySelector('.menuNavegacion--submenu').style.display = 'block' //Muestra el menu  y le quita el display block 

     data.submodules.forEach(sub => {
         const li = document.createElement("li")
         li.classList.add("menuNavegacion__item")
         li.classList.add("menuNavegacion__item--submenu")
         li.textContent = sub.name; // Se le añade el nombre del submodulo al menu
         li.onclick = () => seleccionItems(sub.name,sub.nombreModulo)  // Se le añade el evento onClick donde se mete la funcion seleccionItems() que se le pasa el parametro seleccionItems
         ul.appendChild(li) // Se añade cada elemento a la lista 
     })

   })
   
}




