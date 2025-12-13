const canvas  = document.querySelector('.entradaFormato__entrada--firmaCanvas')
const ctx  = canvas.getContext("2d")

let dibujando = false;


canvas.addEventListener("mousedown",() => dibujando = true);
canvas.addEventListener("mouseup",() =>{
    dibujando = false;
    ctx.beginPath();
})

canvas.addEventListener("mousedown" , () => dibujando = true)
canvas.addEventListener("mouseup" , () => {
    dibujando = false
    ctx.beginPath()
}) 

canvas.addEventListener("mousemove",dibujar)


function dibujar(e){
    if(!dibujando) return;

    ctx.lineWidth = 2;
    ctx.lineCap = "round";
    ctx.strokeStyle = "#000";

    ctx.lineTo(e.offsetX, e.offsetY);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(e.offsetX, e.offsetY);
}

function limpiarFirma() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

function mostrarVentanaModal () {

    menu = document.querySelector('.menuTickets')
    menu.style.display = 'flex';
    
}
//Aca se mostrara el  menu para mostrar la ventana modal para añadir tickets 


function cerrarVentana (){
      
    menu = document.querySelector('.menuTickets')
    menu.style.display = 'none';
         
}


function mostrarFormularioFormato(elemento){

    const cuadricula = document.querySelectorAll('.cuadriculaFormato')
    
    cuadricula.forEach(c => {
        c.style.border = "1px solid var(--color-grisSuave)"
    })

    elemento.style.border = "1px solid var(--color-menu-fondo)"
     
    const nombre = elemento.dataset.name

    fetch(`/tickets/formularios/${nombre}`).then(response => response.text()).then(html =>{
             const  todos = document.querySelectorAll('.formatoContenido')
             todos.forEach(u=>u.style.display = 'none')
             const mostrar = document.querySelector(`.formatoContenido[data-form="${nombre}"]`)
             const formulario = document.querySelector('.formularioBajaEquipo')
             console.log(formulario)
             mostrar.innerHTML = html
             mostrar.style.display = 'block'
    })
    
    

}





