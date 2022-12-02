function deletePost(post_id_var) {
  const post_id = post_id_var.split("/").pop();
  const author_id = post_id_var.split("/").slice(-3)[0];
  const url = "./authors/" + author_id + "/posts/" + post_id;

  const options = {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie("csrftoken"),
    }
  }
  // create an alert to confirm the deletion
  if (confirm("Are you sure you want to delete this post? This action cannot be undone.")) {
    fetch(url, options);
    location.reload();
  }
}
function getCookie(name) {
  const cookiesMap = {};
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      cookiesMap[cookies[i].split('=')[0].trim()] = decodeURIComponent(cookies[i].split('=')[1]);
    }
  }
  return cookiesMap[name];
}

function editProfile(author_id) {
  const newDisplayName = prompt("Enter your new display name");
  const newGithub = prompt("Enter your new github username");
  const newProfileImage = prompt("Enter your new profile image URL");
  // If the user cancels the prompt, don't do anything
  if (newDisplayName === null && newGithub === null && newProfileImage === null) {
    return;
  }
  let data = {};
  if (newDisplayName) {
    data.display_name = newDisplayName;
  }
  if (newGithub) {
    data.github = newGithub;
  }
  if (newProfileImage) {
    data.profileImage = newProfileImage;
  }
  const options = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie("csrftoken")
    },
    body: JSON.stringify(data)
  }
  fetch(author_id, options).then(res => res.json()).then(data => {
    if (data.error) {
      alert(data.error);
    } else {
      location.reload();
    }
  });


}

async function newComment(author_id, post_id) {
  const content = prompt("Enter the content of your comment");
  if (content === null) {
    return;
  }

  const author_obj = await fetch(author_id, { method: 'GET' }).then(response => response.json());
  const post_obj = await fetch(post_id, { method: 'GET' }).then(response => response.json());
  const summary = author_obj.displayName + " commented on your post";
  const reciever_uuid = post_obj.author.id.split("/").pop();
  const data = {
    "type": "comment",
    "summary": summary,
    "author": author_obj,
    "object": post_id,
    "comment": content,
  }
  const options = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie("csrftoken")
    },
    body: JSON.stringify(data)
  }
  fetch("/authors/" + reciever_uuid + "/inbox/", options).then(response => {
    if (response.ok) {
      location.reload();
    } else {
      alert("Error: " + response.status);
    }
  });
}

async function sendRequest(object_id, author_id) {
  const author_obj = await fetch(author_id, { method: 'GET' }).then(response => response.json());
  const object_obj = await fetch(object_id, { method: 'GET' }).then(response => response.json());

  const summary = author_obj.displayName + " wants to follow " + object_obj.displayName;
  const data = {
    "type": "follow",
    "summary": summary,
    "actor": author_obj,
    "object": object_obj

  }
  console.log(data);
  const options = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie("csrftoken")
      // TODO: Refactor this to pass credentials in the backend, and use the local server as a proxy
    },
    body: JSON.stringify(data)
  }
  object_obj.uuid = object_obj.id.split("/").pop();
  console.log("SEND REQUEST TO: " + object_obj.id + "/inbox/")
  fetch("/authors/" + object_obj.uuid + "/inbox/", options).then((response) => {
    if (response.ok) {
      alert("Request sent!");
    }
    else {
      alert("Error: " + response.status);
    }
  });

}

async function removeFollower(author_url, follow_id) {
  const id = follow_id
  const options = {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie("csrftoken")
    }
  }
  fetch(author_url + "/followers/" + id, options).then((response) => {

    if (response.ok) {
      location.reload();
    }
    else {
      alert("Error: " + response.status);
    }
  });

}

async function newLike(author_id, post_id, comment = false) {
  const author_obj = await fetch(author_id, { method: 'GET' }).then(response => response.json());
  const post_obj = await fetch(post_id, { method: 'GET' }).then(response => response.json());
  const summary = author_obj.displayName + (comment ? " likes your comment" : " likes your post");
  const data = {
    "type": "like",
    "summary": summary,
    "author": author_obj,
    "object": post_id

  }
  fetch("/authors/" + post_obj.author.uuid + "/inbox/", {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie("csrftoken")
    },
    body: JSON.stringify(data)
  }).then((response) => {
    if (response.ok) {
      alert("Like sent!");
    }
    else {
      alert("Error: " + response.status);
    }
  })

}

async function sharePost(author_id, post_url) {
  const author_obj = await fetch(author_id, { method: 'GET' }).then(response => response.json());
  const post_obj = await fetch(post_url, { method: 'GET' }).then(response => response.json());
  const summary = author_obj.displayName + " shared a post with you";
  const data = { ...post_obj, "type": "post", "summary": summary, "author": author_obj, "object": post_url }
  const followers = await fetch(author_id + "/followers", { method: 'GET' }).then(response => response.json());
  if (followers.items.length == 0) {
    alert("You have no followers to share with!");
    return;
  }
  console.log(followers);
  // Display a checkbox list of all followers
  const followers_list = followers.items.map((follower) => {
    return `<input type="checkbox" class="form-check-input" name="followers" value="${follower.uuid}">${follower.displayName}</input><br>`
  });
  const followers_html = `<h3>Select followers to share with</h3><form id="followers_form">${followers_list}
  <br>
  <div class="d-flex justify-content-around">
  <button type="button" class="btn btn-danger" id="share-button-close">Close</button>
  <button type="button" class="btn btn-primary" id="share-button-submit">Share</button>
  </div>
  </form>
  
  
  
  `;
  document.getElementById("shareForm").innerHTML = followers_html;
  document.getElementById("shareForm").style.display = "block";
  const buttons = document.getElementsByClassName("share-button")
  for (let i = 0; i < buttons.length; i++) {
    buttons[i].style.display = "none";
  }
  document.getElementById("share-button-close").style.display = "block";
  document.getElementById("share-button-close").addEventListener("click", () => {
    document.getElementById("shareForm").style.display = "none";
    for (let i = 0; i < buttons.length; i++) {
      buttons[i].style.display = "block";
    }
    document.getElementById("shareForm").innerHTML = "";
    document.getElementById("shareForm").style.display = "none";
  });
  document.getElementById("share-button-submit").addEventListener("click", () => {
    const checkboxes = document.getElementsByName("followers");
    const selected = [];
    for (let i = 0; i < checkboxes.length; i++) {
      if (checkboxes[i].checked) {
        selected.push(checkboxes[i].value);
      }
    }
    if (selected.length == 0) {
      alert("No followers selected!");
      return;
    }
    Promise.all(selected.map((follower) => {
      return fetch("/authors/" + follower + "/inbox/", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie("csrftoken")
        },
        body: JSON.stringify(data)
      })
    })).then((responses) => {
      const check = responses.every((response) => response.ok);
      if (check) {
        alert("Post shared!");
      }
      else {
        responses.forEach((response) => {
          if (!response.ok) {
            alert("Error: " + response.status);
          }
        }
        )
      }
    })
    document.getElementById("shareForm").style.display = "none";
    for (let i = 0; i < buttons.length; i++) {
      buttons[i].style.display = "block";
    }
    document.getElementById("shareForm").innerHTML = "";
    document.getElementById("shareForm").style.display = "none";
  });

}


function openForm() {
  document.getElementById("postForm").style.display = "block";
  document.getElementById("postButton").style.display = "block";
  document.getElementById("post-header").innerHTML = "Create Post";
  document.getElementById("editPostButton").style.display = "none";
  document.getElementById("post-type-content").innerHTML = "Post Type"
  document.getElementById("postType").style.display = "block";

}

function closeForm() {
  document.getElementById("postForm").style.display = "none";
  document.getElementById("postButton").style.display = "block";
}

function submitPost(author_id) {
  event.preventDefault();
  const title = document.getElementById("title").value;
  if (title == "") {
    alert("Title cannot be empty");
    return;
  }
  const source = "source"
  const origin = "origin"
  const description = document.getElementById("description").value;
  if (description == "") {
    alert("Description cannot be empty");
    return;
  }
  const unlisted = document.getElementById("unlisted").checked;
  const visibility = document.getElementById("visibility").value;
  const contentType = document.getElementById("postType").value;

  if (postType.value != "text/plain") {
    var content = document.getElementById(contentType).value;
  }

  if (postType.value == "text/markdown") {
    var converter = new showdown.Converter;
    content = converter.makeHtml(content);
  }

  if (postType.value == "text/plain") {
    content = document.getElementById("plain-text").value;
  }



  let data = {
    "title": title,
    "description": description,
    "source": source,
    "origin": origin,
    "unlisted": unlisted,
    "visibility": visibility,
    "contentType": contentType,
    "content": content
  }

  let options = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie("csrftoken")
    },
    body: JSON.stringify(data)
  }

  if (contentType == "image/png;base64") {
    // Read the file in base64
    const file = document.getElementById("image/png;base64").files[0];
    console.log(document.getElementById("image/png;base64"));
    console.log(file);

    const reader = new FileReader();
    reader.readAsDataURL(file);
    var read = false;
    reader.onload = () => {
      data.content = reader.result;
      options.body = JSON.stringify(data);
      fetch(author_id + '/posts/', options).then(() => {
        location.reload();
      })
    };
    reader.onerror = (error) => {
      alert("Error: " + error);
    };


  } else {
    fetch(author_id + '/posts/', options).then(() => {
      location.reload();
    })
  }

}

function editPost(post_url, contentType) {
  console.log(contentType);
  // extract the post id from the post_id_var
  const post_id = post_url.split("/").pop();
  // extract author_id from post_id_var given http://localhost:8000/authors/b1aa5d08243c4bc4bf69bb220c09aa9f/posts/ca6df392b72941d8b9ca393331c5a554
  const author_id = post_url.split("/").slice(-3)[0];

  // to use relative path do ./authors/<author_id>/posts/<post_id>
  let edit_post_url = "./authors/" + author_id + "/posts/" + post_id;


  openForm();

  document.getElementById("postButton").style.display = "none";
  document.getElementById("editPostButton").style.display = "block";
  document.getElementById("post-type-content").innerHTML = contentType;
  document.getElementById("post-header").innerHTML = "Edit Post";
  document.getElementById("postType").style.display = "none";

  if (contentType == "text/plain") {
    document.getElementById("post-type-content").innerHTML = "text/plain";
    document.getElementById("plain-text").style.display = "block";
    document.getElementById("text/markdown").style.display = "none";
  }
  if (contentType == "text/markdown") {
    document.getElementById("post-type-content").innerHTML = "text/markdown";
    document.getElementById("text/markdown").style.display = "block";
    document.getElementById("plain-text").style.display = "none";
  }
  // if its an image don't show anything
  if (contentType == "image/png;base64") {
    document.getElementById("text/markdown").style.display = "none";
    document.getElementById("plain-text").style.display = "none";
  }

  // if the edit button is clicked then we will do the same thing as submitPost but with a PUT request using the post_id_var
  document.getElementById("editPostButton").addEventListener("click", () => {
    event.preventDefault();
    const title = document.getElementById("title").value;
    if (title == "") {
      alert("Title cannot be empty");
      return;
    }
    const source = "source"
    const origin = "origin"
    const description = document.getElementById("description").value;
    if (description == "") {
      alert("Description cannot be empty");
      return;
    }
    const unlisted = document.getElementById("unlisted").checked;
    const visibility = document.getElementById("visibility").value;

    if (contentType != "text/plain") {
      var content = document.getElementById(contentType).value;
    }
    if (contentType == "text/markdown") {
      var converter = new showdown.Converter;
      content = converter.makeHtml(content);
    }
    if (contentType == "text/plain") {
      content = document.getElementById("plain-text").value;
    }

    let data = {
      "title": title,
      "description": description,
      "source": source,
      "origin": origin,
      "unlisted": unlisted,
      "visibility": visibility,
      "contentType": contentType,
      "content": content
    }

    let options = {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie("csrftoken")
      },
      body: JSON.stringify(data)
    }


    if (contentType == "image/png;base64") {
      // The file is already uploaded and it's id is post-img so we just need to get the base64 string and we have img source as the content
      const file = document.getElementById("post-img").src;
      const base64 = file.split("/").pop();
      data.content = base64;
      options.body = JSON.stringify(data);
      fetch(edit_post_url, options).then(() => {
        location.reload();
      })
    }
    else {
      fetch(edit_post_url, options).then(() => {
        location.reload();
      })
    }

  });
}