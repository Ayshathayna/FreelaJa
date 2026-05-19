const carousel = document.getElementById('jobsCarousel');

function scrollLeftJobs(){
  carousel.scrollLeft -= 380; //Ajuste o valor de acordo com a largura do card de vaga
}

function scrollRightJobs(){
  carousel.scrollLeft += 380;
}