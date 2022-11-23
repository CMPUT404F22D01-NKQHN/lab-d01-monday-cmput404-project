function openForm() {
    document.getElementById("postForm").style.display = "block";
    document.getElementById("postButton").style.display = "none";
}

function closeForm() {
    document.getElementById("postForm").style.display = "none";
    document.getElementById("postButton").style.display = "block";
}

function submitPost(id){
  // have access to the form element, can make visible/popup
  // console.log(form);
  // console.log("I AM HERE");
  
  event.preventDefault();

  // const title = prompt("Enter the title of your post");
  // const content = prompt("Enter the content of your post");
  // const source = prompt("Enter the source of your post");
  // const origin = prompt("Enter the origin of your post");
  // const description = prompt("Enter the description of your post");
  console.log("Inside submit post AHHAHHAHAHAHAHA");
  //document.getElementById("fileData").innerHTML = x;
  const title = document.getElementById("title").value;
  const author_id = id;
  console.log(author_id);
  const source = "source"
  const origin = "origin"
  const description = document.getElementById("description").value;
  const unlisted = document.getElementById("unlisted").checked;
  // const content = document.getElementById("content").value;
  const visibility = "PUBLIC";
  const contentType = document.getElementById("postType").value;
  console.log("contentType: " + contentType);
  let content = document.getElementById(contentType).value;

  //wait 2 seconds
  
  // if (contentType == "text/markdown"){
  //   const content = document.getElementById("text/markdown").value;
  // }
  // else if (contentType == "plain/text"){
  //   const content = document.getElementById("text/markdown").value;
  // }
//   if (contentType == "image/png;base64"){
//     content = document.getElementById('fileup').innerHTML;
//   }
//   console.log("content: " + content);

  const data = {
    "title": title,
    "description": description,
    "source": source,
    "origin": origin,
    "unlisted": unlisted,
    "visibility": visibility,
    "contentType": contentType,
    "content": content
  }
  console.log("data: " + JSON.stringify(data));
  const options = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',   
      'X-CSRFToken': '{{ csrf_token }}'
    },
    body: JSON.stringify(data)
  }
  fetch('./authors/'+author_id+'/posts', options).then(()=>{
    location.reload();

  })


}