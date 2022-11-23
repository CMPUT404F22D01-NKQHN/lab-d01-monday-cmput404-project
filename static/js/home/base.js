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

function editPost(post_id_var) {

  // extract the post id from the post_id_var
  const post_id = post_id_var.split("/").pop();
  // extract author_id from post_id_var given http://localhost:8000/authors/b1aa5d08243c4bc4bf69bb220c09aa9f/posts/ca6df392b72941d8b9ca393331c5a554
  const author_id = post_id_var.split("/").slice(-3)[0];

  // to use relative path do ./authors/<author_id>/posts/<post_id>
  post_id_var = "./authors/" + author_id + "/posts/" + post_id;
  console.log(post_id_var);


  const title = prompt("Enter the title of your post");
  const content = prompt("Enter the content of your post");
  const source = prompt("Enter the source of your post");
  const origin = prompt("Enter the origin of your post");
  const description = prompt("Enter the description of your post");
  const unlisted = true;
  const visibility = "PUBLIC";
  const contentType = "text/plain";
  const data = {
    "title": title,
    "source": source,
    "origin": origin,
    "description": description,
    "unlisted": unlisted,
    "visibility": visibility,
    "contentType": contentType,
    "content": content
  }

  const options = {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie("csrftoken")
    },
    body: JSON.stringify(data)
  }
  fetch(post_id_var, options);
  location.reload();
}


function newComment(author_id, post_id) {
  const content = prompt("Enter the content of your comment");

  const data = {
    "post_id": post_id,
    "comment": content,
    "author_id": author_id
  }
  const options = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie("csrftoken")
    },
    body: JSON.stringify(data)
  }
  fetch(post_id + '/comments', options).then(response => {
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
      'X-CSRFToken': getCookie("csrftoken"),
      "Authorization": "Basic " + btoa("team1and2:team1and2")
      // TODO: Refactor this to pass credentials in the backend, and use the local server as a proxy
    },
    body: JSON.stringify(data)
  }
  console.log("SEND REQUEST TO: " + object_obj.id + "/inbox/")
  fetch(object_obj.id + "/inbox/", options).then((response) => alert("Request sent!")).catch((error) => alert("Error: " + error));
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
  fetch(author_url + "/followers/" + id, options).then((response) => location.reload());

}

async function newLike(author_id, post_id) {
  const author_obj = await fetch("./authors/" + author_id, { method: 'GET' }).then(response => response.json());
  const post_obj = await fetch(post_id, { method: 'GET' }).then(response => response.json());
  const summary = author_obj.displayName + " likes your post";
  const data = {
    "type": "like",
    "summary": summary,
    "author": author_obj,
    "object": post_id

  }
  fetch(post_obj.author.id + "/inbox", {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie("csrftoken")
    },
    body: JSON.stringify(data)
  }).then((response) => alert("Like sent!")).catch((error) => alert("Error: " + error));

}