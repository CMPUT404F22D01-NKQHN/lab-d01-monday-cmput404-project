# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['UITestCase::test_home 1'] = '''
<!DOCTYPE html>
<html id = "page">
    <head>
        <meta charset="utf-8">
        <meta name="viewport"
              content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <link rel="stylesheet"
              type="text/css"
              href="/static/css/home/base.1511adcd216c.css">
        <title>Home</title>
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <a class="navbar-brand" href="/">Social Media Project</a>
            <button class="navbar-toggler"
                    type="button"
                    data-toggle="collapse"
                    data-target="#navbarSupportedContent"
                    aria-controls="navbarSupportedContent"
                    aria-expanded="false"
                    aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav mr-auto">
                    <li class="nav-item active">
                        <div class="form-popup" id="shareForm">
                        </div>
                        <div class="form-popup" id="postForm">
                            <h1>Create Post</h1>
                            <label for="title">
                                <b>Title</b>
                            </label>
                            <input id="title"
                                   type="text"
                                   placeholder="Enter Title"
                                   name="title"
                                   required>
                            <label for="description">
                                <b>Description</b>
                            </label>
                            <input id="description"
                                   type="text"
                                   placeholder="Enter Description"
                                   name="description"
                                   required>
                            <label for="categories">
                                <b>Categories</b>
                            </label>
                            <input type="text" placeholder="Enter Categories" name="categories" required>
                            <!-- Create a drop down for post type: text/markdown and image/png;base64 if image/png;base64 is selected, then create a button to upload image/png;base64
                                and if text/markdown is selected, then create a text area for text/markdown by default let it be empty -->
                            <label for="postType"></label>
                            <label for="postType">
                                <b>Post Type</b>
                            </label>
                            <select id="postType" name="postType">
                                <option value="text/markdown">
                                    Common Mark
                                </option>
                                <option value="image/png;base64">
                                    Upload Image
                                </option>
                                <option value="text/plain">
                                    text/plain
                                </option>
                            </select>
                            <!-- If the user selects image/png;base64 create a button to upload image/png;base64 -->
                            <input type="file"
                                   accept="image/png, image/jpeg"
                                   id="image/png;base64"
                                   name="uploadImage">
                            <textarea id="text/markdown" name="text/markdown" rows="4" cols="50">
</textarea>
                            <!-- Hide the upload image button and the text/markdown text area until the user selects the appropriate post type -->
                            <script>
                                    document.getElementById("image/png;base64").style.display = "none";
                                    document.getElementById("text/markdown").style.display = "block";
                                    document.getElementById("postType").addEventListener("change", function() {
                                        if (this.value == "image/png;base64") {
                                            // document.getElementById("uploadImageButton").style.display = "block"; 
                                            document.getElementById("image/png;base64").style.display = "block";
                                            document.getElementById("text/markdown").style.display = "none";
                                        } else if (this.value == "text/markdown") {
                                            document.getElementById("image/png;base64").style.display = "none";
                                            document.getElementById("text/markdown").style.display = "block";

                                        } else {
                                            document.getElementById("image/png;base64").style.display = "none";
                                            document.getElementById("text/markdown").style.display = "block";
                                        }
                                    });
                            </script>
                            <label for="unlisted">
                                <b>Unlisted</b>
                            </label>
                            <input id="unlisted" type="checkbox" name="unlisted"/>
                            <!-- For Visibility make it a selection box with public and private as options and by default make it public -->
                            <label for="visibility">
                                <b>Visibility</b>
                            </label>
                            <select id="visibility" name="visibility">
                                <option value="PUBLIC">
                                    Public
                                </option>
                                <option value="FRIENDS">
                                    Friends
                                </option>
                                <option value="PRIVATE">
                                    Private
                                </option>
                            </select>
                            <button type="submit" class="btn" onclick="submitPost(\'http://localhost:8000/authors/123\')">Create Post</button>
                            <button type="button" class="btn cancel" onclick="closeForm()">Close</button>
                        </div>
                        <button type="button"
                                id="postButton"
                                class="btn btn-primary"
                                onclick="openForm()">Create a Post</button>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/profile">Profile</a> <!-- Here we can put the logged in user\'s name instead of "Profile" -->
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/followers">Followers</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/inbox">Inbox</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/logout/">Logout</a>
                    </li>
                </ul>
            </div>
        </nav>
        <br/>
        <div id="content">
            
  <div class = "container">
    <h2> All Posts on Server </h2>
    <br>
    
    
    <div class="alert alert-info text-center" role="alert">
      <h2>There are no posts, try adding one!</h2>
    </div>
    
  
        </div>
    </body>
    <script>
        document.getElementById("postForm").style.display = "none";
   
    </script>
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.12.9/dist/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    <script src=/static/js/home/base.1b89639d08c9.js></script>
</html>
'''
