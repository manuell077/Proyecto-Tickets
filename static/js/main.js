function seleccionItems(nombre_submodulo){
    
   
    document.querySelectorAll('.menuNavegacion__item--submenu').forEach(li => li.classList.remove('menuNavegacion__item--menuSeleccionado'));

    const elementoSeleccionado = document.querySelector('.menuNavegacion__item--submenu')
    elementoSeleccionado.classList.add('menuNavegacion__item--menuSeleccionado')
     
    fetch(`/menu/submodulos/contenido/${nombre_submodulo}`).then(
      r =>  r.text())
      .then(html =>{
         document.querySelector('.contenidoDinamico').innerHTML = html
      })
    
}

function mostrarSubmodulos(moduleId){
   

  document.querySelectorAll('.menuNavegacion__item').forEach(li => li.classList.remove('menuNavegacion__item--menuSeleccionado'));
  

  const elementoSeleccionado = document.querySelector('.menuNavegacion__item')
  elementoSeleccionado.classList.add('menuNavegacion__item--menuSeleccionado')


   fetch(`/menu/submodulos/${moduleId}/`)
   .then(r => r.json())
   .then(data => {
     const ul = document.querySelector('.menuNavegacion__Lista--submenu')
     ul.innerHTML  = ""
       
    document.querySelector('.menuNavegacion--submenu').style.display = 'block'

     data.submodules.forEach(sub => {
         const li = document.createElement("li")
         li.classList.add("menuNavegacion__item")
         li.classList.add("menuNavegacion__item--submenu")
         li.textContent = sub.name;
         li.onclick = () => seleccionItems(sub.name)
         ul.appendChild(li)
     })

   })
   
}




