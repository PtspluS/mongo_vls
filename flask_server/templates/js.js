function searchstationSelect(){
    if(document.getElementsByName("stations")[0].value != '...'){
        fetch("/station/"+ document.getElementsByName("stations")[0].value).then(response =>{
            response.text().then(text => document.getElementById("content"). innerHTML = text);
        })
    }
}

function searchstation(){
    if(document.getElementsByName("search")[0].value != ''){
        fetch("/station/"+ document.getElementsByName("search")[0].value).then(response =>{
            response.text().then(text => document.getElementById("content"). innerHTML = text);
        })
    }
}

function ULTRAsearchstation(){
    start_date = document.querySelector("#startdate").value;
    end_date = document.querySelector("#enddate").value;
    start_hour = document.querySelector("#starttime").value;
    end_hour = document.querySelector("#endtime").value;
    percent = document.querySelector("#sliderval").innerHTML;
    
    fetch("/ultra/" + start_date +"/" + end_date +"/"+ start_hour + "/" + end_hour +"/"+ percent).then(response =>{
        response.text().then(text => document.getElementById("ultra-search-result"). innerHTML = text);
    })
}

function searchstationGeo(){ 
    fetch('station/geo', {
        method: 'post',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
            },
        body: JSON.stringify( JSON.parse('{ "geojson" :'+ document.getElementById("geojson").value +'}'))
    }).then(response =>{
            response.text().then(text => document.getElementById("toggled"). innerHTML = text);
        })

}

function togglestation(state){ // state is true or false
    if(state != true && state != false){
        return;
    }
    fetch('toggle/'+state, {
        method: 'post',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
            },
        body: JSON.stringify( JSON.parse('{ "geojson" :'+ document.getElementById("geojson").value +'}'))
    }).then(response =>{
            response.text().then(text => document.getElementById("toggled"). innerHTML = text);
        })

}

function editstation(object_id){
    fetch("/getstation/"+ object_id).then(response =>{
            response.text().then(text => {
                console.log(JSON.parse(text));
                document.querySelector("#editstation").value = JSON.stringify(JSON.parse(text));
            })
    });
}

function saveChanges(){
    station = JSON.parse(document.querySelector("#editstation").value)
    station._id = station._id["$oid"]
    fetch('edit/'+station._id, {
        method: 'post',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
            },
        body: JSON.stringify( station )
    }).then(response =>{ 
        toast("Save", "done")
    })
}

function toast(header, text){
    t = document.querySelector(".toast");
    t.querySelector(".toast-header").innerHTML = "<strong class='mr-auto'>"+header+"</strong>";
    t.querySelector(".toast-body").innerHTML = text;
    for (let i = 0; i < 100; i++) {
            setTimeout(()=>{
                t.style.opacity = i;
            }, i*5)
        }
        setTimeout(()=>{
            t.style.opacity = 0;
        }, 2000)
}