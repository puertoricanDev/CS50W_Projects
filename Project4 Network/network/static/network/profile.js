document.addEventListener('DOMContentLoaded', function() {
  
  
    
    load_profile();
    });

    function to_follow(){
        uid = document.querySelector("#profuserid").className
        var t = document.getElementById("profuser").className
        fetch(`/ifollow/${uid}`)
        .then(response => response.json())
        if (document.querySelector("#follbtn").className == "btn btn-outline-danger"){
          document.querySelector("#follbtn").innerHTML = "Follow"
          document.querySelector("#follbtn").className = "btn btn-outline-success"
          var r = document.getElementById("pfollowers").className
          r=parseInt(r)
          r = r - 1
          document.getElementById("pfollowers").className = `${r}`
          document.getElementById("pfollowers").innerHTML = `${t} has ${r} followers.`
        }else{
          document.querySelector("#follbtn").innerHTML = "Unfollow"
          document.querySelector("#follbtn").className = "btn btn-outline-danger"
          var r = document.getElementById("pfollowers").className
          r=parseInt(r)
          
          r = r + 1 
          
          document.getElementById("pfollowers").className = `${r}`
          document.getElementById("pfollowers").innerHTML = `${t} has ${r} followers.`
        }
        
    }

    function load_profile(){
        var w = document.querySelector("#profuser").className
        var v = document.querySelector("#usrnm").className
        if(w==v){
          document.querySelector("#follbtn").style.display= "none";
        }else{
           //show btn
        }}
        