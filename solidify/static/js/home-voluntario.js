const inscritos = document.getElementById("inscritosInput")

if(inscritos.checked) {
    const eventos_regiao = document.getElementsByClassName("eventos-regiao");
    console.log(eventos_regiao)
    eventos_regiao[0].style.display = "none";

    const eventos_inscritos = document.getElementsByClassName("participando");
    eventos_inscritos[0].style.display = '';
}

inscritos.addEventListener("change", (e) => {
    if(inscritos.checked) {
        const eventos_regiao = document.getElementsByClassName("eventos-regiao");
        console.log(eventos_regiao)
        eventos_regiao[0].style.display = "none";

        const eventos_inscritos = document.getElementsByClassName("participando");
        eventos_inscritos[0].style.display = '';
    }
})

const prox_evento = document.getElementById("proxEventosInput")
prox_evento.addEventListener("change", (e) => {
    if(prox_evento.checked){
        const eventos_regiao = document.getElementsByClassName("eventos-regiao");

        eventos_regiao[0].style.display = '';

        participando = document.getElementsByClassName("participando");
        participando[0].style.display = "none";
    }
})