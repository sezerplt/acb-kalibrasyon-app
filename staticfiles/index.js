
function tabs(event,name){
    let i,x
    const link = document.getElementsByClassName("data")
    for (i=0;i<x.link.length;i++){
        x[i].style.display="none";
    }
    const tablinks =document.getElementsByClassName("tablink");
    for (i=0;i<x.link.length;i++){
        tablinks[i].className = tablinks[i].className.replace(" w3-red", ""); 
    }
    document.getElementById(name).style.display = "block";
     event.currentTarget.className += " w3-red"
}