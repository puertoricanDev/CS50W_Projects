document.addEventListener('DOMContentLoaded', function() {
  document.querySelector('#commentboxbtn').addEventListener('click', ()=> show_comment("show"));
  document.querySelector('.close').addEventListener('click', ()=> show_comment("hide"));
  document.querySelector('#btnclose').addEventListener('click', ()=> show_comment("hide"));
  
  document.querySelector('#post_view').style.display = 'none';
  });
  function show_comment(show){
    if (show == "show"){
      document.querySelector('#post_view').style.display = 'block';
      document.querySelector('#btnviewdiv').style.display = 'none'; 
    }else{
      document.querySelector('#post_view').style.display = 'none';
      document.querySelector('#btnviewdiv').style.display = 'block';
      document.querySelector('#post-body').value = '';
    }
    
  };

  function showedit(postid){
    
    var u = document.querySelector(`#body${postid}`).innerHTML
    
    document.getElementById(`body${postid}`).innerHTML = ""
    
    var t = document.createElement("textarea")
    t.setAttribute("id",`edit${postid}`)
    t.setAttribute("class","form-control")
    t.innerHTML = u
    document.getElementById(`body${postid}`).append(t)
    document.getElementById(`edit${postid}`).required = true
    t = document.createElement("button")
    t.setAttribute("id",`editbtn${postid}`)
    t.setAttribute("class", "btn btn-info")
    t.setAttribute("onclick", `saveedit(${postid})`)
    t.innerHTML="Save"
    document.getElementById(`body${postid}`).append(t)
    document.querySelector(`#showedit${postid}`).style.display = "none"
  }

  function saveedit(postid){
    document.querySelector(`#showedit${postid}`).style.display = "block"
    var s = document.getElementById(`edit${postid}`).value
    fetch(`/saveedit/${postid}`, {
      method: 'POST',
      body: JSON.stringify({
        body: s
      })
    })
    document.getElementById(`body${postid}`).innerHTML=s
    document.getElementById(`edit${postid}`).remove()
    document.getElementById(`editbtn${postid}`).remove()
    
  }

  function tlike(postid,amount,liked,post){
    fetch("/ilike", {
      method: 'POST',
      body: JSON.stringify({
        id: postid})
      
    })
    
    if(liked == false){
      amount = parseInt(amount)+1;
      document.querySelector(`#btn${postid}`).className = "fas fa-heart";
      document.querySelector(`#btn${postid}`).setAttribute("onclick",`tlike(${postid},${amount},true,${post})`);
    }else{
      amount = parseInt(amount)-1;
      document.querySelector(`#btn${postid}`).className = "far fa-heart";
      document.querySelector(`#btn${postid}`).setAttribute("onclick", `tlike(${postid},${amount},false,${post})`);
    }
    document.querySelector(`#lk${postid}`).innerHTML=`Likes: ${amount}`;

    
  }    
  

  function new_Post(){
    fetch('/newpost', {
      method: 'POST',
      body: JSON.stringify({
        body: document.querySelector('#post-body').value})
    })
    

  }