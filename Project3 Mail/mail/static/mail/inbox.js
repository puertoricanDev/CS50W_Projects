document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#send-mail').addEventListener('click', send_email);
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  
  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(mailid) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#mail-view').style.display = 'none';
  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
  fetch(`/emails/${mailid}`)
  .then(response => response.json())
  .then(emails => {
    if(emails.sender==undefined){

    }else{
      document.querySelector('#compose-recipients').value = emails.sender;
      document.querySelector('#compose-body').value = 'On '+emails.timestamp+" "+
      emails.recipients+" wrote: "+emails.body;
      var n = emails.subject.search("Re:")
      if(n==0){
        document.querySelector('#compose-subject').value = 'Re: '+ emails.subject.slice(n+3);
      }else{
        document.querySelector('#compose-subject').value = 'Re: '+ emails.subject;
      }
      
    }
  })
}

function get_emails(type) {
  
  var inbx = document.getElementById("inbox_mail")
  if(document.body.contains(inbx)){
    inbx.remove()
    
  }
  
  var y = document.createElement("div");
  y.setAttribute("id", "inbox_mail");
  document.querySelector("#emails-view").append(y);
  var backColor="white";
  var in_sent = "inbox";
  var sen_rec = "Sender: ";
  fetch(`/emails/${type}`)
  .then(response => response.json())
  .then(emails => {
    
    // Print emails
    for (email in emails){
      if(emails[email].read == true){
        backColor = 'gray';
      }else{
        backColor = 'white'
      }
      if(`${type}` == "sent"){
        in_sent = `${emails[email].recipients}`;
        sen_rec = "Recipients: ";
      }else{
        in_sent = `${emails[email].sender}`;
        sen_rec = "Sender: ";
      }
      y = document.createElement("div")
      y.setAttribute("id", `in${email}`);
      y.setAttribute("onclick", `load_a_mail(${emails[email].id}, "${type}")`);
      document.querySelector("#inbox_mail").append(y); 
      var z = document.createElement("div");
      z.style.float = 'left';
      z.style.width = '30%';
      z.style.background = backColor;
      z.style.border = "solid black";
      z.innerHTML=(sen_rec+in_sent);
      document.querySelector(`#in${email}`).append(z);
      z = document.createElement("div");
      z.style.float = 'left';
      z.style.width = '30%';
      z.style.background = backColor;
      z.style.border = "solid black";
      z.innerHTML=(" Subject: "+`${emails[email].subject}`);
      document.querySelector(`#in${email}`).append(z);
      z = document.createElement("div");
      z.style.float = 'left';
      z.style.width = '30%';
      z.style.background = backColor;
      z.style.border = "solid black";
      z.innerHTML=(" Timestamp: "+`${emails[email].timestamp}`);
      document.querySelector(`#in${email}`).append(z);
      
    }
  })
}
function load_mailbox(mailbox){
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#mail-view').style.display = 'none';
  // Show the mailbox name
  document.querySelector('#header').innerHTML=`${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}`;
  get_emails(mailbox);
  
};


function load_a_mail(mailid, type){
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#mail-view').style.display = 'block';
  var inbx = document.getElementById("a_mail")
  if(document.body.contains(inbx)){
    inbx.remove()
    
  }
  var w = document.createElement("div");
  w.setAttribute("id", "a_mail");
  document.querySelector("#mail-view").append(w);
  fetch(`/emails/${mailid}`,{
    method: 'PUT',
    body: JSON.stringify({
        read: true
      })
  })
  fetch(`/emails/${mailid}`)
  .then(response => response.json())
  .then(emails => {
      w = document.createElement("div");
      w.innerHTML = ("Sender: "+`${emails.sender}`);
      document.querySelector('#a_mail').append(w)
      w = document.createElement("div");
      w.innerHTML = ("Recipients: "+`${emails.recipients}`);
      document.querySelector('#a_mail').append(w)
      w = document.createElement("div");
      w.innerHTML = ("Subject: "+`${emails.subject}`);
      document.querySelector('#a_mail').append(w)
      w = document.createElement("div");
      w.innerHTML = (" Timestamp: "+`${emails.timestamp}`);
      document.querySelector('#a_mail').append(w)
      w = document.createElement("div");
      w.innerHTML = ("Body: "+`${emails.body}`);
      document.querySelector('#a_mail').append(w)
      if(`${type}`!="sent" ){
        w = document.createElement('button')
        w.setAttribute("onclick",`compose_email(${emails.id})`)
         w.setAttribute("class","btn btn-sm btn-outline-primary")
        w.innerHTML = "Reply: "
        document.querySelector('#a_mail').append(w)
      };
      
      if(`${type}`=="inbox" ){
        w = document.createElement('button')
        w.setAttribute("onclick",`put_archive(${emails.id},true)`)
        w.setAttribute("class","btn btn-sm btn-outline-primary")
        w.innerHTML = "Archive"
        document.querySelector('#a_mail').append(w)       
       };
       if(`${type}`=="archive" ){
        w = document.createElement('button')
        w.setAttribute("onclick",`put_archive(${emails.id},false)`)
        w.setAttribute("class","btn btn-sm btn-outline-primary")
        w.innerHTML = "Move to Inbox"
        document.querySelector('#a_mail').append(w)       
       };
         
  });
  
};
function put_archive(mailid, tof){
  fetch(`/emails/${mailid}`,{
    method: 'PUT',
    body: JSON.stringify({
        archived : tof
      })
  });
  if(tof==true){
   alert("Your Email had been archived.") 
  }else{
    alert("Your Email was moved to inbox.")
  };
  
  load_mailbox('inbox');
  
};
function add_email(contents) {

  // Create new post
  const email = document.createElement('TABLE');
  email.className = 'email';
  email.innerHTML = contents.sender + "  " + contents.body;

  // Add post to DOM
  document.querySelector('#emails-view').append(email);
};


function send_email() {
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
    })
  
  })
      alert("Your e-mail was sent.");
      load_mailbox('sent');
      
};